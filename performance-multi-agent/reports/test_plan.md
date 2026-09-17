# Performance Test Plan

## Test Information

- **Test Name:** Stress Test - test.k6.io GET Request
- **Test Type:** STRESS

## Target

- **URL:** https://test.k6.io
- **HTTP Method:** GET

## Load Profile

- **VUs:** 0
- **Duration:** 
- **Stages:**
  - 10s → 10 VUs
  - 15s → 25 VUs
  - 15s → 40 VUs
  - 10s → 0 VUs

## Thresholds

- **P95 Response Time:** 800 ms
- **Error Rate:** 1%

## Test Scenarios

### 1. Gradual Load Increase

Progressively increase virtual users from normal baseline (10 VUs) to stress level (40 VUs) to identify performance degradation points and system capacity limits.

### 2. Recovery Validation

Verify system recovery after ramp-down from peak stress load back to zero, ensuring no lingering performance issues or resource exhaustion.

## Assumptions

- Stress test uses staged load profile with gradual VU increase to identify capacity and performance degradation.
- Normal baseline load inferred as 10 VUs; stress level set to 40 VUs (4x baseline) to exceed expected load.
- Total test duration constrained to 50s as specified in the provided load profile.
- P95 response time threshold of 800ms is maintained across all load stages.
- Error rate must not exceed 1% at any point during the stress test.
