import time
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_fireworks import ChatFireworks
from langchain_aws import ChatBedrockConverse
from datetime import datetime

load_dotenv()


def set_model():
    MODE = os.environ.get("MODE")
    if MODE == "OPENAI":
        return ChatOpenAI(
            model=os.environ.get("MODEL_ID"),
        )
    elif MODE == "FIREWORKS":
        return ChatFireworks(
            model=f"accounts/fireworks/models/{os.environ.get('MODEL_ID')}",
        )
    elif MODE == "BEDROCK":
        return ChatBedrockConverse(
            region_name=os.getenv("REGION_NAME"),
            model_id=os.getenv("MODEL_ID"),
        )
    elif MODE == "LOCAL":
        return ChatOpenAI(
            model=os.getenv("MODEL_ID"),
            temperature=0.7,
            api_key="None",
            base_url=os.getenv("BASE_URL"),
        )

model = set_model()

from langchain.agents import create_agent

SYSTEM_PROMPT = """
너는 친절한 챗봇이다.
항상 한국어로 대답한다.
"""

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
)

# 성능 측정을 위한 변수 초기화
start_time = time.perf_counter()
tokens = 0
full_content = ""
last_usage = None

QUESTION = "퀵소트 구현을 하고, 각 줄마다 주석을 달라."

# 스트리밍 실행
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": QUESTION}]},
    stream_mode="messages",
    version="v2",
):
    if chunk["type"] == "messages":
        token_obj, metadata = chunk["data"]
        if token_obj.usage_metadata:
            last_usage = token_obj.usage_metadata
        if token_obj.content_blocks:
            for block in token_obj.content_blocks:
                if block.get("type") == "text":
                    full_content += block["text"]

tokens = last_usage.get("output_tokens", 0) if last_usage else len(full_content.split())

os.makedirs("./results", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"./results/{timestamp}-scenario1-user1.txt"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(full_content)

end_time = time.perf_counter()
duration = end_time - start_time
tps = tokens / duration if duration > 0 else 0

print("\n" + "=" * 50)
print("시나리오1: LLM 추론 - 디코딩 성능 분석 (단일 요청)")
print(f"질문: {QUESTION}")
print(f"초당 토큰 생성량 (TPS): {tps:.2f} tokens/s")
print(f"총 소요 시간: {duration:.4f}초")
print(f"총 생성 토큰 수: {tokens}")
print(f"결과 저장 완료: {file_path}")
print("=" * 50)
