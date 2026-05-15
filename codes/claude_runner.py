import asyncio
import json
import os
import time
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv

CODES_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(CODES_DIR, '.env'))


def get_auth_env(auth_mode: str) -> dict:
    env = os.environ.copy()
    if auth_mode == "API_KEY":
        key = os.getenv("CLAUDE_API_KEY")
        if key:
            env["ANTHROPIC_API_KEY"] = key
        # Bedrock 변수 제거 — logout 후에도 남아 있으면 충돌
        for k in ["ANTHROPIC_BEDROCK_BASE_URL", "AWS_ACCESS_KEY_ID",
                  "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"]:
            env.pop(k, None)
    elif auth_mode == "BEDROCK":
        env.pop("ANTHROPIC_API_KEY", None)  # API key가 Bedrock보다 우선시되는 것 방지
        for src, dst in [
            ("CLAUDE_BEDROCK_AWS_ACCESS_KEY_ID",     "AWS_ACCESS_KEY_ID"),
            ("CLAUDE_BEDROCK_AWS_SECRET_ACCESS_KEY", "AWS_SECRET_ACCESS_KEY"),
            ("CLAUDE_BEDROCK_AWS_SESSION_TOKEN",     "AWS_SESSION_TOKEN"),
            ("CLAUDE_BEDROCK_AWS_REGION",            "AWS_REGION"),
            ("CLAUDE_BEDROCK_AWS_REGION",            "AWS_DEFAULT_REGION"),
        ]:
            val = os.getenv(src)
            if val:
                env[dst] = val
        # logout 후에도 Bedrock 엔드포인트로 라우팅되도록 명시
        region = os.getenv("CLAUDE_BEDROCK_AWS_REGION", "us-east-1")
        env["ANTHROPIC_BEDROCK_BASE_URL"] = os.getenv(
            "CLAUDE_BEDROCK_BASE_URL",
            f"https://bedrock-runtime.{region}.amazonaws.com"
        )
    # MAX: ~/.claude/ 에 저장된 로그인 세션 자동 사용, 추가 env 불필요
    return env


def get_model(auth_mode: str) -> Optional[str]:
    env_map = {
        "MAX":     "CLAUDE_MAX_MODEL",
        "API_KEY": "CLAUDE_API_MODEL",
        "BEDROCK": "CLAUDE_BEDROCK_MODEL",
    }
    key = env_map.get(auth_mode)
    return os.getenv(key) if key else None


def _parse(output: str):
    """claude --output-format json 의 JSONL 출력을 파싱해 (content, tokens) 반환"""
    content, tokens = "", 0
    for line in output.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            t = d.get('type', '')
            if t == 'assistant':
                msg = d.get('message', {})
                tokens = msg.get('usage', {}).get('output_tokens', 0)
                for block in msg.get('content', []):
                    if block.get('type') == 'text':
                        content += block['text']
            elif t == 'result' and not content:
                content = d.get('result', '')
        except (json.JSONDecodeError, AttributeError):
            pass
    if not tokens and content:
        tokens = len(content.split())
    return content, tokens


async def _call(prompt: str, env: dict, model: Optional[str]):
    """claude CLI 를 subprocess 로 호출하고 (content, tokens) 반환"""
    cmd = ["claude", "-p", prompt, "--output-format", "json"]
    if model:
        cmd += ["--model", model]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
        cwd=CODES_DIR,  # langgraph.png, 100code.py 등 상대 경로 기준
    )
    out, _ = await proc.communicate()
    return _parse(out.decode('utf-8', errors='replace'))


def run_single(question: str, scenario_name: str, desc: str, auth_mode: str, prefix: str):
    env   = get_auth_env(auth_mode)
    model = get_model(auth_mode)

    start = time.perf_counter()
    content, tokens = asyncio.run(_call(question, env, model))
    duration = time.perf_counter() - start

    rdir = os.path.join(CODES_DIR, 'results')
    os.makedirs(rdir, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(rdir, f"{ts}-{prefix}-{scenario_name}-user1.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    tps = tokens / duration if duration > 0 else 0
    print("\n" + "="*50)
    print(desc)
    print(f"질문: {question[:60]}")
    print(f"초당 토큰 생성량 (TPS): {tps:.2f} tokens/s")
    print(f"총 소요 시간: {duration:.4f}초")
    print(f"총 생성 토큰 수: {tokens}")
    print(f"결과 저장 완료: {path}")
    print("="*50)


async def _gather(question: str, env: dict, model: Optional[str], n: int):
    tasks = [_call(question, env, model) for _ in range(n)]
    return await asyncio.gather(*tasks)


def run_concurrent(question: str, scenario_name: str, desc: str, auth_mode: str, prefix: str, n_users: int):
    env   = get_auth_env(auth_mode)
    model = get_model(auth_mode)

    start   = time.perf_counter()
    results = asyncio.run(_gather(question, env, model, n_users))
    duration = time.perf_counter() - start

    rdir = os.path.join(CODES_DIR, 'results')
    os.makedirs(rdir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    total_tokens = 0
    for i, (content, tokens) in enumerate(results, 1):
        path = os.path.join(rdir, f"{ts}-{prefix}-{scenario_name}-user{i}.txt")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        total_tokens += tokens

    sps = total_tokens / duration if duration > 0 else 0
    print("\n" + "="*50)
    print(desc)
    print(f"질문: {question[:60]}")
    print(f"초당 토큰 생성량 (TPS): {sps:.2f} tokens/s")
    print(f"총 소요 시간: {duration:.4f}초")
    print(f"총 생성 토큰 수: {total_tokens}")
    print(f"평균 초당 토큰 생성량: {sps/n_users:.2f} tokens/s")
    print(f"평균 생성 토큰 수: {total_tokens/n_users:.2f}")
    print(f"결과 파일 저장 완료 ({ts}-{prefix}-{scenario_name}-user1~{n_users}.txt)")
    print("="*50)
