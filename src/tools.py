import sys
from io import StringIO
import traceback

# Global registry (keep existing logic)
AGENT_REGISTRY = {}

def set_registry(agents):
    global AGENT_REGISTRY
    AGENT_REGISTRY = agents

def run_python(code: str):
    """Executes Python code and returns the standard output."""
    # Note: We removed the 'print(EXECUTING)' lines because src/ui.py handles that now.
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        safe_globals = {"__builtins__": __builtins__, "print": print}
        exec(code, safe_globals)
        sys.stdout = old_stdout
        result = redirected_output.getvalue()
        if not result:
            result = "Code executed successfully (no output printed)."
        return result.strip()
    except Exception:
        sys.stdout = old_stdout
        return f"Error executing code:\n{traceback.format_exc()}"

def delegate_to_agent(agent_name: str, task: str):
    """Delegates a task to a sub-agent."""
    # We removed the print statements here too. The Agent class will handle UI.
    agent = AGENT_REGISTRY.get(agent_name)
    if not agent:
        return f"Error: Agent '{agent_name}' not found."
    
    try:
        # Recursive execution
        return agent.execute(task)
    except Exception as e:
        return f"Error calling agent: {e}"