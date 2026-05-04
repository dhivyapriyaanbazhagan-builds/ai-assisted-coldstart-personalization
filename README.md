# 🧠 First-Session AI Personalization Engine

A hands-on project exploring how systems **personalize under cold start conditions** — when there is little or no user data.

This project simulates how a system:

* starts with zero context
* adapts after the first few interactions
* explains its decisions using AI
* evaluates personalization quality
* logs behavior for observability

---

## 🎯 Problem

Personalization works well with data.

But in the **first session**, systems have:

* no history
* no preferences
* no behavioral signals

> How do you personalize when you know nothing about the user?

---

## 💡 Approach

Instead of relying purely on AI, this system combines:

* **Deterministic decision logic** (for reliability)
* **LLM-based reasoning** (for explainability)
* **Evaluation layer** (for quality measurement)
* **Observability layer** (for debugging & insights)

---

## 🏗️ Architecture

```
User Interaction (Clicks / Events)
 │
 ▼
 ┌──────────────────────┐
 │ Decision Engine │
 │ (Rule-based logic) │
 └─────────┬────────────┘
 │
 ▼
 ┌──────────────────────┐
 │ AI Reasoning Layer │
 │ (LLM explanation) │
 └─────────┬────────────┘
 │
 ▼
 ┌──────────────────────┐
 │ Evaluation Layer │
 │ (Quality scoring) │
 └─────────┬────────────┘
 │
 ▼
 ┌──────────────────────┐
 │ Observability Layer │
 │ (Logs & analysis) │
 └──────────────────────┘
```

---

## 🧩 Project Structure

```
first-session-ai-personalization/
│
├── app.py # Streamlit UI
├── batch_eval.py # Offline evaluation runner
├── requirements.txt
├── README.md
│
├── data/
│ └── scenarios.json # Test scenarios
│
├── agent/
│ ├── engine.py # Personalization logic
│ ├── ai_reasoner.py # LLM explanation layer
│ ├── evaluator.py # Scoring system
│ └── logger.py # Logging / observability
│
└── logs.jsonl # Generated logs
```

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Run offline evaluation

```bash
python batch_eval.py
```

This generates:

* `results.csv`
* evaluation summary

---

### 3. Run the app

```bash
python -m streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## 🔍 What to Try

In the UI:

* Start with no interactions (cold start)
* Click:

 * "View running shoes"
 * "Search gift"
 * "View premium item"
* Observe:

 * Homepage changes
 * AI explanation
 * Evaluation scores
 * Logged behavior

---

## 🧠 Key Learnings

* Cold start is not a data problem — it’s a **decision problem under uncertainty**
* Systems tend to:

 * stay too generic
 * or over-assume too early
* Confidence often grows faster than actual certainty
* Evaluation and observability are critical in AI systems

---

## ⚖️ Limitations

* Rule-based decision engine (not learned model)
* Simple evaluation heuristics
* No real user data (simulated scenarios)

---

## 🔮 Future Improvements

* Add **LLM-as-a-Judge** for evaluation
* Compare multiple models (Gemma, Qwen, etc.)
* Add visualization dashboards
* Introduce adaptive learning instead of static rules

---

## 🔧 Tech Stack

* **Python** — core logic
* **Streamlit** — UI
* **Ollama (local LLM)** — reasoning layer
* **JSON / CSV** — data + logs
* **ChatGPT** was used to code & iterate
