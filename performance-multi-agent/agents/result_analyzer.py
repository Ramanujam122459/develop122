import asyncio
import json
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler


class ResultAnalyzerAgent:

    def __init__(self):
        base_dir = Path(__file__).parent.parent

        prompt_path = (
            base_dir
            / "prompts"
            / "analyzer_prompt.txt"
        )

        self.system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

    async def run_async(
        self,
        execution_result: dict,
        test_plan: dict = None
    ):

        print(
            "\n🤖 AI Result Analyzer Agent "
            "is working with Copilot..."
        )

        client = CopilotClient()

        await client.start()

        try:

            session = await client.create_session(
                on_permission_request=PermissionHandler.approve_all,
                model="auto"
            )

            k6_output = execution_result.get(
                "stdout",
                ""
            )

            prompt = f"""
{self.system_prompt}

PERFORMANCE TEST PLAN:

{json.dumps(test_plan or {}, indent=4)}

K6 EXECUTION OUTPUT:

{k6_output}

Analyze the performance test results now.
"""

            response = await session.send_and_wait(
                prompt
            )

            content = response.data.content.strip()

            # Remove markdown fences if returned
            if content.startswith("```"):

                lines = content.splitlines()

                if lines and lines[0].startswith("```"):
                    lines = lines[1:]

                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]

                content = "\n".join(lines).strip()

            analysis = json.loads(content)

            return analysis

        finally:
            await client.stop()

    def run(
        self,
        execution_result: dict,
        test_plan: dict = None
    ):

        return asyncio.run(
            self.run_async(
                execution_result,
                test_plan
            )
        )