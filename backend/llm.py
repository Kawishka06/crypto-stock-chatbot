from backend.config import LLM_PROVIDER

def generate_reply(prompt:str) -> str:
    if LLM_PROVIDER =="mock":
        return prompt
    
    raise NotImplementedError("Set LLM_PROVIDER and implement provider client.")