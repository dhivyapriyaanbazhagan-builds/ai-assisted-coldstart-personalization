import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

LOG_FILE = Path("logs.jsonl")

def log_snapshot(payload: Dict[str, Any]) -> None:
 row = {
 "timestamp": datetime.now(timezone.utc).isoformat(),
 **payload
 }
 with LOG_FILE.open("a", encoding="utf-8") as f:
  f.write(json.dumps(row, ensure_ascii=False) + "\n")

def load_logs() -> List[Dict[str, Any]]:
 if not LOG_FILE.exists():
  return []

 rows = []
 with LOG_FILE.open("r", encoding="utf-8") as f:
  for line in f:
   line = line.strip()
   if line:
    rows.append(json.loads(line))
 return rows