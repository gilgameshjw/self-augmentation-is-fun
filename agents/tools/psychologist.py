
from langchain_community.chat_models import ChatOpenAI

def tool_psychologist(llm: ChatOpenAI, query: str, personality: str) -> str:
    """ you are a psychologist """
    prompt = f"{personality}:\n{query}"
    result = llm.invoke(prompt)

    return {
        "output": result.content,
        "agent": "psychologist",
    }
