import http from "k6/http";
import { sleep, check, group } from "k6";
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

const BASE_URL = __ENV.BASE_URL = "https://test.k6.io/"

export const options = {
  vus: 10,
  duration: "10s",

  thresholds :{
    http_req_duration : ["p(95) < 500"]
  },
};

export default function () {
    group('homepage', ()=>{

         const res = http.get(BASE_URL);
  check(res, { " homepage status code 200 ": (r) => r.status === 200 });

    });
   
    group ('login', () => {
         const res = http.get(BASE_URL);
  check(res, { " homepage status code 200 ": (r) => r.status === 200 });
    });

    group ("place order" ,()=> {

         const res = http.get(BASE_URL);
  check(res, { " homepage status code 200 ": (r) => r.status === 200 });

    });
 

}
  sleep(1);

  export function handleSummary(data){
 return{

    'groupings.html' : htmlReport(data)
 }

  }

