
import os
import time
import nest_asyncio # required for notebooks
import asyncio
nest_asyncio.apply()
from langchain_community.chat_models import ChatOpenAI


# using open source library gpt-researcher
from gpt_researcher import GPTResearcher

from formats.markdown import text_to_markdown


# report_types = ["research_report", "subtopic_report"]

async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()

    # Get additional information
    research_context = researcher.get_research_context()
    research_costs = researcher.get_costs()
    research_images = researcher.get_research_images()
    research_sources = researcher.get_research_sources()

    return report, research_context, research_costs, research_images, research_sources


def run_researcher(query: str, report_type: str, mock=True) -> str:
    t_0 = time.time()
    if not mock:
        research_report, research_context, research_costs, research_images, research_sources = asyncio.run(get_report(query, report_type))
    t_1 = time.time()
    research_time = t_1 - t_0
    print("costs::///////////////////////////////////////////////")
    #"""
    if not mock:
        # save to file
        print(research_costs)
        with open("checks/costs.txt", "w") as f:
            f.write(str(research_costs))
        print("report::///////////////////////////////////////////////")
        with open("checks/report.txt", "w") as f:
            f.write(research_report)
        print("context::///////////////////////////////////////////////")
        with open("checks/context.txt", "w") as f:
            f.write(str(research_context))
        print(research_context)
        print("images::///////////////////////////////////////////////")
        with open("checks/images.txt", "w") as f:
            f.write(str(research_images))
        print(research_images)
        print("sources::///////////////////////////////////////////////")
        with open("checks/sources.txt", "w") as f:
            f.write(str(research_sources))
        print(research_sources)
    if mock:
        # read research_report from txt file
        with open("checks/report.txt", "r") as f:
            research_report = f.read()
        # read research_costs from txt file
        with open("checks/costs.txt", "r") as f:
            research_costs = f.read()

    # write to markdown
    text_to_markdown(research_report, "tmp/report.md")

    return research_report, research_costs, research_time




def tool_researcher(llm: ChatOpenAI, config, query: str) -> str:
    """ you are a researcher """
    prompt = f"""
If you find a research or question in the user query, return a sentence with the question but starting with research.

Otherwise, ask the user to provide more information.

user query:
{query}
"""
    result = llm.invoke(prompt)

    report_type = "research_report"

    query = result.content.strip()
    if query.startswith("research"):
        # query = query[8:].strip()
        research_report, research_costs, research_time = run_researcher(query, report_type, config.mock)
        response = f"find below a detailed answer to your question: \n{query}"
        print(f"costs: {research_costs}")
        print(f"time: {research_time}")
        # Save the full report to a temporary file
        report_file_path = "tmp/report.md"
        os.makedirs(os.path.dirname(report_file_path), exist_ok=True)  # Ensure the directory exists
        with open(report_file_path, "w", encoding="utf-8") as f:
            f.write(research_report)
        
    else:
        response = query
        report_file_path = None
        research_costs = 0.0
        research_time = 0.0

        
    # write research costs and time to chat in dictionary format:
    d_research = {
        "status": "completed",
        "costs": research_costs,
        "time": research_time
    }

    return {
        "research_metadata": d_research,
        "output": response,
        "agent": "researcher",
        "file_data": report_file_path     
    }
