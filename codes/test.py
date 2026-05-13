import subprocess
import os
import time
from datetime import datetime

def run_scenario(scenario_name):
    """지정된 시나리오 파일을 실행하고 결과를 문자열로 반환함"""
    file_path = f"{scenario_name}.py"
    output_log = ""
    
    if not os.path.exists(file_path):
        msg = f"[-] {file_path} 파일이 존재하지 않아 건너뜁니다.\n"
        print(msg, end="")
        return msg

    header = f"\n[▶] {scenario_name} 실행 중...\n"
    print(header, end="")
    output_log += header
    
    start = time.perf_counter()
    
    try:
        process = subprocess.Popen(
            ["python", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )

        for line in process.stdout:
            print(line, end="")
            output_log += line

        process.wait()
        
        footer = ""
        if process.returncode == 0:
            footer = f"[✓] {scenario_name} 완료 (소요 시간: {time.perf_counter() - start:.2f}초)\n"
        else:
            footer = f"[!] {scenario_name} 오류 발생 (Exit Code: {process.returncode})\n"
        
        print(footer, end="")
        output_log += footer

    except Exception as e:
        error_msg = f"[!] {scenario_name} 예외 발생: {e}\n"
        print(error_msg, end="")
        output_log += error_msg

    return output_log

def main():
    os.makedirs("./test", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = f"./test/test-{timestamp}.txt"
    
    combined_log = []
    scenarios = [f"scenario{i}" for i in range(1, 7)]
    
    start_msg = "="*60 + f"\nLLM & Vision 성능 테스트 통합 실행기\n시작 시간: {datetime.now()}\n" + "="*60 + "\n"
    print(start_msg, end="")
    combined_log.append(start_msg)

    total_start = time.perf_counter()

    for scenario in scenarios:
        scenario_log = run_scenario(scenario)
        combined_log.append(scenario_log)
        time.sleep(2)

    total_duration = time.perf_counter() - total_start
    
    end_msg = "\n" + "="*60 + f"\n모든 성능 테스트 시나리오 종료\n전체 총 소요 시간: {total_duration:.2f}초\n" + "="*60 + "\n"
    print(end_msg, end="")
    combined_log.append(end_msg)

    with open(log_file_path, "w", encoding="utf-8") as f:
        f.writelines(combined_log)
    
    print(f"\n[INFO] 전체 실행 결과가 저장되었습니다: {log_file_path}")

if __name__ == "__main__":
    main()