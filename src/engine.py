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
            # (Legacy support code here, or just route everything through conditional)
            self._run_sequential(initial_input)
        elif self.config.workflow.type == "parallel":
            self._run_parallel(initial_input)

    def _run_conditional(self, context: str):
        """
        Executes a workflow by following 'next_step' pointers.
        """
        # 1. Build a map of step_id -> step_object for fast lookup
        step_map = {s.id: s for s in self.config.workflow.steps}
        
        # 2. Start at the defined start_step
        current_step_id = self.config.workflow.start_step
        
        # Safety: Prevent infinite loops
        max_steps = 10 
        steps_taken = 0
        
        while current_step_id and steps_taken < max_steps:
            step = step_map.get(current_step_id)
            if not step:
                ui.print_error(f"Step '{current_step_id}' not found!")
                break
                
            agent = self.agents[step.agent]
            ui.print_step(f"Executing Step '{step.id}' (Agent: {agent.role})")
            
            # 3. Execute Agent
            # Note: We prepend previous context so they have memory
            full_context = f"Previous Context: {context}"
            output = agent.execute(full_context)
            context = output # Update context for next person
            
            steps_taken += 1

            # 4. Determine Next Step (The Routing Logic)
            next_id = None
            
            # Check conditions first
            if step.conditions:
                for condition in step.conditions:
                    if condition.target in output:
                        ui.print_step(f"⚡ Condition Met: Found '{condition.target}', jumping to '{condition.step}'")
                        next_id = condition.step
                        break
            
            # If no condition met, use default next
            if not next_id:
                next_id = step.next_step
            
            # Move to next
            current_step_id = next_id

        if steps_taken >= max_steps:
            ui.print_error("Terminated: Max steps reached (Infinite Loop Protection)")
        else:
            ui.print_step("Workflow Complete")

    # ... (Keep _run_sequential and _run_parallel as they were)
    def _run_sequential(self, context: str):
        # (Paste your previous _run_sequential code here)
        pass 
        
    def _run_parallel(self, context: str):
        # (Paste your previous _run_parallel code here)
        pass