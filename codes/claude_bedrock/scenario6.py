import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from claude_runner import run_concurrent, CODES_DIR

with open(os.path.join(CODES_DIR, '100code.py'), 'r', encoding='utf-8') as f:
    code = f.read()

run_concurrent(
    question=f"다음 코드를 보고 어떤 내용인지 3줄로 분석하라\n\n{code}",
    scenario_name="scenario6",
    desc="Claude Code (Bedrock) 인코딩 성능 분석 (30 동시 요청)",
    auth_mode="BEDROCK",
    prefix="claude-bedrock",
    n_users=30,
)
