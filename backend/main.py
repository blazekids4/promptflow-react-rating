import json
import os
from pathlib import Path

from promptflow import load_flow

# Load configuration
with open(Path(__file__).parent / "config1.json", "r") as f:
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
def handle_prompt(prompt: str, chat_history: list, thumbs_up: bool, context: str) -> str:
    """Handle a prompt from the user and return the response."""

    # Load the correct configuration based on the context
    if context == 'context1':
        with open(Path(__file__).parent / "config1.json", "r") as f:
            config = json.load(f)
    elif context == 'context2':
        with open(Path(__file__).parent / "config2.json", "r") as f:
            config = json.load(f)
    # ... add more contexts as needed

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

    data = {
        "query": prompt,
        "chat_history": chat_history,
        "thumbs_up": thumbs_up,
    }
    result = invoker.invoke(data)
    if result.run_info.status.value == "Failed":
        raise Exception(result.run_info.error)
    response = result.output.get("reply")  # Adjust this based on your flow's output structure
    return response