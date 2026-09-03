from pathlib import Path

BASE_DIR = Path(__file__).parent

K6_DIR = BASE_DIR / "k6"
RESULTS_DIR = BASE_DIR / "results"
REPORTS_DIR = BASE_DIR / "reports"

GENERATED_SCRIPT = K6_DIR / "generated_test.js"
RESULT_FILE = RESULTS_DIR / "result.json"
REPORT_FILE = REPORTS_DIR / "performance_report.md"

for directory in [K6_DIR, RESULTS_DIR, REPORTS_DIR]:
    directory.mkdir(exist_ok=True)