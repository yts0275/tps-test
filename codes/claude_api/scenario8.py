import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from claude_runner import run_concurrent

run_concurrent(
    question="다음 Workflow 의 Node 들의 흐름에 대해 최대한 상세히 서술하라. @langgraph.png",
    scenario_name="scenario8",
    desc="Claude Code (API Key) Vision 이미지 분석 (10 동시 요청)",
    auth_mode="API_KEY",
    prefix="claude-api",
    n_users=10,
)
