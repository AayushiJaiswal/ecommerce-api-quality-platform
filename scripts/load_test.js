import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    vus: 10,
    duration: '20s',
    thresholds: {
        http_req_duration: ['p(95)<500'],
        http_req_failed: ['rate<0.01'],
    },
};

export default function () {
    const res1 = http.get('http://127.0.0.1:8000/health');
    check(res1, {
        'health status is 200': (r) => r.status === 200,
    });

    const res2 = http.get('http://127.0.0.1:8000/products/');
    check(res2, {
        'products status is 200': (r) => r.status === 200,
    });

    sleep(1);
}