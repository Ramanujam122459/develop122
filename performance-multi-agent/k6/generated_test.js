import http from 'k6/http';
import { check, sleep } from 'k6';

const TEST_NAME = 'Device Enrollment API Load Test';
const TARGET_URL = 'https://test.k6.io';
const HTTP_METHOD = 'GET';
const SCENARIO_NAME = 'Device Enrollment Baseline';

export let options = {
  vus: 5,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
  tags: {
    test_name: TEST_NAME,
  },
};

export default function () {
  const params = {
    tags: {
      test_name: TEST_NAME,
      scenario: SCENARIO_NAME,
      method: HTTP_METHOD,
    },
  };

  const res = http.get(TARGET_URL, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  sleep(1);
}