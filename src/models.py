from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field

class AgentModel(BaseModel):
    id: str = Field(..., description="Unique identifier for the agent")
    role: str = Field(..., description="The role of the agent")
    goal: str = Field(..., description="The objective")
    model: str = Field("gemini-1.5-flash", description="The LLM model")
    tools: Optional[List[str]] = Field(default_factory=list, description="List of tools")

# NEW: Defines "If output contains X, go to Y"
class ConditionModel(BaseModel):
    target: str = Field(..., description="The text to look for (e.g., 'RETRY')")
    step: str = Field(..., description="The step ID to jump to if target is found")

class StepModel(BaseModel):
    id: str = Field(..., description="Unique ID for this step (needed for looping)")
    agent: str = Field(..., description="The ID of the agent to execute")
    # NEW: A step can now have routing logic
    conditions: Optional[List[ConditionModel]] = Field(None, description="Conditional routing logic")
    next_step: Optional[str] = Field(None, description="The default next step ID")

class WorkflowModel(BaseModel):
    # We are switching to a more graph-like structure
    type: Literal["sequential", "parallel", "conditional"] = Field(..., description="Execution mode")
    
    # Common fields
    steps: Optional[List[StepModel]] = Field(None, description="List of steps")
    start_step: Optional[str] = Field(None, description="ID of the first step to run")

    # Parallel fields (keep for compatibility)
    branches: Optional[List[str]] = Field(None, description="Parallel agents")
    then: Optional[StepModel] = Field(None, description="Aggregation step")

class ConfigModel(BaseModel):
    agents: List[AgentModel]
    workflow: WorkflowModel