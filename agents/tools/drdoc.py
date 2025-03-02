
from langchain_community.chat_models import ChatOpenAI

def tool_drdoc (llm: ChatOpenAI, query: str, personality: str) -> str:
    """ you are a automation helper in medical space """
    prompt = f"{personality}:\n{query}"
    result = llm.invoke(prompt)

    return {
        "output": result.content,
        "agent": "drdoc",
    }