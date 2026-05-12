import http from "k6/http";
import { sleep, check, group } from "k6";
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";
import { textSummary } from "https://jslib.k6.io/k6-summary/0.0.1/index.js";

const BASE_URL = __ENV.BASE_URL || "https://test.k6.io/";

const TRAFFIC_SPLIT = {
  home: 0.6,
  loginpage: 0.15,
  productbooking: 0.15,
  signout: 0.1,
};

export const options = {
  vus : 5,
  duration : '5s',

//   stages: [
//     { duration: "2s", target: 10 },
//     { duration: "5s", target: 10 },
//     { duration: "2s", target: 0 },
//   ],

  thresholds: {
    http_req_duration: ["p(95) < 500"],
  },
};

export default function () {
  const random = Math.random();

  if (random < TRAFFIC_SPLIT.home) {
    group("homepage", () => {
      const responcecode = http.get(BASE_URL);

      check(responcecode, { "is status code 200 ": (r) => r.status === 200 });
    });


  } 
  else if (
    random < TRAFFIC_SPLIT.home + TRAFFIC_SPLIT.loginpage){

    group("loginpage", () => {
      const responcecode = http.get(BASE_URL);

      check(responcecode, { "is status code 200 ": (r) => r.status === 200 });
    });
  }

else if (random < TRAFFIC_SPLIT.home + TRAFFIC_SPLIT.loginpage + TRAFFIC_SPLIT.productbooking ){

  group("productbookingpage", () => {
    const responcecode = http.get(BASE_URL);

    check(responcecode, { "is status code 200 ": (r) => r.status === 200 });
  });
}


else{

  group("signout", () => {
    const responcecode = http.get(BASE_URL);

    check(responcecode, { "is status code 200 ": (r) => r.status === 200 });
  });
}

  sleep(0.5);
}

export function handleSummary(data) {
  return {
    "htmlreport2.html": htmlReport(data),
    // "reportsummery.csv": exportSummaryToCSV(data),
  };
}
