# First-Session AI Personalization Engine

A hands-on demo that simulates how an AI-powered e-commerce homepage adapts during the first session.

## What it does
- Starts with zero user history
- Learns from the first 1–2 interactions
- Reconfigures the homepage dynamically
- Uses an LLM to explain personalization decisions
- Logs session behavior
- Scores personalization quality with a simple eval layer

## Why it matters
This project explores:
- cold start personalization
- grounding
- evals
- observability
- AI reasoning under uncertainty

## What I learned building it
- Personalization is weak when the system has no context
- After 1–2 clicks, the homepage should stop being generic
- Evaluation is as important as generation
- Observability helps explain why the UI changed
- AI should explain and critique decisions, not blindly make them

## Run it

```bash
pip install -r requirements.txt
python batch_eval.py
streamlit run app.py

