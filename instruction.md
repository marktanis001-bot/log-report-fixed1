There is an Apache-style access log at `/app/access.log`. Analyze the traffic and
write a JSON summary report to `/app/report.json`.

The report must include:

- `total_requests`: total number of non-empty log lines processed.
- `unique_ips`: number of distinct client IP addresses.
- `client_ips`: sorted list of distinct client IP addresses.
- `client_request_counts`: object mapping each client IP address to its request count.
- `path_counts`: object mapping each requested path to its request count.
- `top_path`: the path with the highest number of requests.

Only count well-formed request lines. Save the final JSON file at `/app/report.json`.
