
import os
import time
import nest_asyncio # required for notebooks
import asyncio
nest_asyncio.apply()
from langchain_community.chat_models import ChatOpenAI

# using open source library gpt-researcher
from gpt_researcher import GPTResearcher

from formats.markdown import text_to_markdown, markdown_to_pdf


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
    print(mock)
    if not mock:
        research_report, research_context, research_costs, research_images, research_sources = \
            asyncio.run(get_report(query, report_type))
    t_1 = time.time()
    research_time = t_1 - t_0
    print("costs::///////////////////////////////////////////////")
    
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

    else:
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
Analyze the user query below and follow these instructions:

1. If the query contains a research-related statement or question (including simple questions):
   - Extract the core topic or question.
   - Rephrase it to start with the word "research" while preserving the original meaning.
   - Return ONLY the rephrased question starting with "research."

2. If the query does not contain a clear research-related statement or question:
   - Return ONLY the message: "Please provide a clear question or specify your research topic."

Examples:
- Query: "I want to research the number of frogs in the universe"
  Output: "research the number of frogs in the universe"

- Query: "What is the result of this particular equation?"
  Output: "research what is the result of this particular equation?"

- Query: "How many ants are in the world?"
  Output: "research how many ants are in the world?"

- Query: "I need to speak with a researcher"
  Output: "Please provide a clear question or specify your research topic."

- Query: "I have a question here"
  Output: "Please provide a clear question or specify your research topic."

User Query:
{query}
"""
    result = llm.invoke(prompt)
    processed_query = result.content.strip()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(config.mock)
    print(processed_query)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@")

    if processed_query.lower().startswith("research"):

        report_type = "research_report"
        research_report, research_costs, research_time = \
            run_researcher(processed_query, report_type, config.mock)
        response = f"find below a detailed answer to your question: \n{processed_query}"
        print(f"costs: {research_costs}")
        print(f"time: {research_time}")

        # Save the full report to a temporary file
        report_file_path = "./tmp/report.md"
        os.makedirs(os.path.dirname(report_file_path), exist_ok=True)  # Ensure the directory exists
        with open(report_file_path, "w", encoding="utf-8") as f:
            f.write(research_report)

        report_file_path_pdf = report_file_path.replace(".md", ".pdf")
        markdown_to_pdf(report_file_path, report_file_path_pdf)
        
        d_research = {
            "status": "completed",
            "costs": research_costs,
            "time": research_time
        }

        return {
            "research_metadata": d_research,
            "file_data": report_file_path_pdf,
            "output": response,
            "agent": "researcher"
        }
    

    return {
        "output": processed_query,
        "agent": "researcher"
    }
