import http from "k6/http";
import { check, sleep } from "k6";
import { html } from "k6/html";

export default function () {
  http.get("https://test.k6.io");
  sleep(1);
}
