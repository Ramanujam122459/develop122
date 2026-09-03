import subprocess
from config import GENERATED_SCRIPT


class K6ExecutorAgent:

    def run(self):

        print("\n🤖 K6 Execution Agent is working...")
        print("🚀 Starting k6 test...\n")

        command = [
            "k6",
            "run",
            str(GENERATED_SCRIPT)
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }