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



## Project Structure

trendly-agent/
│
├── app/
│   ├── controllers/
│   ├── routes/
│   ├── services/
│   ├── state/
│   └── tools/
│
├── data/
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│
├── main.py
├── requirements.txt
├── README.md
├── PROMPTS.md
├── SOLUTION.md
└── .env.example


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


