**Workshop Goal**

Building an Email-Sorting Agent for Gmail Using Agentic Architectures
This workshop is designed to empower developers with practical, up-to-date knowledge of agentic architectures powered by Large Language Models (LLMs). Participants will explore the theory and practice of AI agents by building a real-world email-sorting assistant integrated with Gmail.

Primary Objectives:
Demystify Agentic Architectures with LLMs:
Deliver concise, accessible explanations and code examples that make the foundational concepts of agentic systems and AI-powered automation clear to both beginners and experienced developers.

Hands-On Experience with a Real-World Use Case:
Guide attendees through the development of an intelligent email sorter that classifies and routes Gmail messages based on their content, using real email data (with appropriate permissions/sandboxing).

Familiarization with Modern LLM Tooling:
Provide structured exercises that introduce core tools such as:

1. LangGraph – for building multi-step, stateful workflows.
2. LangChain – for orchestration, memory management, and retrieval.
3. OpenAPI SDK / Gmail API – for accessing and interacting with email content in a real-world context.

Reproducible, Minimal-Friction Development Environment:
Ensure the workshop environment is simple to set up and run, with pre-built templates, minimal dependencies, and step-by-step instructions (e.g., Google Colab or Docker-based starter kits).

**Prequities**

1. Starter Code Repository:

Provide participants with a well-structured starter repository containing modular and extendable components.

- Focus on minimizing boilerplate so participants can concentrate on logic and experimentation.

- Each step should be reproducible with minimal effort, ideally runnable with a single command or in hosted environments like Google Colab or Replit.

2. Pre-Configured Google Accounts for Gmail API Access:

- Prepare a set of 10+ sandboxed Google accounts, pre-authorized with Gmail API access, for participants who may not have time or ability to configure their own accounts.

- Share credentials (login, password, OAuth client credentials/API keys) in a secure, time-limited manner during the workshop.

- Include instructions on how to connect these accounts with the starter code securely.

3. Test Scenarios & Validation Suite:

- Create a suite of predefined test scenarios (e.g., mock emails: invoices, support tickets, spam, newsletters) to help participants validate their email classification and routing workflows.

- Include automated test scripts or test harnesses where possible to ensure functionality is working as expected.

4. OpenAI API Access:

- Secure an OpenAI account with at least $50 credit, or equivalent shared access, to ensure all participants can make API requests during the workshop without interruptions.

- Provide a shared API key or assist each participant in generating and securely managing their own API keys.

**Format**

The workshop is divided into two key parts:

- Theory Presentation – Brief, high-level walkthrough using slides.
- Hands-On Development – Step-by-step practical implementation using prepared templates and modular code.

*** Theory Presentation ***

- Delivered using a short PowerPoint or slide deck (5–10 slides).
- Visualizations of core tools and concepts, including:
- Agentic architecture overview
- LangGraph workflows
- Role of LLMs and APIs
- Integration flow with Gmail

Purpose: Equip participants with enough conceptual grounding to understand the upcoming implementation stages.

*** Hands-On Development ***


1. Initialize basic agent structure and establish requests/responses handling with OpenAPI
- Set up a basic agent structure.
- Handle request/response flows using OpenAI APIs via LangChain.
- Confirm that the agent can make successful calls and receive structured responses.

2. Add First Node (Email Reading Logic) - Start
- Introduce the first node/tool for email reading.
- Visualize the basic agent structure using LangGraph's graph view.
- Discuss how tools and nodes relate to real-world agent workflows.

3. Gmail Integration
- Connect to the Gmail API using prepared or personal credentials.
- Add a tool/node to allow the agent to read incoming emails.
- Test that the agent can access and parse real or test emails correctly.

4. Add Decision Logic (Spam/Actionable Classification) - Graph level
- Expand the workflow with a decision tree for LangGraph.
- Visualize the updated LangGraph diagram to reflect new branching logic.

5. Implement Email Classification
- Enable the agent to classify email.
- Test that object of Email classified correctly with its metadata

6. Implement Spam Step
- Implement Spam node to put the spam email to spam folder
- Test and show Gmail that it moved to spam

7. Implement Response node with Email template for non spam email
- Enable agent to generate polite and professional email response based on pre-defined template
- Enable node to send email via gmail
- Test that output is correct and expected

8. Run Tests with Prepared Scenarios
- Use the prepared email templates to test how the agent classifies and reacts.
- Validate outputs and logic using known inputs (spam vs. non-spam cases).
- Allow time for debugging, improvements, and participant-led customizations.
