import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

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

prompt = f"""
    What is typical weather in Wroclaw in September ?
    """
    
# Call the LLM
messages = [HumanMessage(content=prompt)]
response = model.invoke(messages)
print(response.content)
