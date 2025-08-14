import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

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
    presented: bool
    subject: str
    sender: str
    content: str
    is_spam: bool
    spam_reason: str
    email_category: str
    message_id: str

# --- Helper function to authenticate and get service ---
def get_gmail_service():
    """
        Returns initialized gmail service
    """
    creds = None
    # token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        # Run local server for OAuth if no token exists
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_console()

        # Save credentials for future runs
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Call Gmail API
    service = build('gmail', 'v1', credentials=creds)
    return service
     

def read_email(state: EmailState):
    """
        Reading UNREAD emails from gmail, saves data to EmailState
    """
    service = get_gmail_service()

    # Fetch unread messages
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No new emails found.")
        return {
            "presented": False,
        }
    
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])
        
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)")

        # Try to decode the message body
        parts = payload.get("parts", [])
        body = ""

        if parts:
            for part in parts:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data", "")
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break
        else:
            data = payload.get("body", {}).get("data", "")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

        return {
            "presented": True,
            "subject": subject,
            "sender": sender,
            "content": body,
            "message_id": msg['id'],
        }
    
    return {}

def should_process_email(state: EmailState) -> str:
    """Determine the next step based on presence of emails to process"""
    if state["presented"]:
        return "email_presented"
    else:
        return "no_new_emails"

def route_email(state: EmailState) -> str:
    """Determine the next step based on email type"""
    if state["is_spam"]:
        return "spam"
    else:
        return "legitimate"

def classify_email(state: EmailState):
    print("classifying email")
    prompt = f"""
You are an intelligent email assistant. Analyze the following email and determine:
1. Whether it is spam or not.
2. The reason it is spam (if applicable).
3. The email's category. Choose from: Work, Social, Promotions, Updates, Personal, Other.

Email details:
Subject: {state['subject']}
Sender: {state['sender']}
Content: {state['content']}

Respond in JSON format with the following keys:
- is_spam: true or false
- spam_reason: string
- email_category: string
    """

    response = model.invoke([
        HumanMessage(content=prompt)
    ])

    import json
    try:
        result = json.loads(response.content)
        state["is_spam"] = result.get("is_spam", False)
        state["spam_reason"] = result.get("spam_reason", "")
        state["email_category"] = result.get("email_category", "Other")
    except Exception as e:
        # Fallbacks in case of parsing error
        state["is_spam"] = False
        state["spam_reason"] = "Failed to classify due to model error"
        state["email_category"] = "Other"

    return state


def handle_spam(state: EmailState):
    """
    Moves an email to spam by modifying its labels.
    """

    print("handling spam")
    service = get_gmail_service()
    message_id = state["message_id"]

    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={
            "addLabelIds": ["SPAM"],
            "removeLabelIds": []  # Optional: you can remove INBOX if needed
        }
    ).execute()
    return {}

def handle_response(state: EmailState):
    print("handling response")
    print(f"state is {state}")
    return {}

def mark_as_read(state: EmailState):
    print("marking as read")
    return {}

# GRAPH WORKFLOW INITIALIZATION
# ---------------------

# Create the graph
email_graph = StateGraph(EmailState)

# Add nodes
email_graph.add_node("read_email", read_email)
email_graph.add_node("classify_email", classify_email)
email_graph.add_node("handle_spam", handle_spam)
email_graph.add_node("handle_response", handle_response)
email_graph.add_node("mark_as_read", mark_as_read)

# Start the edges
email_graph.add_edge(START, "read_email")
# Add edges - defining the flow
# Add conditional branching from read_email
email_graph.add_conditional_edges(
    "read_email",
    should_process_email,
    {
        "email_presented": "classify_email",
        "no_new_emails": END
    }
)

email_graph.add_edge("read_email", "classify_email")

# Add conditional branching from classify_email
email_graph.add_conditional_edges(
    "classify_email",
    route_email,
    {
        "spam": "handle_spam",
        "legitimate": "handle_response"
    }
)

email_graph.add_edge("handle_response", "mark_as_read")

# Add the final edges
email_graph.add_edge("read_email", END)
email_graph.add_edge("handle_spam", END)
email_graph.add_edge("mark_as_read", END)

# Compile the graph
compiled_graph = email_graph.compile()

compiled_graph.invoke({})
