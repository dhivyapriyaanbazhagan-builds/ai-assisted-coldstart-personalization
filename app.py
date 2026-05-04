import json
import streamlit as st

from engine import build_homepage
from evaluator import evaluate_homepage
from ai_reasoner import explain_personalization
from logger import log_snapshot, load_logs

st.set_page_config(
 page_title="First-Session AI Personalization Engine",
 page_icon="🧠",
 layout="wide"
)

if "events" not in st.session_state:
 st.session_state.events = []

def add_event(event_type: str, item: str):
 st.session_state.events.append({"type": event_type, "item": item})

st.title("First-Session AI Personalization Engine")
st.caption("A homepage that adapts after 1–2 clicks and explains why.")

changed = False

with st.sidebar:
 st.header("Simulate user actions")

 if st.button("View running shoes"):
  add_event("view", "running shoes")
  changed = True

 if st.button("Search gift"):
  add_event("search", "gift")
  changed = True

 if st.button("View premium watch"):
  add_event("view", "premium watch")
  changed = True

 if st.button("Click sale banner"):
  add_event("click", "sale banner")
  changed = True

 if st.button("View kids backpack"):
  add_event("view", "kids backpack")
  changed = True

 if st.button("Reset session"):
  st.session_state.events = []
  changed = True

state = build_homepage(st.session_state.events)
evaluation = evaluate_homepage(state, [])

ai_analysis = ""
try:
 ai_analysis = explain_personalization(
 st.session_state.events,
 [m["id"] for m in state["modules"]]
 )
except Exception as e:
 ai_analysis = f"AI explanation unavailable: {e}"

if changed:
 log_snapshot({
 "events": st.session_state.events,
 "stage": state["stage"],
 "modules": [m["id"] for m in state["modules"]],
 "confidence": state["confidence"],
 "assumption_risk": state["assumption_risk"],
 "evaluation": evaluation,
 "ai_analysis": ai_analysis
 })

col1, col2, col3, col4 = st.columns(4)
col1.metric("Session stage", state["stage"])
col2.metric("Confidence", state["confidence"])
col3.metric("Assumption risk", state["assumption_risk"])
col4.metric("Personalization score", evaluation["personalization_score"])

st.divider()

left, right = st.columns([2, 1])

with left:
 st.subheader("Homepage modules")
 for module in state["modules"]:
  st.markdown(f"### {module['icon']} {module['title']}")
  st.write(module["description"])
  st.caption(module["reason"])
  st.divider()

with right:
 st.subheader("What the engine sees")
 st.json(state["signals"])

 st.subheader("Next best action")
 st.write(state["next_best_action"])

 st.subheader("AI analysis")
 st.write(ai_analysis)

 st.subheader("Current session events")
 st.code(json.dumps(st.session_state.events, indent=2), language="json")

 st.subheader("Eval notes")
 for note in evaluation["notes"]:
  st.write(f"- {note}")

st.divider()
st.subheader("Logged sessions")
logs = load_logs()
st.write(f"Total logs: {len(logs)}")
if logs:
 st.write("Most recent log:")
 st.json(logs[-1])