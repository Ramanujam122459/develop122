import http from 'k6/http';
import { check, sleep } from 'k6';

const TARGET_URL = 'https://test.k6.io';

export const options = {
  scenarios: {
    'Device Enrollment Load Test': {
      executor: 'constant-vus',
      vus: 10,
      duration: '50s',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const params = {
    headers: {
      'Accept': 'application/json',
      'User-Agent': 'k6-device-enroll-test/1.0',
    },
    tags: {
      test_name: 'Device Enrollment API Load Test',
      scenario: 'Device Enrollment Load Test',
      endpoint: 'device-enrollment',
      method: 'GET',
    },
  };

  const res = http.get(TARGET_URL, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  sleep(1);
}