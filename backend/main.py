import json
import os
from pathlib import Path

from promptflow import load_flow

# Load configuration
with open(Path(__file__).parent / "config.json", "r") as f:
    config = json.load(f)
    flow_path = config["flow_path"]
    is_streaming = config["is_streaming"]

# Load the flow
if flow_path:
    flow = Path(flow_path)
else:
    flow = Path(__file__).parent / "flow"
if flow.is_dir():
    os.chdir(flow)
else:
    os.chdir(flow.parent)
invoker = load_flow(flow)
invoker.context.streaming = is_streaming

thumbs_up = True  # Define the variable "thumbs_up"
def handle_prompt(prompt: str, chat_history: list, thumbs_up: bool) -> str:    
    """Handle a prompt from the user and return the response."""
    data = {
            "query": prompt,
            "chat_history": chat_history,
            "thumbs_up": thumbs_up,  # Use the defined variable "thumbs_up"
        }
    result = invoker.invoke(data)
    if result.run_info.status.value == "Failed":
        raise Exception(result.run_info.error)
    response = result.output.get("reply")  # Adjust this based on your flow's output structure
    return response


if __name__ == "__main__":
    # Test the function
    prompt = "Hello, how are you?"
    chat_history = []  # Initialize an empty chat history for testing
    response = handle_prompt(prompt, chat_history, thumbs_up)    
    
    print(response)
