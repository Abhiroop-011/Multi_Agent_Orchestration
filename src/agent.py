import os
import sys
import traceback
import google.genai as genai
from google.genai import types
from src.models import AgentModel
from src.tools import run_python, delegate_to_agent
import src.ui as ui  # <--- NEW IMPORT

class Agent:
    def __init__(self, config: AgentModel):
        self.id = config.id
        self.role = config.role
        self.goal = config.goal
        self.model = config.model

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            ui.print_error(f"GOOGLE_API_KEY not found for agent {self.id}")
            sys.exit(1)

        self.client = genai.Client(api_key=api_key)

        # Tool Config (Same as before)
        self.tool_config = None
        if config.tools:
            active_tools = []
            if "python" in config.tools: active_tools.append(run_python)
            if "delegate" in config.tools: active_tools.append(delegate_to_agent)

            if active_tools:
                self.tool_config = types.GenerateContentConfig(
                    tools=active_tools,
                    tool_config=types.ToolConfig(
                        function_calling_config=types.FunctionCallingConfig(mode="AUTO")
                    )
                )

    def execute(self, context: str) -> str:
        # History setup
        history = [
            types.Content(
                role="user",
                parts=[types.Part(text=f"You are a {self.role}. Goal: {self.goal}.\n{context}")]
            )
        ]

        try:
            while True:
                # --- UI: SPINNER START ---
                with ui.console.status(f"[bold blue]{self.role}[/bold blue] is thinking...", spinner="dots"):
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=history,
                        config=self.tool_config
                    )
                # --- UI: SPINNER END ---

                # Handle Function Calls
                if response.function_calls:
                    call = response.function_calls[0]
                    func_name = call.name
                    func_args = call.args
                    
                    # --- UI: PRINT TOOL CALL ---
                    ui.print_tool_call(func_name, func_args)

                    tool_output = ""
                    if func_name == "run_python":
                        tool_output = run_python(func_args.get("code"))
                    elif func_name == "delegate_to_agent":
                        # For delegation, we let the sub-agent print its own UI
                        tool_output = delegate_to_agent(func_args.get("agent_name"), func_args.get("task"))
                    else:
                        tool_output = f"Error: Unknown tool '{func_name}'"

                    # --- UI: PRINT RESULT ---
                    if func_name != "delegate_to_agent":
                        ui.print_tool_result(tool_output)

                    # Update history
                    history.append(response.candidates[0].content)
                    history.append(types.Content(
                        role="user",
                        parts=[types.Part.from_function_response(
                            name=func_name,
                            response={"result": tool_output}
                        )]
                    ))
                    continue

                # Final Response
                text = response.text or ""
                # --- UI: PRINT FINAL ANSWER ---
                # We only print the panel if we are NOT inside a delegation call being run by another agent
                # (Optional logic, but printing always is fine for now)
                ui.print_agent_response(self.role, text)
                
                return text

        except Exception as e:
            ui.print_error(f"Agent {self.id} failed: {e}")
            return str(e)