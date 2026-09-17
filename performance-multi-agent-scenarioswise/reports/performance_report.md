# Performance Test Report

## 1. Executive Summary

- Test Type: STRESS  
- Test Name: Stress Performance Test - test.k6.io  
- Target URL: https://test.k6.io  
- Overall Result: PASS  
- Thresholds: Configured P95 (800 ms) and Error Rate (1%) were met during this test (P95 = 332.25 ms; Error Rate = 0.00%).

## 2. Test Configuration

| Parameter     | Value |
| ------------- | ----- |
| Test Name     | Stress Performance Test - test.k6.io |
| Test Type     | STRESS |
| Target URL    | https://test.k6.io |
| HTTP Method   | GET |
| Load Profile  | Staged ramp-up and ramp-down (see Stages) |
| Virtual Users | 0 |
| Duration      | Not Available |

Stages:

| Stage | Duration | Target VUs |
| ----- | -------- | ---------- |
| 1     | 1m       | 10         |
| 2     | 2m       | 25         |
| 3     | 2m       | 40         |
| 4     | 2m       | 60         |
| 5     | 1m       | 0          |

Test Scenarios:

- Gradual Load Increase: Gradually increase virtual users from 10 to 60 to identify system capacity and performance degradation point.  
- Peak Load Validation: Maintain 60 concurrent users to validate system behavior under stress conditions and identify breaking points.  
- Recovery Phase: Ramp down from peak load to 0 VUs to validate system recovery and stability after stress period.

## 3. Performance Thresholds

| Metric            | SLA  |
| ----------------- | ---- |
| P95 Response Time | 800 ms |
| Error Rate        | 1%    |

## 4. Test Results

| Metric                | Result            | Status / Notes |
| --------------------- | ----------------- | -------------- |
| Overall Status        | PASS              | PASS (as reported) |
| P95 Response Time     | 332.25 ms         | Met (332.25 ms ≤ 800 ms) |
| Maximum Response Time | 2.5 s             | Not Applicable (no max-response SLA configured) |
| Error Rate            | 0.00%             | Met (0.00% ≤ 1%) |
| Total Requests        | 20654             | Not Applicable |
| Throughput            | 43.013949/s       | Not Applicable |

## 5. Key Findings

- Observed p95 = 332.25 ms, below the configured 800 ms SLA (threshold PASSED).  
- Observed error rate = 0.00%, below the configured 1% SLA (threshold PASSED).  
- Observed total HTTP requests = 20,654 and overall throughput = 43.013949 requests/sec.  
- Observed avg latency = 176.42 ms, median = 258.7 ms, p90 = 305.84 ms, p95 = 332.25 ms.  
- Observed maximum response-time spike to 2.5 s (tail latency) during the run.  
- VUs observed: min=1, max=60 (vus_max=60); iterations=10327 (21.506975/s); checks_succeeded=100.00%.

These findings relate to the STRESS test focus: system maintained P95 and error-rate SLAs while load increased to the configured peak (60 VUs), but tail-latency spikes were observed.

## 6. Performance Risks

- Observed: max response time spike to 2.5 s — risk to user experience during tail latency despite p95 passing.  
- Observed: server-side metrics were not provided, limiting root-cause analysis of the 2.5 s spike.  
- The test covered the configured load progression up to 60 VUs only; behavior beyond this configured peak was not evaluated.

## 7. Possible Bottlenecks

### Observed Bottlenecks
No confirmed bottlenecks were identified from the available test evidence.

### Potential Bottlenecks
- Potential: intermittent backend processing or a slow dependency causing the observed 2.5 s latency spike (assumption; server-side metrics not provided).  
- Potential: network latency variability between the load generator and target contributing to tail-latency spikes (assumption).  
- Potential: resource contention at peak VUs (up to 60) — not verifiable without server-side metrics.

(Each item above is a potential explanation; none are confirmed by the supplied analysis.)

## 8. Recommendations

- Collect server-side metrics (CPU, memory, threads, database, GC, connection pool) during a repeat run to correlate the observed 2.5 s spikes with infrastructure or application resource behavior.  
- Run targeted sustained peak tests at 60 VUs for longer duration to observe stability and tail-latency behavior (as recommended in the analysis).  
- Instrument and capture distributed traces or logs for requests that hit the 2.5 s max to identify slow code paths or external dependencies.  
- Repeat the test from multiple load-generator locations to rule out network variability.  
- If spikes are reproducible, add finer-grained percentiles (p99, p99.9) to thresholds and alerts to monitor tail latency.

## 9. Conclusion

A STRESS test named "Stress Performance Test - test.k6.io" was executed against https://test.k6.io using GET with the staged load profile up to 60 VUs. Actual results show P95 = 332.25 ms and Error Rate = 0.00%, both within the configured SLAs (800 ms and 1% respectively). A maximum response-time spike to 2.5 s was observed (tail-latency risk) but no threshold for maximum response time was configured. Server-side resource correlation is not available from the supplied data, limiting root-cause analysis. Production readiness cannot be determined from this test alone because the available evidence is limited to the configured test scope and collected performance metrics.