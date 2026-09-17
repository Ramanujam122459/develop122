import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '1m', target: 10 },
        { duration: '2m', target: 25 },
        { duration: '2m', target: 40 },
        { duration: '2m', target: 60 },
        { duration: '1m', target: 0 }
    ],
    thresholds: {
        http_req_duration: ['p(95)<800'],
        http_req_failed: ['rate<0.01']
    }
};

export default function () {
    const res = http.get('https://test.k6.io', {
        tags: { name: 'StressTest' }
    });

    check(res, {
        'status is 200': (r) => r.status === 200
    });

    sleep(1);
}