import http from "k6/http";
import { sleep, check } from "k6";
// import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

const BASE_URL = __ENV.BASE_URL || "https://test.k6.io/";

export const options = {
  // vus: 3,
  // duration: "10s",

  stages: [
    { duration: "1s", target: 2 },
    { duration: "10s", target: 5 },
    { duration: "1s", target: 0 },
  ],

  thresholds: {
    http_req_duration: ["p(95) < 500"],
  },
};

export default function () {
  const res = http.get(BASE_URL);
  check(res, { " is status code 200 ": (r) => r.status === 200 });

  sleep(1);
}

// export function handleSummary(data) {
//   return {
//     "report.html": htmlReport(data),
//   };
// }
