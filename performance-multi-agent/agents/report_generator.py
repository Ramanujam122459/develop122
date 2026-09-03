import asyncio
import json
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler


class ReportGeneratorAgent:

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

PERFORMANCE TEST PLAN:

{json.dumps(test_plan, indent=4)}

PERFORMANCE ANALYSIS:

{json.dumps(analysis, indent=4)}

Generate the professional Markdown performance report now.
"""

            response = await session.send_and_wait(
                prompt
            )

            report = response.data.content.strip()

            # Safety cleanup if AI returns markdown fences
            if report.startswith("```"):

                lines = report.splitlines()

                if lines and lines[0].startswith("```"):
                    lines = lines[1:]

                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]

                report = "\n".join(lines).strip()

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