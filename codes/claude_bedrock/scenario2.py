import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from claude_runner import run_single, CODES_DIR

with open(os.path.join(CODES_DIR, '100code.py'), 'r', encoding='utf-8') as f:
    code = f.read()

run_single(
    question=f"다음 코드를 보고 어떤 내용인지 3줄로 분석하라\n\n{code}",
    scenario_name="scenario2",
    desc="Claude Code (Bedrock) 인코딩 성능 분석 (단일 요청)",
    auth_mode="BEDROCK",
    prefix="claude-bedrock",
)
