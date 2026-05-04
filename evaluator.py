from typing import Any, Dict, List

GENERIC_MODULES = {"hero_onboarding", "trending_products", "popular_categories"}

SPORTS_MODULES = {"sports_essentials", "running_gear"}
PREMIUM_MODULES = {"premium_picks", "luxury_accessories"}
GIFT_MODULES = {"gift_guide", "gift_bundles"}
DEAL_MODULES = {"deals", "under_budget"}
KIDS_MODULES = {"kids_favorites", "family_essentials"}

def _ids(modules: List[Dict[str, Any]]) -> List[str]:
 return [m["id"] for m in modules]

def evaluate_homepage(engine_output: Dict[str, Any], expected_modules: List[str] | None = None) -> Dict[str, Any]:
 expected_modules = expected_modules or []
 actual_modules = _ids(engine_output["modules"])
 signals = engine_output["signals"]

 overlap = len(set(actual_modules) & set(expected_modules))
 expected_count = max(len(expected_modules), 1)
 overlap_ratio = overlap / expected_count

 if overlap_ratio >= 0.75:
  personalization_score = 5
 elif overlap_ratio >= 0.50:
  personalization_score = 4
 elif overlap_ratio >= 0.25:
  personalization_score = 3
 elif actual_modules:
  personalization_score = 2
 else:
  personalization_score = 1

 generic_count = sum(1 for m in actual_modules if m in GENERIC_MODULES)
 genericity_flag = engine_output["stage"] != "cold_start" and generic_count >= 2

 matched_signals = 0
 total_signals = sum(1 for v in signals.values() if v)

 if signals.get("sports") and any(m in SPORTS_MODULES for m in actual_modules):
  matched_signals += 1
 if signals.get("premium") and any(m in PREMIUM_MODULES for m in actual_modules):
  matched_signals += 1
 if signals.get("gift") and any(m in GIFT_MODULES for m in actual_modules):
  matched_signals += 1
 if signals.get("deal") and any(m in DEAL_MODULES for m in actual_modules):
  matched_signals += 1
 if signals.get("kids") and any(m in KIDS_MODULES for m in actual_modules):
  matched_signals += 1

 if total_signals == 0 and engine_output["stage"] == "cold_start":
  grounding_score = 5
 elif total_signals > 0 and matched_signals == total_signals:
  grounding_score = 5
 elif matched_signals > 0:
  grounding_score = 3
 else:
  grounding_score = 1

 if engine_output["stage"] == "learning" and len(actual_modules) > 1 and matched_signals == 0:
  assumption_risk = "high"
 elif engine_output["stage"] == "personalized" and matched_signals > 0:
  assumption_risk = "low"
 else:
  assumption_risk = "medium"

 notes = []
 if genericity_flag:
  notes.append("Homepage stayed too generic after signals appeared.")
 if total_signals > 0 and matched_signals == 0:
  notes.append("Chosen modules did not reflect the observed signals.")
 if assumption_risk == "high":
  notes.append("The system jumped to a specific segment with weak evidence.")
 if not notes:
  notes.append("Homepage adaptation looks reasonable for the observed session.")

 return {
 "personalization_score": personalization_score,
 "grounding_score": grounding_score,
 "genericity_flag": genericity_flag,
 "assumption_risk": assumption_risk,
 "notes": notes
 }