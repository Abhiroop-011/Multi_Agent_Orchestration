import os
import sys
from dotenv import load_dotenv
from src.engine import Orchestrator

# 1. Load environment variables (API Keys)
load_dotenv()

def main():
    # Check if API Key exists
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return

    # 2. Define the path to our YAML config
    config_path = "config/supervisor_workflow.yaml"
    
    # Allow user to specify a different file via command line
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    print(f"Loading configuration from: {config_path}")

    try:
        # 3. Initialize the Orchestrator
        orchestrator = Orchestrator(config_path)
        
        # 4. Get the starting task from the user
        user_task = input("\nEnter the starting task for the agents: ")
        
        # 5. Run the workflow
        orchestrator.run(user_task)
        
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    main()