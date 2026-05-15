import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from claude_runner import run_single

run_single(
    question="퀵소트 구현을 하고, 각 줄마다 주석을 달라.",
    scenario_name="scenario1",
    desc="Claude Code (Max 플랜) 디코딩 성능 분석 (단일 요청)",
    auth_mode="MAX",
    prefix="claude-max",
)
