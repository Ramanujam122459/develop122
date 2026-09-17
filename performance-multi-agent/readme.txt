				
	The Entire Flow :			
				
				
				USER REQUIREMENT
                           │
                           ▼
               TEST PLANNER AGENT
              ─────────────────────
              Understands requirement
              Creates test plan
                           │
                           ▼
                    TEST PLAN JSON
                           │
                           ▼
               K6 GENERATOR AGENT
              ─────────────────────
              Generates k6 script
                           │
                           ▼
                 GENERATED K6 SCRIPT
                           │
                           ▼
              SCRIPT REVIEWER AGENT
             ─────────────────────────
             Reviews & fixes script
                           │
                           ▼
                  REVIEWED K6 SCRIPT
                           │
                           ▼
                 ️ K6 EXECUTOR AGENT
                 ─────────────────────
                    Runs k6 test
                           │
                           ▼
                    RAW K6 RESULTS
                           │
                           ▼
               RESULT ANALYZER AGENT
              ─────────────────────────
                AI Performance Insights
                           │
                           ▼
              REPORT GENERATOR AGENT
             ──────────────────────────
              Professional Markdown Report
                           │
                           ▼
                 PERFORMANCE REPORT