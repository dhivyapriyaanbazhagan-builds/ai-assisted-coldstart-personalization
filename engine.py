from typing import Any, Dict, List

MODULE_LIBRARY = {
 "hero_onboarding": {
 "title": "Tell us what you like",
 "icon": "🧭",
 "description": "Pick a few interests so the homepage can adapt faster."
 },
 "trending_products": {
 "title": "Trending now",
 "icon": "🔥",
 "description": "Popular products across the platform."
 },
 "popular_categories": {
 "title": "Popular categories",
 "icon": "🛍️",
 "description": "A safe fallback when there is little user history."
 },
 "recently_viewed": {
 "title": "Recently viewed",
 "icon": "🕒",
 "description": "Keep the session anchored to the user’s recent actions."
 },
 "sports_essentials": {
 "title": "Sports essentials",
 "icon": "🏃",
 "description": "Recommended because the session showed fitness intent."
 },
 "running_gear": {
 "title": "Running gear",
 "icon": "👟",
 "description": "Matched to running-related browsing behavior."
 },
 "premium_picks": {
 "title": "Premium picks",
 "icon": "💎",
 "description": "Shown after a premium or high-value signal."
 },
 "luxury_accessories": {
 "title": "Luxury accessories",
 "icon": "⌚",
 "description": "Higher-end items aligned with premium browsing."
 },
 "gift_guide": {
 "title": "Gift guide",
 "icon": "🎁",
 "description": "Useful when the user shows gifting intent."
 },
 "gift_bundles": {
 "title": "Gift bundles",
 "icon": "📦",
 "description": "Curated bundles for a gift-focused session."
 },
 "deals": {
 "title": "Deals",
 "icon": "🏷️",
 "description": "Activated by price-sensitive or sale-seeking behavior."
 },
 "under_budget": {
 "title": "Under budget",
 "icon": "💸",
 "description": "Budget-friendly picks for a value-seeking session."
 },
 "kids_favorites": {
 "title": "Kids favorites",
 "icon": "🧒",
 "description": "Surface family-friendly items when the session suggests it."
 },
 "family_essentials": {
 "title": "Family essentials",
 "icon": "🏡",
 "description": "Practical items aligned with family shopping intent."
 }
}

KEYWORDS = {
 "sports": {"running", "shoe", "shoes", "gym", "fitness", "sports"},
 "premium": {"premium", "luxury", "watch", "headphones", "designer"},
 "gift": {"gift", "present", "birthday", "anniversary"},
 "deal": {"sale", "discount", "offer", "cheap", "budget", "under"},
 "tech": {"laptop", "phone", "smartwatch", "headphones", "tablet"},
 "kids": {"kids", "child", "children", "family", "school"}
}

def _flatten_event(event: Dict[str, Any]) -> str:
 return " ".join(str(v) for v in event.values()).lower()

def dedupe(seq: List[str]) -> List[str]:
 seen = set()
 out = []
 for item in seq:
  if item not in seen:
   out.append(item)
   seen.add(item)
 return out

def infer_signals(events: List[Dict[str, Any]]) -> Dict[str, bool]:
 signals = {
  "sports": False,
  "premium": False,
  "gift": False,
  "deal": False,
  "tech": False,
  "kids": False
 }

 for event in events:
  text = _flatten_event(event)

  if any(k in text for k in KEYWORDS["sports"]):
   signals["sports"] = True
  if any(k in text for k in KEYWORDS["premium"]):
   signals["premium"] = True
  if any(k in text for k in KEYWORDS["gift"]):
   signals["gift"] = True
  if any(k in text for k in KEYWORDS["deal"]):
   signals["deal"] = True
  if any(k in text for k in KEYWORDS["tech"]):
   signals["tech"] = True
  if any(k in text for k in KEYWORDS["kids"]):
   signals["kids"] = True

 return signals
def choose_module_ids(events: List[Dict[str, Any]], signals: Dict[str, bool]) -> List[str]:
 if not events:
  return ["hero_onboarding", "trending_products", "popular_categories"]

 module_ids: List[str] = []

 if signals["gift"]:
  module_ids += ["gift_guide", "gift_bundles"]

 if signals["sports"]:
  module_ids += ["sports_essentials", "running_gear"]

 if signals["premium"]:
  module_ids += ["premium_picks", "luxury_accessories"]

 if signals["deal"]:
  module_ids += ["deals", "under_budget"]

 if signals["tech"]:
  module_ids += ["trending_products"]

 if signals["kids"]:
  module_ids += ["kids_favorites", "family_essentials"]

 if len(events) >= 2:
  module_ids.insert(0, "recently_viewed")
 else:
  module_ids.append("recently_viewed")

 if not module_ids:
  module_ids = ["trending_products", "popular_categories"]

 return dedupe(module_ids)

def module_reason(module_id: str, events: List[Dict[str, Any]], signals: Dict[str, bool]) -> str:
 if module_id == "hero_onboarding":
  return "No history yet, so the homepage starts with lightweight preference capture."
 if module_id == "trending_products":
  return "Used as a safe fallback when the system has very little context."
 if module_id == "popular_categories":
  return "Shows broad categories until the system learns more."
 if module_id == "recently_viewed":
  return "Keeps the homepage connected to the user’s latest action."
 if module_id == "sports_essentials":
  return "The session shows fitness intent, so this section becomes more relevant."
 if module_id == "running_gear":
  return "Running-related browsing was detected in the first few interactions."
 if module_id == "premium_picks":
  return "A premium browsing signal was detected early in the session."
 if module_id == "luxury_accessories":
  return "This section follows a high-value or premium interaction."
 if module_id == "gift_guide":
  return "The user appears to be browsing with gifting intent."
 if module_id == "gift_bundles":
  return "Bundled gifts are useful when the session hints at a present-buying task."
 if module_id == "deals":
  return "The user appears price-sensitive or sale-driven."
 if module_id == "under_budget":
  return "Budget-friendly picks are useful after a discount-oriented signal."
 if module_id == "kids_favorites":
  return "The session hints at family or kids-related shopping."
 if module_id == "family_essentials":
  return "Practical family products are surfaced after family-related context."
 return "Matched to the observed session behavior."

def build_homepage(events: List[Dict[str, Any]]) -> Dict[str, Any]:
 signals = infer_signals(events)
 module_ids = choose_module_ids(events, signals)

 if len(events) == 0:
  stage = "cold_start"
  confidence = 0.10
  assumption_risk = "low"
  next_best_action = "Ask the user for 2–3 interests or wait for the first click."
 elif len(events) == 1:
  stage = "learning"
  confidence = 0.45
  assumption_risk = "medium"
  next_best_action = "Wait for one more interaction before narrowing too aggressively."
 else:
  stage = "personalized"
  confidence = 0.78
  assumption_risk = "low"
  next_best_action = "Use recent behavior plus the strongest observed signal."

 if any(signals.values()):
  confidence = min(confidence + 0.08, 0.95)

 modules = []
 for module_id in module_ids:
  meta = MODULE_LIBRARY[module_id]
  modules.append({
   "id": module_id,
   "title": meta["title"],
   "icon": meta["icon"],
   "description": meta["description"],
   "reason": module_reason(module_id, events, signals)
  })

 return {
  "stage": stage,
  "confidence": round(confidence, 2),
  "assumption_risk": assumption_risk,
  "signals": signals,
  "modules": modules,
  "next_best_action": next_best_action,
  "events": events
 }