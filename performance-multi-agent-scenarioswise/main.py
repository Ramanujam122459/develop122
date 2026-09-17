import json

from config import (
    GENERATED_SCRIPT,
    REPORT_FILE,
    load_test_config
)

from agents.test_planner import TestPlannerAgent
from agents.k6_generator import K6ScriptGeneratorAgent
from agents.script_reviewer import ScriptReviewerAgent
from agents.k6_executor import K6ExecutorAgent
from agents.result_analyzer import ResultAnalyzerAgent
from agents.report_generator import ReportGeneratorAgent


def save_test_plan(test_plan, file_path):
    """
    Save the AI-generated test plan as a Markdown file.
    """

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:

        # ==========================================
        # Title
        # ==========================================

        file.write("# Performance Test Plan\n\n")

        # ==========================================
        # Test Information
        # ==========================================

        file.write("## Test Information\n\n")

        file.write(
            f"- **Test Name:** "
            f"{test_plan.get('test_name', '')}\n"
        )

        file.write(
            f"- **Test Type:** "
            f"{test_plan.get('test_type', '')}\n\n"
        )

        # ==========================================
        # Target
        # ==========================================

        file.write("## Target\n\n")

        file.write(
            f"- **URL:** "
            f"{test_plan.get('target_url', '')}\n"
        )

        file.write(
            f"- **HTTP Method:** "
            f"{test_plan.get('http_method', '')}\n\n"
        )

        # ==========================================
        # Load Profile
        # ==========================================

        file.write("## Load Profile\n\n")

        load_profile = test_plan.get("load_profile", {})

        if "vus" in load_profile:
            file.write(
                f"- **VUs:** "
                f"{load_profile.get('vus', '')}\n"
            )

        if "duration" in load_profile:
            file.write(
                f"- **Duration:** "
                f"{load_profile.get('duration', '')}\n"
            )

        stages = load_profile.get("stages", [])

        if stages:

            file.write("- **Stages:**\n")

            for stage in stages:

                if isinstance(stage, dict):

                    duration = stage.get("duration", "")
                    target = stage.get("target", "")

                    file.write(
                        f"  - {duration} → {target} VUs\n"
                    )

        file.write("\n")

        # ==========================================
        # Thresholds
        # ==========================================

        file.write("## Thresholds\n\n")

        thresholds = test_plan.get("thresholds", {})

        file.write(
            f"- **P95 Response Time:** "
            f"{thresholds.get('p95_response_time_ms', '')} ms\n"
        )

        file.write(
            f"- **Error Rate:** "
            f"{thresholds.get('error_rate_percent', '')}%\n\n"
        )

        # ==========================================
        # Test Scenarios
        # ==========================================

        file.write("## Test Scenarios\n\n")

        scenarios = test_plan.get("scenarios", [])

        if scenarios:

            for index, scenario in enumerate(scenarios, start=1):

                if isinstance(scenario, dict):

                    name = scenario.get("name", "")
                    description = scenario.get("description", "")

                    file.write(
                        f"### {index}. {name}\n\n"
                    )

                    file.write(
                        f"{description}\n\n"
                    )

        else:

            file.write("No scenarios provided.\n\n")

        # ==========================================
        # Assumptions
        # ==========================================

        file.write("## Assumptions\n\n")

        assumptions = test_plan.get("assumptions", [])

        if assumptions:

            for assumption in assumptions:

                file.write(
                    f"- {assumption}\n"
                )

        else:

            file.write("- None\n")


def main():

    print("🚀 Multi-Agent Performance Testing PoC Started")

    # ==========================================
    # Load Test Configuration
    # ==========================================

    test_config = load_test_config()

    # ==========================================
    # Select Performance Test Scenario
    # ==========================================

    print("\nSelect Performance Test Type:")
    print("1. Load")
    print("2. Stress")
    print("3. Spike")
    print("4. Endurance")

    choice = input("\nEnter your choice (1-4): ").strip()

    scenario_map = {
        "1": "load",
        "2": "stress",
        "3": "spike",
        "4": "endurance"
    }

    if choice not in scenario_map:

        raise ValueError(
            "Invalid choice. Please select 1, 2, 3, or 4."
        )

    test_config["scenario"] = scenario_map[choice]

    print(
        f"\n✅ Selected Performance Test: "
        f"{test_config['scenario'].upper()}"
    )

    # ==========================================
    # Display Test Configuration
    # ==========================================

    print("\n===== TEST CONFIGURATION =====")

    print(
        json.dumps(
            test_config,
            indent=4
        )
    )

    # ==========================================
    # Build Performance Testing Requirement
    # ==========================================

    requirement = f"""
Perform a {test_config["scenario"]} performance test.

Target URL:
{test_config["target"]["url"]}

HTTP Method:
{test_config["target"]["method"]}

Load Profile:
{json.dumps(test_config["load_profile"], indent=4)}

Performance Thresholds:
{json.dumps(test_config["thresholds"], indent=4)}

Generate a structured performance test plan.
"""

    print("\n===== PERFORMANCE TEST REQUIREMENT =====")

    print(requirement)

    # ==========================================
    # Agent 1 - AI Test Planner
    # ==========================================

    print("\n🤖 Test Planner Agent is working...")

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
    # Save Test Plan
    # ==========================================

    test_plan_file = REPORT_FILE.parent / "test_plan.md"

    save_test_plan(
        test_plan,
        test_plan_file
    )

    print("\n✅ Test plan saved successfully at:")

    print(test_plan_file)

    # ==========================================
    # Agent 2 - AI K6 Script Generator
    # ==========================================

    print("\n🤖 K6 Script Generator Agent is working...")

    generator = K6ScriptGeneratorAgent()

    k6_script = generator.run(test_plan)

    print("\n===== GENERATED K6 SCRIPT =====")

    print(k6_script)

    # ==========================================
    # Agent 3 - AI Script Reviewer
    # ==========================================

    print("\n🤖 Script Reviewer Agent is working...")

    reviewer = ScriptReviewerAgent()

    reviewed_script = reviewer.run(k6_script)

    print("\n===== REVIEWED K6 SCRIPT =====")

    print(reviewed_script)

    # ==========================================
    # Save Reviewed K6 Script
    # ==========================================

    GENERATED_SCRIPT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

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

    print("\n🤖 Result Analyzer Agent is working...")

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

    print("\n🤖 Report Generator Agent is working...")

    reporter = ReportGeneratorAgent()

    report = reporter.run(
        test_plan,
        analysis
    )

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT_FILE.write_text(
        report,
        encoding="utf-8"
    )

    print("\n===== PERFORMANCE REPORT GENERATED =====")

    print(
        f"📄 Report saved at: {REPORT_FILE}"
    )

    # ==========================================
    # Completed
    # ==========================================

    print(
        "\n🎉 Multi-Agent Performance Testing PoC "
        "Completed Successfully!"
    )


if __name__ == "__main__":
    main()