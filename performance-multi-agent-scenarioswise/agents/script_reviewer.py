import asyncio
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler


class ScriptReviewerAgent:

    def __init__(self):
        base_dir = Path(__file__).parent.parent

        prompt_path = (
            base_dir
            / "prompts"
            / "reviewer_prompt.txt"
        )

        self.system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

    async def run_async(self, k6_script: str):

        print(
            "\n🤖 AI Script Reviewer Agent "
            "is reviewing the generated k6 script..."
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

GENERATED K6 SCRIPT:

{k6_script}

Review and return the corrected k6 script.
"""

            response = await session.send_and_wait(
                prompt
            )

            content = response.data.content.strip()

            # Remove markdown code fences if AI adds them
            if content.startswith("```"):

                lines = content.splitlines()

                if lines and lines[0].startswith("```"):
                    lines = lines[1:]

                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]

                content = "\n".join(lines).strip()

            return content

        finally:
            await client.stop()

    def run(self, k6_script: str):
        return asyncio.run(
            self.run_async(k6_script)
        )