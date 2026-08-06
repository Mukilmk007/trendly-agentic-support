# Prompt Engineering

## Overview

Trendly AI uses Google Gemini for two distinct tasks:

1. Planning (Reasoning)
2. Response Generation

Separating these responsibilities improves reliability by allowing the model to first decide *what to do* before generating a customer facing response.

---

# Prompt 1 – Planner

## Objective

Determine:

- User intent
- Whether a business tool is required
- Which tool(s) to execute
- Tool arguments

The planner never generates customer facing text.

Instead, it produces structured JSON that drives the ReAct workflow.

### Input

The planner receives:

- Conversation history
- Current order (if available)
- Current policy (if available)
- Latest user message

### Output

Example:

```json
{
  "intent": "order_status",
  "thought": "Need order information before responding.",
  "actions": [
    {
      "tool": "lookup_order",
      "arguments": {
        "order_id": "TR-4521"
      }
    }
  ]
}
```

---

# Prompt 2 – Response Generator

## Objective

Generate a natural customer support response using only grounded information.

The response model receives:

- Conversation history
- Current order
- Current policy
- Tool observations
- Latest user message

Unlike the planner, the response generator never decides which tools to execute.

Its responsibility is only to explain the retrieved information in a friendly and concise manner.

---

# Prompt Iterations

Several improvements were made during development.

## Iteration 1

The response prompt relied only on the latest tool outputs.

Example instruction:

> Use ONLY the tool results above.

### Problem

Follow up questions failed.

Example:

User:

```
Where is my order TR-4530?
```

User:

```
What was the payment method?
```

Because no tool executed during the second message, the model replied:

> I don't know.

even though the payment method already existed in conversation memory.

---

## Iteration 2

The response prompt was updated to include:

- Current Order
- Current Policy
- Conversation History

The instructions explicitly tell the model to answer from the conversation state whenever the required information already exists.

This eliminated unnecessary tool calls while enabling accurate multi turn conversations.

---

## Iteration 3

The planner prompt was refined to reuse existing conversation state.

Instead of repeatedly calling the order lookup tool, the planner now checks whether the requested information already exists.

Benefits:

- Lower latency
- Fewer API/tool calls
- Better conversational continuity

---

# Design Decisions

Several prompt engineering principles were followed.

## Separation of Planning and Responding

Reasoning and response generation use separate prompts.

This reduces hallucinations and keeps business logic deterministic.

---

## Grounded Responses

The response model only answers using:

- Current Order
- Current Policy
- Tool Results

It does not invent facts.

---

## Conversation Memory

Prompt context includes conversation state so that follow-up questions can be answered naturally without repeating tool calls.

---

## Concise Responses

The assistant is instructed to produce short, friendly customer support replies instead of long explanations.

---

# Prompting Strategy

The project follows a ReAct style workflow:

User Message

↓

Planner Prompt

↓

Tool Execution

↓

Response Prompt

↓

Customer Response

This separation makes the system easier to maintain, extend, and debug compared to using a single prompt for both reasoning and answering.