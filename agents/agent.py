
from typing import Dict, Any, List, Tuple, Union
from langchain.agents import Tool
from langchain_community.chat_models import ChatOpenAI

from agents.tools.researcher import tool_researcher
from agents.tools.coder import tool_coder
from agents.tools.psychologist import tool_psychologist
from agents.tools.sexologist import tool_sexologist
from agents.tools.drdoc import tool_drdoc

from agents.agent_executor import AgentExecutor


def set_up_agent(config):
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0125", 
        temperature=0, 
        api_key=config.llm["api_key"]
    )

    psychologist_tool = Tool(
        name="Psychologist",
        func=lambda query: tool_psychologist(llm, query, config.d_agent_personalities["psychologist"]),
        description=config.d_agent_personalities["psychologist"]
    )

    sexologist_tool = Tool(
        name="Sexologist",
        func=lambda query: tool_sexologist(llm, query, config.d_agent_personalities["sexologist"]),
        description=config.d_agent_personalities["sexologist"]
    )

    researcher_tool = Tool(
        name="Researcher",
        func=lambda query: tool_researcher(llm, config, query),
        description=config.d_agent_personalities["researcher"]
    )

    coder_tool = Tool(
        name="Coder",
        func=lambda query: tool_coder(llm, query, config.d_agent_personalities["coder"]),
        description=config.d_agent_personalities["coder"]
    )

    drdoc_tool = Tool(
        name="DrDoc",
        func=lambda query: tool_drdoc(llm, query, config.d_agent_personalities["drdoc"]),
        description=config.d_agent_personalities["drdoc"]
    )

    tools = [psychologist_tool, sexologist_tool, researcher_tool, coder_tool, drdoc_tool]
    # Initialize the agent
    return AgentExecutor(
            llm=llm, \
            tools=tools, \
            agent_personality=config.d_agent_personalities["main_agent"], \
            agent_avatars=config.d_agent_avatars, \
            verbose=True, \
            maximal_steps=config.thinking_depth
        )
