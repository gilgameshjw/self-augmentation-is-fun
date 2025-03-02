
from typing import Dict, Any, List, Tuple, Union
# from langchain.agents import Tool


# Custom agent to understand what is going on...
# To be upgraded later on.
# for instance: https://arxiv.org/abs/2210.03629

class AgentExecutor:
    def __init__(self, llm, tools: List, agent_personality: str, agent_avatars: dict, verbose: bool = False, maximal_steps: int = 10):
        """
        Initialize the agent.
        :param llm: The LLM used for reasoning.
        :param tools: A list of tools available for the agent to use.
        :param verbose: Whether to print intermediate steps for debugging.
        :param maximal_steps: Maximum number of steps allowed in the execution loop.
        """
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.tool_descriptions = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools.values()]
        )
        self.personality = agent_personality
        self.avatars = agent_avatars
        self.verbose = verbose
        self.maximal_steps = maximal_steps

    def preprocess_chat_history(self, chat_history: List[str]):
        """
        Preprocess the chat history by joining it into a single string.
        :param chat_history: The conversation history to provide context.
        :return: The preprocessed chat history string.
        """
        print(f"chat_history: {chat_history}")
        return "\n".join([f"role: {h['role']}\ncontent: {h['content']}" for h in chat_history]) \
            if chat_history else "No previous conversation."
    
    def set_agent_prompt(self, chat_history: List[str], query: str):
        """
        Create a prompt for the LLM to generate the best possible answer based on the query and conversation history.
        :param chat_history: The conversation history to provide context.
        :param query: The user's input query.
        :return: The prompt string for the LLM.
        """
        chat_context = self.preprocess_chat_history(chat_history)
        prompt = (
                    f"Agent Personality:\n{self.personality}\n"
                    f"Agent Tools:\n{self.tools}\n"
                    f"Agent Tools Descriptions:\n{self.tool_descriptions}\n"
                    f"Conversation history:\n{chat_context}\n\n"
                    f"Current Query: {query}\n\n"
                    "Provide the best possible answer based on the query and conversation history."
                )
        return prompt

    def decide_tool(self, query: str, chat_history: List[str]) -> str:
        """
        Use the LLM to decide which tool to use based on the query and chat history.
        :param query: The user's input query.
        :param chat_history: The conversation history to provide context.
        :return: The name of the tool to use, or None if no tool is applicable.
        """
        # Create a prompt for the LLM to decide the tool
        chat_context = self.preprocess_chat_history(chat_history)
        prompt = (
            f"Agent Personality:\n{self.personality}\n"
            f"Available tools:\n{self.tool_descriptions}\n\n"
            f"Conversation history:\n{chat_context}\n\n"
            f"Query: {query}\n\n"
            "Based on the query and conversation history, decide which tool to use and return just the tool name.\n"
            "If none of the tools are applicable, respond with 'None'.\n"
            "Tool name:"
        )

        # Invoke the LLM to get the decision
        print(prompt)
        result = self.llm.invoke(prompt)
        tool_name = result.content.strip()
        print(f"decide_tool:")
        print(f"tool_name: {tool_name}")
        print("-----")

        print(tool_name.strip() in self.tools)
        print(f"self.tools {self.tools.keys()}")
        print(1234567)
        print(tool_name == "Psychologist")
        # write tool_name to file
        with open("tool_name.txt", "w") as f:
            f.write(tool_name)

        # Return the tool name if it matches one of the available tools
        if tool_name in self.tools:
            return tool_name
        return None

    def execute(self, inputs: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Execute the agent and return the appropriate output format.
        :param inputs: Dictionary of inputs for the agent (includes 'input' and 'chat_history').
        :return: A dictionary if a tool is used, or a string if the LLM provides the best possible answer.
        """
        intermediate_steps: List[Tuple[dict, Any]] = []
        query = inputs.get("input", "")
        chat_history = inputs.get("chat_history", [])
        step_count = 0

        while step_count < self.maximal_steps:
            step_count += 1

            # Decide which tool to use (or provide the best possible answer)
            tool_name = self.decide_tool(query, chat_history)

            if tool_name:
                # Execute the selected tool
                tool = self.tools[tool_name]
                tool_result = tool.run(query)

                # Log intermediate steps if verbose
                if self.verbose:
                    print(f"Step {step_count}: Using tool '{tool_name}'")
                    print(f"Tool result: {tool_result}")

                # Add the step to intermediate steps
                intermediate_steps.append(({"tool": tool_name, "tool_input": query}, tool_result))

                # If the tool result is a dictionary, return it immediately
                if isinstance(tool_result, dict):
                    return tool_result

            else:
                # If no tool is selected, ask the LLM to generate the best possible answer
                prompt = self.set_agent_prompt(chat_history, query)
                result = self.llm.invoke(prompt)
                best_answer = result.content.strip()

                if self.verbose:
                    print(f"Step {step_count}: No tool selected. Best possible answer: {best_answer}")
                return best_answer

        # If maximal steps are reached, return the best possible answer
        prompt = self.set_agent_prompt(chat_history, query)
        result = self.llm.invoke(prompt)
        best_answer = result.content.strip()

        if self.verbose:
            print(f"Step {step_count}: Maximal steps reached. Best possible answer: {best_answer}")
        return best_answer

    def invoke(self, inputs: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
            Here performing postprocessing
        """
        agent_response = self.execute(inputs)
        if type(agent_response) == dict:
            agent_response["avatar"] = self.avatars[agent_response["agent"]]
            return agent_response
        else:
            return {"output": agent_response, "avatar": self.avatars["main_agent"]}
        return agent_response

