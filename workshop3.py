import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

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

# GMAIL_INITIALIZATION
# ---------------------

gmail_creds = None
# token.json stores the user's access and refresh tokens
if os.path.exists('token.json'):
    gmail_creds = Credentials.from_authorized_user_file('token.json', SCOPES)
else:
    # Run local server for OAuth if no token exists
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    gmail_creds = flow.run_console()

    # Save credentials for future runs
    with open('token.json', 'w') as token:
        token.write(gmail_creds.to_json())

# Call Gmail API
gmail_service = build('gmail', 'v1', credentials=gmail_creds)

# NODES INITIALIZATION
# ---------------------

class EmailState(TypedDict):
    presented: bool
    subject: str
    sender: str
    content: str
     
def read_email(state: EmailState):
    """
        Read UNREAD emails from gmail, saves data to EmailState
    """

    # Fetch unread messages
    results = gmail_service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No new emails found.")
        return {
            "presented": False,
        }
    
    print(f"messages {messages}")

    for msg in messages:
        msg_data = gmail_service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
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
        }
    
    return {}

def classify_email(state: EmailState):
    print("classifying email")
    print(f"email state", state)
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
