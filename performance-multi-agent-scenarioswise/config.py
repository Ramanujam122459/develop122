import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

TEST_CONFIG_FILE = BASE_DIR / "test_config.json"

GENERATED_SCRIPT = BASE_DIR / "k6" / "generated_test.js"

REPORT_FILE = BASE_DIR / "reports" / "performance_report.md"


def load_test_config():

    with open(TEST_CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)