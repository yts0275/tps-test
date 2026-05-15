import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from claude_runner import run_concurrent

run_concurrent(
    question="퀵소트 구현을 하고, 각 줄마다 주석을 달라.",
    scenario_name="scenario5",
    desc="Claude Code (Bedrock) 디코딩 성능 분석 (30 동시 요청)",
    auth_mode="BEDROCK",
    prefix="claude-bedrock",
    n_users=30,
)
