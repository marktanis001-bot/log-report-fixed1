import json
import re
from collections import Counter
from pathlib import Path

LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")
REQUEST_RE = re.compile(r'^(?P<ip>\S+)\s+\S+\s+\S+\s+\[[^\]]+\]\s+"(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+HTTP/[^"]+"\s+(?P<status>\d{3})\s+(?P<size>\S+)')

client_counts = Counter()
path_counts = Counter()
total_requests = 0

with LOG_PATH.open(encoding="utf-8") as log_file:
    for raw_line in log_file:
        line = raw_line.strip()
        if not line:
            continue
        match = REQUEST_RE.match(line)
        if not match:
            continue
        total_requests += 1
        client_counts[match.group("ip")] += 1
        path_counts[match.group("path")] += 1

report = {
    "total_requests": total_requests,
    "unique_ips": len(client_counts),
    "client_ips": sorted(client_counts),
    "client_request_counts": dict(sorted(client_counts.items())),
    "path_counts": dict(sorted(path_counts.items())),
    "top_path": path_counts.most_common(1)[0][0] if path_counts else None,
}

REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"wrote {REPORT_PATH}")
