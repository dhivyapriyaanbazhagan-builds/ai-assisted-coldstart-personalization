import json
import pandas as pd

from engine import build_homepage
from evaluator import evaluate_homepage

def run_batch_eval():
 with open("data/scenarios.json", "r", encoding="utf-8") as f:
  scenarios = json.load(f)

 rows = []

 for scenario in scenarios:
  engine_output = build_homepage(scenario["events"])
  eval_output = evaluate_homepage(engine_output, scenario.get("expected_modules", []))

 rows.append({
  "scenario_id": scenario["id"],
  "scenario_name": scenario["name"],
  "stage": engine_output["stage"],
  "confidence": engine_output["confidence"],
  "assumption_risk": engine_output["assumption_risk"],
  "signals": json.dumps(engine_output["signals"]),
  "modules": json.dumps([m["id"] for m in engine_output["modules"]]),
  "personalization_score": eval_output["personalization_score"],
  "grounding_score": eval_output["grounding_score"],
  "genericity_flag": eval_output["genericity_flag"],
  "eval_assumption_risk": eval_output["assumption_risk"],
  "notes": " | ".join(eval_output["notes"])
 })

 df = pd.DataFrame(rows)
 df.to_csv("results.csv", index=False)

 print("\n=== Batch Evaluation Complete ===")
 print(df[[
  "scenario_name",
  "stage",
  "personalization_score",
  "grounding_score",
  "genericity_flag",
  "eval_assumption_risk"
 ]].to_string(index=False))

 print("\nSaved to results.csv")

if __name__ == "__main__":
 run_batch_eval()