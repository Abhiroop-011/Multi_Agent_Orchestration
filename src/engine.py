import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.models import ConfigModel
from src.agent import Agent
from src.tools import set_registry
import src.ui as ui

class Orchestrator:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.agents = {a.id: Agent(a) for a in self.config.agents}
        set_registry(self.agents)

    def _load_config(self, path: str) -> ConfigModel:
        with open(path, "r") as f:
            return ConfigModel(**yaml.safe_load(f))

    def run(self, initial_input: str):
        ui.print_header("Agent Orchestrator", f"Workflow: {self.config.workflow.type.upper()}")
        
        if self.config.workflow.type == "conditional":
            self._run_conditional(initial_input)
        elif self.config.workflow.type == "sequential":
            self._run_sequential(initial_input)
        elif self.config.workflow.type == "parallel":
            self._run_parallel(initial_input)

    def _run_sequential(self, context: str):
        """Runs agents one after another."""
        for step in self.config.workflow.steps:
            agent = self.agents[step.agent]
            ui.print_step(f"Passing context to [bold white]{agent.role}[/bold white]")
            context = agent.execute(context)

    def _run_parallel(self, context: str):
        """Runs agents simultaneously and aggregates results."""
        results = {}
        ui.print_step(f"Spawning parallel agents: {self.config.workflow.branches}")
        
        with ThreadPoolExecutor() as executor:
            future_to_agent = {
                executor.submit(self.agents[agent_id].execute, context): agent_id 
                for agent_id in self.config.workflow.branches
            }
            
            for future in as_completed(future_to_agent):
                agent_id = future_to_agent[future]
                try:
                    output = future.result()
                    results[agent_id] = output
                except Exception as e:
                    ui.print_error(f"{agent_id} failed: {e}")

        ui.print_step("Aggregating results & passing to Reviewer...")
        
        combined_output = "Here are the proposals from the team:\n\n"
        for agent_id, output in results.items():
            combined_output += f"--- {agent_id.upper()} PROPOSAL ---\n{output}\n\n"

        if self.config.workflow.then:
            reviewer = self.agents[self.config.workflow.then.agent]
            reviewer.execute(combined_output)

    def _run_conditional(self, context: str):
        """Runs agents with dynamic routing (loops/jumps)."""
        step_map = {s.id: s for s in self.config.workflow.steps}
        current_step_id = self.config.workflow.start_step
        
        max_steps = 15
        steps_taken = 0
        
        while current_step_id and steps_taken < max_steps:
            step = step_map.get(current_step_id)
            if not step:
                ui.print_error(f"Step '{current_step_id}' not found!")
                break
                
            agent = self.agents[step.agent]
            ui.print_step(f"Executing Step '{step.id}' (Agent: {agent.role})")
            
            # Execute
            full_context = f"Previous Context: {context}"
            output = agent.execute(full_context)
            context = output 
            
            steps_taken += 1

            # Routing
            next_id = None
            if step.conditions:
                for condition in step.conditions:
                    if condition.target in output:
                        ui.print_step(f"⚡ Condition Met: Found '{condition.target}', jumping to '{condition.step}'")
                        next_id = condition.step
                        break
            
            if not next_id:
                next_id = step.next_step
            
            current_step_id = next_id

        if steps_taken >= max_steps:
            ui.print_error("Terminated: Max steps reached (Loop Protection)")
        else:
            ui.print_step("Workflow Complete")