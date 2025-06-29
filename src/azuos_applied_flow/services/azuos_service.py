from azuos_applied_flow.main import AzuosFlow, ReportState

def processar_kickoff(respostas):
    state = ReportState()
    flow = AzuosFlow(state=state)
    final_state = flow.kickoff(inputs={"respostas": respostas})
    return final_state.dict()
