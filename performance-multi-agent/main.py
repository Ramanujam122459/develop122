import json

from config import GENERATED_SCRIPT, REPORT_FILE

from agents.test_planner import TestPlannerAgent
from agents.k6_generator import K6ScriptGeneratorAgent
from agents.script_reviewer import ScriptReviewerAgent
from agents.k6_executor import K6ExecutorAgent
from agents.result_analyzer import ResultAnalyzerAgent
from agents.report_generator import ReportGeneratorAgent


def main():

    print("🚀 Multi-Agent Performance Testing PoC Started")

    # ==========================================
    # User Performance Testing Requirement
    # ==========================================
    requirement = """
    Perform a load test for a Device Enrollment API.

    Use 5 virtual users for 30 seconds.

    The P95 response time should be below 500ms.
    Error rate should remain below 1%.

    Use https://test.k6.io as the target URL for this PoC.
    Use GET request.
    """

    # ==========================================
    # Agent 1 - AI Test Planner
    # ==========================================
    planner = TestPlannerAgent()

    test_plan = planner.run(requirement)

    print("\n===== GENERATED AI TEST PLAN =====")

    print(
        json.dumps(
            test_plan,
            indent=4
        )
    )

    # ==========================================
    # Agent 2 - AI K6 Script Generator
    # ==========================================
    generator = K6ScriptGeneratorAgent()

    k6_script = generator.run(test_plan)

    print("\n===== GENERATED K6 SCRIPT =====")

    print(k6_script)

    # ==========================================
    # Agent 3 - AI Script Reviewer
    # ==========================================
    reviewer = ScriptReviewerAgent()

    reviewed_script = reviewer.run(k6_script)

    print("\n===== REVIEWED K6 SCRIPT =====")

    print(reviewed_script)

    # Save reviewed script for execution
    GENERATED_SCRIPT.write_text(
        reviewed_script,
        encoding="utf-8"
    )

    print("\n✅ Reviewed script saved successfully at:")

    print(GENERATED_SCRIPT)

    # ==========================================
    # Agent 4 - K6 Executor
    # ==========================================
    print("\n⚙️ K6 Executor Agent is working...")

    executor = K6ExecutorAgent()

    execution_result = executor.run()

    print("\n===== K6 EXECUTION RESULT =====")

    print(execution_result["stdout"])

    if execution_result["stderr"]:

        print("\n===== K6 ERRORS =====")

        print(execution_result["stderr"])

    print(
        f"\nReturn Code: "
        f"{execution_result['returncode']}"
    )

    # ==========================================
    # Agent 5 - AI Result Analyzer
    # ==========================================
    analyzer = ResultAnalyzerAgent()

    analysis = analyzer.run(
        execution_result,
        test_plan
    )

    print("\n===== PERFORMANCE ANALYSIS =====")

    print(
        json.dumps(
            analysis,
            indent=4
        )
    )

    # ==========================================
    # Agent 6 - AI Report Generator
    # ==========================================
    reporter = ReportGeneratorAgent()

    report = reporter.run(
        test_plan,
        analysis
    )

    REPORT_FILE.write_text(
        report,
        encoding="utf-8"
    )

    print("\n===== PERFORMANCE REPORT GENERATED =====")

    print(f"📄 Report saved at: {REPORT_FILE}")

    print("\n🎉 Multi-Agent Performance Testing PoC Completed Successfully!")


if __name__ == "__main__":
    main()