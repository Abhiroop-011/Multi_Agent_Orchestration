from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.theme import Theme

# Custom color theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "agent": "bold blue",
    "tool": "magenta"
})

console = Console(theme=custom_theme)

def print_header(text: str, subtitle: str = ""):
    """Prints a big bold header for the workflow."""
    console.print(Panel(
        f"[bold white]{subtitle}[/bold white]", 
        title=f"[bold cyan]{text}[/bold cyan]",
        expand=False,
        border_style="cyan"
    ))

def print_step(text: str):
    """Prints a workflow step notification."""
    console.print(f"\n[bold yellow] ➤ {text}[/bold yellow]")

def print_agent_start(role: str, model: str):
    """Prints a notification that an agent is starting."""
    # We don't print much here because we will use a spinner in the agent code
    pass 

def print_agent_response(role: str, content: str):
    """Renders the agent's output as a Markdown Panel."""
    md = Markdown(content)
    console.print(Panel(
        md,
        title=f"[bold blue]🤖 {role}[/bold blue]",
        subtitle="[dim]Task Complete[/dim]",
        border_style="blue",
        expand=True
    ))

def print_tool_call(tool_name: str, args: dict):
    """Shows that a tool is being called."""
    console.print(f"[dim]⚙️ Calling Tool: [bold magenta]{tool_name}[/bold magenta]...[/dim]")
    if "code" in args:
        # Render Python code nicely
        syntax = Syntax(args["code"], "python", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="[magenta]Python Code[/magenta]", border_style="dim"))

def print_tool_result(result: str):
    """Shows the output of a tool."""
    # If result is short, print simple. If long, panel it.
    if len(result) < 100:
        console.print(f"[dim]   ↳ Result: {result}[/dim]")
    else:
        console.print(Panel(result, title="[dim]Tool Output[/dim]", border_style="dim"))

def print_error(text: str):
    console.print(f"[error]❌ {text}[/error]")