import http from "k6/http";
import { sleep, check } from "k6";
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

export const options = {
  vus: 1,
  duration: "1s",
};

export default function () {
  const response = http.get("https://test.k6.io/");
  check(response,{"is statycode 200 " : (r) => r.status === 400})
}
sleep(2);

// export function handleSummary(data) {
//   return {
//     "ram.html": htmlReport(data),
//     // "ram.csv" : exportSummaryToCSV(data),
//   };
// }
