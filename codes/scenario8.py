import time
import os
import asyncio
import httpx
import base64
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_fireworks import ChatFireworks
from langchain_aws import ChatBedrockConverse
from langchain.agents import create_agent
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

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        return None

async def run_request(agent, messages):
    full_content = ""
    last_usage = None
    async for chunk in agent.astream(
        {"messages": messages},
        stream_mode="messages",
        version="v2",
    ):
        if chunk["type"] == "messages":
            token_obj, _ = chunk["data"]
            if token_obj.usage_metadata:
                last_usage = token_obj.usage_metadata
            if token_obj.content_blocks:
                for block in token_obj.content_blocks:
                    if block.get("type") == "text":
                        full_content += block["text"]
    tokens = last_usage.get('output_tokens', 0) if last_usage else len(full_content.split())
    return tokens, full_content

async def main():
    IMAGE_PATH = "langgraph.png"
    base64_image = encode_image(IMAGE_PATH)
    
    if not base64_image:
        print(f"에러: '{IMAGE_PATH}' 파일을 찾을 수 없어 시나리오를 중단합니다.")
        return

    QUESTION_TEXT = "다음 Workflow 의 Node 들의 흐름에 대해 최대한 상세히 서술하라."
    CONCURRENT_USERS = 10
    
    shared_messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": QUESTION_TEXT},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
            ],
        }
    ]

    limits = httpx.Limits(max_keepalive_connections=50, max_connections=100)
    async with httpx.AsyncClient(limits=limits, timeout=180.0) as client:
        model = set_model()

        SYSTEM_PROMPT = "너는 이미지를 상세히 분석하는 전문 어시스턴트다. 항상 한국어로 대답한다."
        agent = create_agent(model=model, system_prompt=SYSTEM_PROMPT)
        
        start_time = time.perf_counter()
        tasks = [run_request(agent, shared_messages) for _ in range(CONCURRENT_USERS)]
        results = await asyncio.gather(*tasks)
        duration = time.perf_counter() - start_time

        os.makedirs("./results", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, (tokens, content) in enumerate(results, 1):
            file_path = f"./results/{timestamp}-scenario8-user{i}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        total_tokens = sum(r[0] for r in results)
        system_tps = total_tokens / duration if duration > 0 else 0

        print("\n" + "="*50)
        print(f"시나리오8: Vision 추론 - 이미지 분석 ({CONCURRENT_USERS}개 동시 요청 처리)")
        print(f"질문: {QUESTION_TEXT}")
        print(f"초당 토큰 생성량 (TPS): {system_tps:.2f} tokens/s")
        print(f"총 소요 시간: {duration:.4f}초")
        print(f"총 생성 토큰 수: {total_tokens}")
        print(f"평균 초당 토큰 생성량: {system_tps / CONCURRENT_USERS:.2f} tokens/s")
        print(f"평균 생성 토큰 수: {total_tokens / CONCURRENT_USERS:.2f}")
        print(f"결과 파일 저장 완료: ./results/{timestamp}-scenario8-user1~{CONCURRENT_USERS}.txt")
        print("="*50)

if __name__ == "__main__":
    asyncio.run(main())