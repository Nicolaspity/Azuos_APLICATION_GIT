from azuos_applied_flow.main import AzuosFlow, ReportState

def processar_kickoff(respostas):
    state = ReportState()
    flow = AzuosFlow(state=state)
    flow.respostas = respostas.strip()
    final_state = flow.kickoff()
    return final_state.dict()
