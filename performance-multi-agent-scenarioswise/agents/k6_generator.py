import asyncio
import json
import re
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler


class K6ScriptGeneratorAgent:

    def __init__(self):
        base_dir = Path(__file__).parent.parent

        prompt_path = (
            base_dir
            / "prompts"
            / "k6_generator_prompt.txt"
        )

        self.system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

    # ==================================================
    # Extract stages from generated K6 JavaScript
    # ==================================================

    def extract_stages(self, content):

        pattern = (
            r"\{\s*duration:\s*['\"]([^'\"]+)['\"]"
            r"\s*,\s*target:\s*(\d+)\s*\}"
        )

        matches = re.findall(
            pattern,
            content
        )

        return [
            {
                "duration": duration,
                "target": int(target)
            }
            for duration, target in matches
        ]

    # ==================================================
    # Validate generated load profile
    # ==================================================

    def validate_load_profile(
        self,
        test_plan,
        generated_script
    ):

        test_type = test_plan.get(
            "test_type",
            ""
        ).upper()

        load_profile = test_plan.get(
            "load_profile",
            {}
        )

        expected_stages = load_profile.get(
            "stages",
            []
        )

        # ==============================================
        # LOAD TEST
        # ==============================================

        if test_type == "LOAD":

            expected_vus = load_profile.get(
                "vus"
            )

            expected_duration = load_profile.get(
                "duration"
            )

            if expected_vus is None:

                raise ValueError(
                    "LOAD test plan does not contain VUs."
                )

            if not expected_duration:

                raise ValueError(
                    "LOAD test plan does not contain duration."
                )

            vus_pattern = re.search(
                r"\bvus\s*:\s*(\d+)",
                generated_script
            )

            duration_pattern = re.search(
                r"\bduration\s*:\s*['\"]([^'\"]+)['\"]",
                generated_script
            )

            if not vus_pattern:

                raise ValueError(
                    "Generated LOAD script does not contain VUs."
                )

            if not duration_pattern:

                raise ValueError(
                    "Generated LOAD script does not contain duration."
                )

            generated_vus = int(
                vus_pattern.group(1)
            )

            generated_duration = (
                duration_pattern.group(1)
            )

            if generated_vus != expected_vus:

                raise ValueError(
                    "\n❌ LOAD PROFILE MISMATCH!\n\n"
                    f"Expected VUs: {expected_vus}\n"
                    f"Generated VUs: {generated_vus}"
                )

            if generated_duration != expected_duration:

                raise ValueError(
                    "\n❌ LOAD PROFILE MISMATCH!\n\n"
                    f"Expected duration: {expected_duration}\n"
                    f"Generated duration: {generated_duration}"
                )

            print(
                "\n✅ LOAD profile validation passed."
            )

            return

        # ==============================================
        # STRESS / SPIKE / ENDURANCE
        # ==============================================

        if test_type in {
            "STRESS",
            "SPIKE",
            "ENDURANCE"
        }:

            if not expected_stages:

                raise ValueError(
                    f"{test_type} test plan does not "
                    "contain stages."
                )

            generated_stages = (
                self.extract_stages(
                    generated_script
                )
            )

            expected_normalized = []

            for stage in expected_stages:

                expected_normalized.append(
                    {
                        "duration": str(
                            stage.get(
                                "duration",
                                ""
                            )
                        ),
                        "target": int(
                            stage.get(
                                "target",
                                0
                            )
                        )
                    }
                )

            # ==========================================
            # Compare stage count
            # ==========================================

            if len(generated_stages) != len(
                expected_normalized
            ):

                raise ValueError(
                    "\n❌ LOAD PROFILE MISMATCH!\n\n"
                    f"Expected stages:\n"
                    f"{json.dumps(expected_normalized, indent=4)}\n\n"
                    f"Generated stages:\n"
                    f"{json.dumps(generated_stages, indent=4)}"
                )

            # ==========================================
            # Compare every stage
            # ==========================================

            for index, (
                expected,
                generated
            ) in enumerate(
                zip(
                    expected_normalized,
                    generated_stages
                ),
                start=1
            ):

                if expected != generated:

                    raise ValueError(
                        "\n❌ LOAD PROFILE MISMATCH!\n\n"
                        f"Stage {index} does not match.\n\n"
                        f"Expected:\n"
                        f"{json.dumps(expected, indent=4)}\n\n"
                        f"Generated:\n"
                        f"{json.dumps(generated, indent=4)}"
                    )

            print(
                f"\n✅ {test_type} load profile "
                "validation passed."
            )

    # ==================================================
    # Clean Copilot Response
    # ==================================================

    def clean_ai_response(self, content):

        content = content.strip()

        # ==============================================
        # Remove markdown code fences
        # ==============================================

        lines = content.splitlines()

        cleaned_lines = []

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("```"):
                continue

            cleaned_lines.append(line)

        lines = cleaned_lines

        # ==============================================
        # Find beginning of JavaScript
        # ==============================================

        start_index = None

        for i, line in enumerate(lines):

            stripped = line.strip()

            if (
                stripped.startswith("import ")
                or stripped.startswith("export ")
            ):

                start_index = i
                break

        if start_index is None:

            raise ValueError(
                "AI did not return valid k6 JavaScript."
            )

        lines = lines[start_index:]

        # ==============================================
        # Remove explanation after JavaScript
        # ==============================================

        javascript_lines = []

        for line in lines:

            stripped = line.strip()

            # Common Copilot explanation patterns
            if stripped.startswith(
                "The script you provided"
            ):
                break

            if stripped.startswith(
                "The generated script"
            ):
                break

            if stripped.startswith(
                "This script"
            ):
                break

            if stripped.startswith(
                "Here is the"
            ):
                break

            if stripped.startswith(
                "Here’s the"
            ):
                break

            if stripped.startswith(
                "The above script"
            ):
                break

            javascript_lines.append(line)

        content = "\n".join(
            javascript_lines
        ).strip()

        return content

    # ==================================================
    # Validate generated JavaScript
    # ==================================================

    def validate_javascript(
        self,
        content
    ):

        # ==============================================
        # Required HTTP import
        # ==============================================

        if (
            "import http from 'k6/http';"
            not in content
        ):

            if (
                'import http from "k6/http";'
                not in content
            ):

                raise ValueError(
                    "Generated k6 script does not contain "
                    "the required k6 HTTP import."
                )

        # ==============================================
        # Options
        # ==============================================

        if "export const options" not in content:

            raise ValueError(
                "Generated k6 script does not contain "
                "an options object."
            )

        # ==============================================
        # Default function
        # ==============================================

        if "export default" not in content:

            raise ValueError(
                "Generated k6 script does not contain "
                "an export default function."
            )

        # ==============================================
        # Thresholds
        # ==============================================

        if "http_req_duration" not in content:

            raise ValueError(
                "Generated k6 script does not contain "
                "http_req_duration threshold."
            )

        if "http_req_failed" not in content:

            raise ValueError(
                "Generated k6 script does not contain "
                "http_req_failed threshold."
            )

        # ==============================================
        # HTTP request
        # ==============================================

        if not any(
            method in content
            for method in [
                "http.get(",
                "http.post(",
                "http.put(",
                "http.patch(",
                "http.del("
            ]
        ):

            raise ValueError(
                "Generated k6 script does not contain "
                "a valid HTTP request."
            )

    # ==================================================
    # Generate K6 Script
    # ==================================================

    async def run_async(
        self,
        test_plan: dict
    ):

        print(
            "\n🤖 AI K6 Script Generator Agent "
            "is working with Copilot..."
        )

        client = CopilotClient()

        await client.start()

        try:

            session = await client.create_session(
                on_permission_request=PermissionHandler.approve_all,
                model="auto"
            )

            # ==========================================
            # Extract Test Plan Information
            # ==========================================

            test_type = test_plan.get(
                "test_type",
                ""
            ).upper()

            target_url = test_plan.get(
                "target_url",
                ""
            )

            http_method = test_plan.get(
                "http_method",
                "GET"
            ).upper()

            load_profile = test_plan.get(
                "load_profile",
                {}
            )

            thresholds = test_plan.get(
                "thresholds",
                {}
            )

            expected_vus = load_profile.get(
                "vus"
            )

            expected_duration = load_profile.get(
                "duration"
            )

            expected_stages = load_profile.get(
                "stages",
                []
            )

            # ==========================================
            # Build Generator Prompt
            # ==========================================

            prompt = f"""
{self.system_prompt}

==================================================
AUTHORITATIVE PERFORMANCE TEST PLAN
==================================================

The following values are the ONLY source of truth.

Test Type:
{test_type}

Target URL:
{target_url}

HTTP Method:
{http_method}

VUs:
{expected_vus}

Duration:
{expected_duration}

Stages:
{json.dumps(expected_stages, indent=4)}

Thresholds:
{json.dumps(thresholds, indent=4)}

==================================================
CRITICAL RULE
==================================================

DO NOT invent any performance values.

DO NOT create your own load profile.

DO NOT use standard/default k6 stages.

DO NOT change the planner's values.

DO NOT increase VUs.

DO NOT decrease VUs.

DO NOT change stage durations.

DO NOT change stage targets.

DO NOT add stages.

DO NOT remove stages.

DO NOT reorder stages.

==================================================
LOAD TEST
==================================================

If Test Type is LOAD:

Use the exact VUs and duration provided above.

==================================================
STRESS / SPIKE / ENDURANCE
==================================================

If Test Type is STRESS, SPIKE, or ENDURANCE:

Use the stages provided above EXACTLY.

Every stage must have the exact:

- duration
- target

The number and order of stages must remain unchanged.

==================================================
TARGET
==================================================

Use this exact URL:

{target_url}

==================================================
HTTP METHOD
==================================================

Use this exact HTTP method:

{http_method}

==================================================
THRESHOLDS
==================================================

P95 response time:

{thresholds.get("p95_response_time_ms", "")} ms

Error rate:

{thresholds.get("error_rate_percent", "")}%

Convert these values into valid k6 thresholds.

==================================================
K6 REQUIREMENTS
==================================================

Generate valid Grafana k6 JavaScript.

The script must:

- import required k6 modules
- contain export const options
- contain export default
- execute the requested HTTP request
- use the exact target URL
- use the exact HTTP method
- use the exact load profile
- use the exact thresholds
- include a status code check
- include sleep(1)
- use meaningful tags
- use no external npm packages

==================================================
OUTPUT RULE
==================================================

Return ONLY executable JavaScript.

Do NOT return explanations.

Do NOT say:

"The script you provided is syntactically and semantically correct."

Do NOT say:

"The generated script is..."

Do NOT provide any introduction.

Do NOT provide any conclusion.

Do NOT use markdown.

Do NOT use markdown code fences.

Do NOT include ```javascript.

Do NOT include ```.

The response MUST begin with:

import http from 'k6/http';

Return ONLY the JavaScript.
"""

            # ==========================================
            # Send Prompt to Copilot
            # ==========================================

            response = await session.send_and_wait(
                prompt
            )

            content = response.data.content.strip()

            # ==========================================
            # Clean AI Response
            # ==========================================

            content = self.clean_ai_response(
                content
            )

            # ==========================================
            # Validate JavaScript
            # ==========================================

            self.validate_javascript(
                content
            )

            # ==========================================
            # Validate Load Profile
            # ==========================================

            print(
                "\n🔍 Validating generated load profile..."
            )

            self.validate_load_profile(
                test_plan,
                content
            )

            print(
                "\n✅ K6 Script Generator validation "
                "completed successfully."
            )

            return content

        finally:

            await client.stop()

    # ==================================================
    # Synchronous Wrapper
    # ==================================================

    def run(
        self,
        test_plan: dict
    ):

        return asyncio.run(
            self.run_async(test_plan)
        )