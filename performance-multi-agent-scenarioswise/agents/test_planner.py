import asyncio
import json
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler


class TestPlannerAgent:

    def __init__(self):
        base_dir = Path(__file__).parent.parent
        prompt_path = base_dir / "prompts" / "planner_prompt.txt"

        self.system_prompt = prompt_path.read_text(encoding="utf-8")

    async def run_async(self, requirement: str):

        print("\n🤖 AI Test Planner Agent is working with Copilot...")

        client = CopilotClient()
        await client.start()

        try:
            session = await client.create_session(
                on_permission_request=PermissionHandler.approve_all,
                model="auto"
            )

            prompt = f"""
{self.system_prompt}

USER PERFORMANCE TESTING REQUIREMENT:
{requirement}
"""

            response = await session.send_and_wait(prompt)

            content = response.data.content.strip()

            # Remove markdown fences if Copilot adds them
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()

            test_plan = json.loads(content)

            return test_plan

        finally:
            await client.stop()

    def run(self, requirement: str):
        return asyncio.run(self.run_async(requirement))