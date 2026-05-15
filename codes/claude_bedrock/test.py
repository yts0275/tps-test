import subprocess
import os
import time
from datetime import datetime

SCENARIO_DIR = os.path.dirname(os.path.abspath(__file__))


def do_logout():
    print("[INFO] 기존 로그인 세션 로그아웃 중...")
    try:
        result = subprocess.run(
            ["claude", "logout"],
            input="y\n",
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        msg = "[INFO] 로그아웃 완료\n" if result.returncode == 0 else "[WARN] 로그아웃 실패 (계속 진행)\n"
        print(msg, end="")
    except Exception as e:
        print(f"[WARN] 로그아웃 예외 (계속 진행): {e}\n", end="")


def run_scenario(name):
    file_path = os.path.join(SCENARIO_DIR, f"{name}.py")
    log = ""

    if not os.path.exists(file_path):
        msg = f"[-] {name}.py 파일이 없어 건너뜁니다.\n"
        print(msg, end="")
        return msg

    header = f"\n[▶] {name} 실행 중...\n"
    print(header, end="")
    log += header
    start = time.perf_counter()

    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        proc = subprocess.Popen(
            ["python", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            env=env,
        )
        for line in proc.stdout:
            print(line, end="")
            log += line
        proc.wait()
        elapsed = time.perf_counter() - start
        footer = f"[{'OK' if proc.returncode == 0 else '!!'}] {name} {'완료' if proc.returncode == 0 else '오류'} (소요: {elapsed:.2f}초)\n"
        print(footer, end="")
        log += footer
    except Exception as e:
        err = f"[!] {name} 예외: {e}\n"
        print(err, end="")
        log += err

    return log


def main():
    log_dir = os.path.join(SCENARIO_DIR, '..', '..', 'test')
    os.makedirs(log_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(log_dir, f"test-claude-bedrock-{ts}.txt")

    header = "="*60 + f"\nClaude Code (Bedrock) 성능 테스트\n시작: {datetime.now()}\n" + "="*60 + "\n"
    print(header, end="")
    logs = [header]

    do_logout()
    total_start = time.perf_counter()
    for i in range(1, 10):
        logs.append(run_scenario(f"scenario{i}"))
        time.sleep(2)

    footer = "\n" + "="*60 + f"\n전체 완료  총 소요: {time.perf_counter()-total_start:.2f}초\n" + "="*60 + "\n"
    print(footer, end="")
    logs.append(footer)

    with open(log_path, 'w', encoding='utf-8') as f:
        f.writelines(logs)
    print(f"\n[INFO] 결과 저장: {log_path}")


if __name__ == "__main__":
    main()
