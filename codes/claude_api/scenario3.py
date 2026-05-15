import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from claude_runner import run_concurrent

run_concurrent(
    question="퀵소트 구현을 하고, 각 줄마다 주석을 달라.",
    scenario_name="scenario3",
    desc="Claude Code (API Key) 디코딩 성능 분석 (10 동시 요청)",
    auth_mode="API_KEY",
    prefix="claude-api",
    n_users=10,
)
