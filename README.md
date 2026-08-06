# Trendly AI – Agentic Customer Support Assistant

## Overview

Trendly AI is an intelligent customer support assistant built for Trendly, a direct-to-consumer fashion retailer. The assistant leverages an Agentic ReAct workflow to reason about customer requests, invoke specialized tools when required, and generate grounded, context-aware responses.

Unlike a traditional chatbot that relies solely on a language model, Trendly AI separates reasoning from tool execution, allowing it to retrieve factual order information, consult company policies, evaluate return eligibility, and escalate conversations when appropriate.

The project demonstrates how Large Language Models can be combined with deterministic business logic to create reliable customer support experiences.

## Features

* Multi-turn conversations with contextual memory
* ReAct-style planning and reasoning
* Order lookup using structured data
* Return policy retrieval
* Return eligibility verification
* Human support escalation
* Grounded responses based on tool outputs
* Responsive chat interface
* WhatsApp-style typing indicator
* Reset conversation functionality
* FastAPI REST backend
* Modern HTML/CSS/JavaScript frontend

## Demo

Once the application is running:

### Frontend

http://127.0.0.1:8000

### Health Check

GET /health

### Chat Endpoint

POST /chat

### Reset Conversation

POST /reset




## Technology Stack

### Backend

* Python
* FastAPI

### AI

* Google Gemini

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript

### Data

* JSON
* Markdown policy documents




## Agent Workflow

Every customer request follows the same pipeline:

1. User Message

The customer submits a query through the chat interface.

2. Planner

Gemini determines:

* User intent
* Required tools
* Tool parameters

3. Tool Execution

The controller executes only the required tools.

Examples include:

* Lookup Order
* Retrieve Policy
* Check Eligibility
* Escalate to Human

4. Response Generation

Gemini generates the final customer-facing response using:

* Conversation history
* Tool outputs
* Current conversation state

5. Memory Update

The assistant stores:

* Conversation history
* Current order
* Retrieved policies
* Tool observations

This enables accurate multi-turn conversations.



## Supported Customer Queries

The assistant supports scenarios such as:

* Where is my order?
* Track order by ID
* Can I return my order?
* Return eligibility
* Refund timeline
* Return policy
* Exchange policy
* Talk to a human


## Quick Start

### Prerequisites

- Python 3.11+
- A Google Gemini API key

### Clone the repository

```bash
git clone https://github.com/Mukilmk007/trendly-agentic-support
cd trendly-agentic-support
```

### Create and activate a virtual environment

**macOS/Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=your_model_name
```

### Start the application

```bash
uvicorn main:app --reload
```

### Open the application

Frontend: `http://127.0.0.1:8000`

Base URL: `http://127.0.0.1:8000`




## Example Conversation

#### User:
Where is my order TR-4521?

#### Assistant:
Your order TR-4521 is currently in transit with BlueDart and is expected to arrive on July 31, 2026.

#### User:
Can I return it?

#### Assistant:
Since the order has not yet been delivered, it is not currently eligible for return.




## AI Usage

Google Gemini is used for two primary responsibilities:

### Planning

The planner analyzes customer intent and decides which business tools should be executed.

### Response Generation

The response model produces natural language answers using only grounded information from executed tools and conversation state.

The language model never directly accesses business data; all factual information is retrieved through dedicated tools.



## Design Principles

* Separation of reasoning and execution
* Grounded AI responses
* Minimal hallucination risk
* Modular tool architecture
* Conversation-aware interactions
* Easy extensibility


## Guardrails

To improve reliability and reduce incorrect responses, the assistant implements the following guardrails:

* Tool-First Responses: The assistant retrieves factual information (such as order details and company policies) through dedicated tools instead of relying on the language model’s memory.
* Conversation Memory: The current order and retrieved policy are stored in conversation state, allowing follow-up questions (for example, “What was the payment method?”) to be answered without performing unnecessary lookups.
* Policy-Based Decisions: Return, exchange, and refund responses are generated only from the official Trendly policy document, ensuring consistent and accurate answers.
* No Hallucinations: If the requested information is unavailable in the current conversation state or tool results, the assistant does not fabricate an answer and instead informs the user or requests additional information.
* Input Normalization: Order IDs are normalized before lookup (for example, tr-4530, Tr-4530, and TR-4530 are all treated as TR-4530) to improve user experience.
* Human Escalation: Requests that require human assistance or cannot be confidently resolved are escalated using the dedicated escalation tool, along with a summary of the conversation context.
* Minimal Tool Usage: The planner avoids redundant tool calls by reusing information already stored in the conversation state, improving both response time and efficiency.


## Troubleshooting

### API key errors

Ensure the .env file exists and contains a valid Gemini API key.

### Module not found

#### Install all dependencies:

pip install -r requirements.txt


## Frontend not loading

Ensure the FastAPI server is running and that the static directory is present.

## Prerequisites

- Python 3.11+
- Google Gemini API Key

### Live URL

```

https://trendly-agentic-support-qa52.onrender.com/

```