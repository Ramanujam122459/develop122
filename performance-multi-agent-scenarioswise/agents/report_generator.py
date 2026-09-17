import asyncio
import json
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler

class ReportGeneratorAgent:
    pass


def __init__(self):
    base_dir = Path(__file__).parent.parent

    prompt_path = (
        base_dir
        / "prompts"
        / "report_generator_prompt.txt"
    )

    self.system_prompt = prompt_path.read_text(
        encoding="utf-8"
    )

async def run_async(
    self,
    test_plan: dict,
    analysis: dict
):

    print(
        "\n🤖 AI Report Generator Agent "
        "is working with Copilot..."
    )

    client = CopilotClient()

    await client.start()

    try:

        session = await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="auto"
        )

        prompt = f"""


{self.system_prompt}

============================================================
CURRENT PERFORMANCE TEST PLAN
=============================

The following JSON is the ONLY authoritative source for the
current test configuration.

CURRENT TEST PLAN:

{json.dumps(test_plan, indent=4)}

============================================================
CURRENT PERFORMANCE ANALYSIS
============================

The following JSON is the ONLY authoritative source for the
current test execution results.

CURRENT PERFORMANCE ANALYSIS:

{json.dumps(analysis, indent=4)}

============================================================
STRICT REPORT GENERATION RULES
==============================

Generate the final Markdown performance report using ONLY the
CURRENT PERFORMANCE TEST PLAN and CURRENT PERFORMANCE ANALYSIS.

IMPORTANT:

1. Never use values from previous test runs.

2. Never use values from previous reports.

3. Never use values from previous conversations.

4. Never use memory.

5. Never use example values as actual test values.

6. Never invent performance metrics.

7. Never invent VUs.

8. Never invent durations.

9. Never invent stages.

10. Never invent thresholds.

11. Never invent URLs.

12. Never invent HTTP methods.

13. Never invent test results.

14. Never assume the test is LOAD.

15. Test Type MUST exactly match the current test plan.

16. Test Name MUST exactly match the current test plan.

17. Target URL MUST exactly match the current test plan.

18. HTTP Method MUST exactly match the current test plan.

19. Load Profile MUST exactly match the current test plan.

20. Thresholds MUST exactly match the current test plan.

21. Actual performance metrics MUST come only from the current
    PERFORMANCE ANALYSIS.

22. For STRESS and SPIKE tests, preserve the exact stages from
    the current test plan.

23. Never replace staged execution with an invented fixed VU
    count.

24. Never replace staged execution with an invented duration.

25. Never create new numeric load profiles.

26. Never recommend a specific VU count unless it exists in the
    current test plan or analysis.

27. Never claim a maximum response-time threshold violation
    unless a maximum response-time threshold is explicitly
    configured.

28. Only compare actual metrics against thresholds that are
    explicitly configured in the current test plan.

29. If information is unavailable, write:

    Not Available

30. If information does not apply, write:

    Not Applicable

============================================================
FACTUAL ACCURACY
================

The report must distinguish between:

* Observed facts
* Test evidence
* Potential explanations
* Assumptions

Never present assumptions as confirmed facts.

Do NOT claim that any of the following caused a performance
problem unless the current PERFORMANCE ANALYSIS contains direct
evidence:

* CPU
* Memory
* Database
* Network
* Connection pools
* Thread pools
* Queues
* Garbage collection
* Infrastructure resources

If the analysis does not identify the root cause, say that the
root cause could not be determined from the available test data.

============================================================
TEST TYPE INTERPRETATION
========================

LOAD:

Focus on stability under the configured load, response time,
error rate, and threshold compliance.

STRESS:

Focus on behavior as load increases, response-time changes,
error behavior, threshold compliance, and evidence of
performance degradation.

Do NOT claim that maximum system capacity was reached unless
the current analysis explicitly proves it.

SPIKE:

Focus on behavior during sudden traffic increases, response
time during the spike, error behavior, and recovery behavior
when supported by evidence.

ENDURANCE:

Focus on long-running stability, response-time consistency,
error behavior, and evidence of degradation over time.

============================================================
PRODUCTION READINESS
====================

Do NOT automatically state that the system is:

* Production ready
* Production safe
* Suitable for production
* Approved for production
* Ready for production deployment
* Conditionally production ready

unless the CURRENT PERFORMANCE TEST PLAN or CURRENT PERFORMANCE
ANALYSIS explicitly provides evidence supporting such a claim.

The conclusion must remain limited to the executed test scope.

If production readiness cannot be determined from the available
evidence, state:

"Production readiness cannot be determined from this test alone
because the available evidence is limited to the configured test
scope and collected performance metrics."

============================================================
RECOMMENDATIONS
===============

Recommendations must be based only on the CURRENT test results.

Do NOT invent:

* VU counts
* Durations
* Stages
* Thresholds
* Capacity limits

For example, do NOT write:

"Increase the load to 25-30 VUs"

unless 25-30 VUs explicitly exists in the current test plan or
analysis.

Instead, if supported by the evidence, use wording such as:

"Consider extending the stress-test load beyond the current
peak to further characterize system capacity."

============================================================
REQUIRED REPORT
===============

Generate exactly these sections:

# Performance Test Report

## 1. Executive Summary

Mention:

* Current Test Type
* Current Test Name
* Target URL
* Overall Result
* Whether configured thresholds were met

Use current input values only.

## 2. Test Configuration

Include:

* Test Name
* Test Type
* Target URL
* HTTP Method
* Load Profile
* Virtual Users
* Duration
* Stages when applicable
* Test Scenarios when available

For staged tests use:

| Stage | Duration        | Target VUs      |
| ----- | --------------- | --------------- |
| 1     | <current value> | <current value> |

Do not replace stages with a fixed VU count.

## 3. Performance Thresholds

Include:

* P95 Response Time SLA
* Error Rate SLA

Use only the current test plan.

## 4. Test Results

Include:

* Overall Status
* P95 Response Time
* Maximum Response Time
* Error Rate
* Total Requests
* Throughput

Use only the current PERFORMANCE ANALYSIS.

## 5. Key Findings

Summarize only observations supported by the current analysis.

Relate the findings to the selected test type.

Do not turn assumptions into facts.

## 6. Performance Risks

List only risks supported by the current test evidence.

If no significant risks exist, state:

"No significant risks were identified based on the available
test evidence."

## 7. Possible Bottlenecks

Use two subsections:

### Observed Bottlenecks

Only include bottlenecks directly supported by test evidence.

If none exist, state:

"No confirmed bottlenecks were identified from the available
test evidence."

### Potential Bottlenecks

Only include possible explanations supported by the observed
behavior.

Clearly label them as potential or possible.

## 8. Recommendations

Provide actionable recommendations based only on the current
test results.

Do not invent numeric load profiles.

## 9. Conclusion

Summarize:

* What was tested
* Actual results
* Threshold compliance
* Important limitations or risks

Keep the conclusion within the scope of the executed test.

Do not make unsupported production-readiness claims.

============================================================
MARKDOWN OUTPUT RULES
=====================

Return ONLY valid Markdown.

Do NOT return:

* Markdown code fences
* ```
  ```
* ```markdown
  ```
* ```text
  ```
* Explanations before the report
* Explanations after the report
* "Here is the report"
* "The report is..."
* AI commentary
* Validation commentary

The first line of the response MUST be:

# Performance Test Report

Use properly formatted Markdown tables.

Correct:

| Parameter   | Value   |
| ----------- | ------- |
| Test Name   | <value> |
| Test Type   | <value> |
| Target URL  | <value> |
| HTTP Method | <value> |

Do NOT create malformed tables such as:

| ParameterValue |
| StageDurationTarget VUsPurpose |

The final response MUST contain ONLY the Markdown performance report.
"""


        response = await session.send_and_wait(prompt)

        report = response.data.content.strip()

        # Remove accidental Markdown code fences.
        lines = report.splitlines()

        cleaned_lines = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("```"):
                continue

            cleaned_lines.append(line)

        report = "\n".join(cleaned_lines).strip()

        # Ensure the report starts from the expected heading.
        report_start = report.find("# Performance Test Report")

        if report_start != -1:
            report = report[report_start:].strip()

        # Remove accidental AI commentary after the report.
        unwanted_markers = [
            "\nThe report above",
            "\nThis report has been",
            "\nThis report was",
            "\nI hope this report",
            "\nLet me know if",
            "\nIf you need",
            "\nPlease let me know"
        ]

        for marker in unwanted_markers:

            position = report.find(marker)

            if position != -1:
                report = report[:position].strip()

        return report

    finally:
        await client.stop()

def run(
    self,
    test_plan: dict,
    analysis: dict
):
    return asyncio.run(
        self.run_async(
            test_plan,
            analysis
        )
    )


ReportGeneratorAgent.__init__ = __init__
ReportGeneratorAgent.run_async = run_async
ReportGeneratorAgent.run = run

