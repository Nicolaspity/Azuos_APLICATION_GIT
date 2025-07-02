#!/usr/bin/env python
import os
import json
from openai import OpenAI
from random import randint
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from crewai import LLM
from azuos_applied_flow.crews.content_crew.content_crew import ContentCrew
from azuos_applied_flow.crews.capacitation_crew.capacitation_crew import CapacitationCrew
from fpdf import FPDF  # Para salvar o relatório em PDF


class ReportState(BaseModel):
    respostas: str = ""
    interpretacao: str = ""
    relatorio: str = ""
    trilha: str = ""


class AzuosFlow(Flow[ReportState]):

    @start()
    def receber_respostas(self):
        print("📩 Recebendo respostas do formulário...")
        # Corrigido: acessa diretamente o atributo recebido pelo input
        self.state.respostas = getattr(self, "respostas", "").strip()
        # print("DEBUG respostas recebidas:", repr(self.state.respostas))

    @listen(receber_respostas)
    def interpretar_respostas(self):
        print("🧠 Interpretando respostas com base no código de ética...")
        # Leia o conteúdo do arquivo YAML
        with open("knowledge/form_questions/form.yaml", "r", encoding="utf-8") as f:
            questionnaire_content = f.read()
        result = ContentCrew().crew().kickoff(
            inputs={"form_interpretation_task": self.state.respostas,
                   "questionnaire": questionnaire_content}
        )


        self.state.interpretacao = result.raw
        return "Interpretação concluída"

    @listen(interpretar_respostas)
    def gerar_relatorio(self):
        print("📝 Gerando relatório com base na interpretação...")

        result = ContentCrew().crew().kickoff(
            inputs={"reporting_task": self.state.interpretacao,
                    "form_interpretation_task": self.state.respostas,
                    "questionnaire": "knowledge/form_questions/form.yaml"
                }
        )

        self.state.relatorio = result.raw
        relatorio_ajustado = self.state.relatorio.replace("—", "-")
        # Salvando relatório em PDF
        os.makedirs("outputs", exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for linha in relatorio_ajustado.split("\n"):
            pdf.multi_cell(0, 10, linha.replace("—", "-").replace("’", "'").replace("“", '"').replace("”", '"').replace("…", "..."))

        pdf.output("outputs/relatorio_final.pdf")
        print("✅ Relatório salvo em: outputs/relatorio_final.pdf")
    @listen(interpretar_respostas)
    def gerar_trilha_formativa(self):
        print("📚 Escrevendo seção da trilha de capacitação...")

        # 1️⃣ Rodar a Crew
        result = CapacitationCrew().crew().kickoff(
            inputs={"topic_writing_task": self.state.interpretacao}
        )

        self.state.trilha = result.raw
    @listen(gerar_trilha_formativa)
    def gerar_modulos(self):
        trilha = json.loads(self.state.trilha)
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        for idx, modulo in enumerate(trilha, start=1):
            nome = modulo.get("nome", "Sem título")
            descricao = modulo.get("descricao", "")
            justificativa = modulo.get("justificativa", "")
            prompt = f"""
                        Você é um especialista em educação e precisa escrever um conteúdo didático sobre o tema abaixo.
            O texto deve ser claro, informativo e voltado para estudantes de nível médio ou superior.
            Use uma linguagem acessível, mas com profundidade e riqueza de explicações.

            Tema: {nome}
            Descrição: {descricao}
            Justificativa: {justificativa}

            Com base nessas informações, elabore um texto estruturado com:

            1. Uma introdução contextualizando o tema.
            2. Desenvolvimento com explicações claras, exemplos e aprofundamento.
            3. Uma conclusão que reforce a importância do tema.

            Evite jargões técnicos excessivos e mantenha um tom envolvente.
            O objetivo é tornar o conteúdo compreensível e atrativo. """
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um especialista em educação"},
                    {"role": "system", "content": prompt},
                ],
                temperature=0.7
            )
            texto = response.choices[0].message.content.strip()
            
            #Gerar PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            def clean_text(text):
                return (
                    text.replace("—", "-")
                        .replace("’", "'")
                        .replace("“", '"')
                        .replace("”", '"')
                        .replace("…", "...")
                )

            for line in texto.split("\n"):
               pdf.multi_cell(0, 10, clean_text(line))

            pdf_path = os.path.join(output_dir, f"modulo_{idx}.pdf")
            pdf.output(pdf_path, 'F')
        return self.state


def kickoff():
    flow = AzuosFlow()
    flow.kickoff()


def plot():
    flow = AzuosFlow()
    flow.plot()


if __name__ == "__main__":
    kickoff()
