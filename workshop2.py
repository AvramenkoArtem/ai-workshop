import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

# OPENAI_INITIALIZATION
# ---------------------

open_ai_key=""

# Fallback to environment variable if not set
if not open_ai_key:
    open_ai_key = os.getenv("OPENAI_API_KEY")

# Raise an error if the key is still not found
if not open_ai_key:
        raise ValueError("OpenAI API key is not provided and not found in environment variables.")

# Initialize our LLM
model = ChatOpenAI(
    temperature=0,
    openai_api_key=open_ai_key,
    )

# NODES INITIALIZATION
# ---------------------

class EmailState(TypedDict):
    pass

def read_email(state: EmailState):
    print("Reading the email")
    return {}

def classify_email(state: EmailState):
    print("classifying email")
    return {}


# GRAPH WORKFLOW INITIALIZATION
# ---------------------

# Create the graph
email_graph = StateGraph(EmailState)

# Add nodes
email_graph.add_node("read_email", read_email)
email_graph.add_node("classify_email", classify_email)

# Start the edges
email_graph.add_edge(START, "read_email")
# Add edges - defining the flow
email_graph.add_edge("read_email", "classify_email")

# Add the final edges
email_graph.add_edge("classify_email", END)

# Compile the graph
compiled_graph = email_graph.compile()

compiled_graph.invoke({})

with open("graph.png", "wb") as f:
    f.write(compiled_graph.get_graph().draw_mermaid_png())