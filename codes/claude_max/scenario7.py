import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from claude_runner import run_single

# claude -p 에서 @파일명 은 cwd(codes/) 기준으로 파일을 참조
# Claude Code 가 이미지 파일을 Vision 입력으로 처리하지 못할 경우 결과가 달라질 수 있음
run_single(
    question="다음 Workflow 의 Node 들의 흐름에 대해 최대한 상세히 서술하라. @langgraph.png",
    scenario_name="scenario7",
    desc="Claude Code (Max 플랜) Vision 이미지 분석 (단일 요청)",
    auth_mode="MAX",
    prefix="claude-max",
)
