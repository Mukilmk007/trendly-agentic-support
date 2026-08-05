# Solution Note

## Overview

Trendly AI is an agentic customer support assistant built using a ReAct (Reason + Act) architecture. The system separates reasoning, tool execution, and response generation, enabling the assistant to answer customer queries using grounded business data instead of relying solely on a language model.

The application is built with FastAPI, Google Gemini, and a modular tool-based architecture. It supports multi-turn conversations with conversation memory, policy retrieval, order lookup, return eligibility checks, and human escalation.

---

# Architecture

The system consists of five major components.

## 1. Frontend

A lightweight HTML/CSS/JavaScript interface allows users to interact with the assistant.

Responsibilities:

- Display chat history
- Quick action buttons
- Typing indicator
- Reset conversation

---

## 2. ReAct Controller

The ReAct controller orchestrates the complete workflow.

Responsibilities:

- Maintain conversation state
- Invoke the planner
- Execute tools
- Update memory
- Generate the final response

---

## 3. Planner

The planner uses Google Gemini to determine:

- User intent
- Required business tools
- Tool arguments

The planner never generates customer-facing responses.

Instead, it outputs structured JSON describing which actions should be executed.

---

## 4. Tool Layer

Business logic is encapsulated inside independent tools.

Current tools include:

- Order Lookup
- Policy Retrieval
- Return Eligibility
- Human Escalation

This modular design makes it easy to add new tools without changing the planner.

---

## 5. Response Generator

After tool execution, the response model produces a concise customer-facing reply using:

- Tool outputs
- Conversation state
- Retrieved policies
- Conversation history

---

# ReAct Flow

User Query
     │
     ▼
 Reason (Planner)
     │
     ▼
 Select Tool(s)
     │
     ▼
 Execute Tool(s)
     │
     ▼
 Update Memory
     │
     ▼
 Generate Response
     │
     ▼
 Customer

# Key Trade-offs

## 1. ReAct vs Single Prompt

I chose a ReAct workflow instead of a single LLM prompt.

Advantages:

- Better reasoning
- Easier debugging
- Lower hallucination risk
- Modular architecture

Trade-off:

- Two LLM calls increase latency compared to a single prompt.

---

## 2. JSON Files vs Database

Order data is stored in JSON files.

Advantages:

- Simple
- Easy to review
- No external database setup

Trade-off:

- Not suitable for production-scale datasets.

---

## 3. Conversation Memory

The system stores the current order and retrieved policies.

Advantages:

- Natural follow-up conversations
- Fewer repeated tool calls

Trade-off:

- Memory is reset when the conversation is cleared.

---

## 4. Rule-based Business Logic

Return eligibility is implemented through deterministic business rules.

Advantages:

- Predictable behavior
- Easy testing
- Consistent decisions

Trade-off:

- Policy updates require code or document changes.

---

# Known Limitations

Although functional, this implementation has several limitations.

- Uses JSON instead of a production database.
- Maintains conversation state in memory rather than persistent storage.
- Supports a single active conversation instance.
- Uses simulated order and policy data.
- No authentication or user accounts.
- No real shipping carrier integration.
- Responses are generated after the complete workflow rather than streamed.

---

# Discovery Questions for Trendly's Operations Team

Before building a production version, I would clarify the following:

### 1. Customer Authentication

How are customers identified? Should users authenticate before accessing order information?

---

### 2. Order Management System

Where does order data originate?

Would the assistant integrate with an ERP, OMS, or another backend service?

---

### 3. Return Policy Variations

Do return policies differ by:

- Product category
- Region
- Promotional campaigns
- Loyalty status

---

### 4. Human Escalation Workflow

How should escalations be handled?

Should the assistant create support tickets, transfer chats to live agents, or integrate with existing CRM software?

---

### 5. Performance Requirements

What are the expected response-time targets, daily traffic, and availability requirements for the production system?

---

# Conclusion

This project demonstrates how an agentic AI assistant can combine LLM reasoning with deterministic business tools to provide reliable, grounded, and context-aware customer support. The modular architecture makes the system easy to extend while minimizing hallucinations through tool-first reasoning and conversation memory.