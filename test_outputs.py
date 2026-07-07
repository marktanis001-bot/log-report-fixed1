import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")
REQUEST_RE = re.compile(r'^(?P<ip>\S+)\s+\S+\s+\S+\s+\[[^\]]+\]\s+"(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+HTTP/[^"]+"\s+(?P<status>\d{3})\s+(?P<size>\S+)')


def expected_summary():
    client_counts = Counter()
    path_counts = Counter()
    total_requests = 0
    for raw_line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = REQUEST_RE.match(line)
        if not match:
            continue
        total_requests += 1
        client_counts[match.group("ip")] += 1
        path_counts[match.group("path")] += 1
    return {
        "total_requests": total_requests,
        "unique_ips": len(client_counts),
        "client_ips": sorted(client_counts),
        "client_request_counts": dict(sorted(client_counts.items())),
        "path_counts": dict(sorted(path_counts.items())),
        "top_path": path_counts.most_common(1)[0][0] if path_counts else None,
    }


def load_report():
    assert REPORT_PATH.exists(), "no report.json found"
    assert REPORT_PATH.stat().st_size > 0, "report.json is empty"
    try:
        return json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"report.json is not valid JSON: {exc}") from exc


def test_report_matches_access_log_summary():
    """The report contains the required traffic summary for the provided access log."""
    assert load_report() == expected_summary()


def test_report_uses_required_schema():
    """The report includes all required fields with appropriate JSON types."""
    report = load_report()
    assert set(report) == {
        "total_requests",
        "unique_ips",
        "client_ips",
        "client_request_counts",
        "path_counts",
        "top_path",
    }
    assert isinstance(report["total_requests"], int)
    assert isinstance(report["unique_ips"], int)
    assert isinstance(report["client_ips"], list)
    assert isinstance(report["client_request_counts"], dict)
    assert isinstance(report["path_counts"], dict)
    assert isinstance(report["top_path"], str)
