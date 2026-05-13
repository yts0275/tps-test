# LLM 모델 벤치마크 분석 보고서

> 분석 기준일: 2026-05-13  

---

## 요약 및 추천

### 용도별 추천 모델

| 용도 | 추천 모델 | 이유 |
|---|---|---|
| **최고 처리속도 (텍스트)** | Amazon Bedrock Tokyo gpt-oss-20b | 디코딩 TPS 전체 1위 (10명: 151.86, 30명: 135.67) |
| **최고 가성비 (텍스트)** | Amazon Bedrock Tokyo gpt-oss-20b | 가성비 지수 1위(345.1), 저렴한 단가 |
| **VL + 성능/가성비** | OpenAI gpt-5-nano | 이미지분석 TPS 1위, VL 모델 중 가성비 최상(지수 236.1) |
| **고부하 안정성** | OpenAI gpt-5.4-nano / gpt-5-mini | 30명 동시요청 시 TPS 저하율 최저 |
| **비용 절감 최우선** | Amazon Bedrock US gpt-oss-20b | Input $0.07/Output $0.30, 충분한 TPS |

### 주의해야 할 모델

| 모델 | Provider/Region | 문제점 |
|---|---|---|
| qwen3-coder-30b | Amazon Bedrock US | 30명 동시 시 TPS 65.6% 급락 (19.43 수준), 고부하 환경 부적합 |
| gpt-5.4-nano | OpenAI | 인코딩 TPS가 30명 시 72% 급락 (46.24 → 12.96) |
| gpt-5-mini, gpt-5.1-codex-mini | OpenAI | 출력 비용 $2/1M으로 최고가 대비 성능은 중간 수준 |
| qwen3-14b | Local | TPS 전체 최하위 (디코딩 10명: 22.68), 개인 장비 한계 명확 |

### 종합 판단

1. **Amazon Bedrock Tokyo 리전**이 전반적으로 가장 높은 TPS를 제공하며, 한국에서 서비스할 경우 지리적으로도 유리하다.
2. **gpt-oss-20b** 모델이 텍스트 생성 속도와 가성비 모두에서 압도적 우위를 보인다.
3. **VL 기능이 필요하다면** OpenAI gpt-5-nano가 성능과 가성비를 동시에 만족시킨다.
4. **고부하(30명 이상) 서비스**를 계획한다면 TPS 저하율이 낮은 OpenAI gpt-5.4-nano를 고려해야 한다.
5. **Local 환경(qwen3-14b)**은 비용 없이 사용 가능하나, TPS가 타 플랫폼 대비 현저히 낮아 개발·테스트 목적에만 적합하다.
6. **OpenAI gpt-5-nano의 위치**: 가성비 지수 236.1로 전체 3위이며, VL 지원 모델 중에서는 단연 1위다. 이미지분석 TPS도 전체 1위(10명: 123.91)이고, 입력 비용($0.05/1M)은 전 모델 중 최저다. 텍스트 전용이라면 Bedrock Tokyo gpt-oss-20b에 밀리지만, VL이 필요한 상황에서는 성능과 비용 모두 최선의 선택이다.
7. **대한민국에서 Bedrock US 리전을 선택할 이유는 없다**: Tokyo 리전 대비 TPS가 모델에 따라 20~65% 낮고, 비용 절감폭은 고작 7~22%에 불과하다. 지리적 레이턴시까지 고려하면 한국 서비스 기준으로 US 리전은 선택할 근거가 없다.
8. **Fireworks AI 를 선택할 이유가 없다**: 텍스트 전용 모델(gpt-oss-20b)의 가성비 지수는 127.5로, 동급 Bedrock US(282.7)의 절반에도 못 미친다. VL 모델(qwen3-vl-30b, 가성비 123.0)도 OpenAI gpt-5-nano(가성비 236.1)보다 가성비가 낮고 이미지분석 TPS도 떨어진다. 텍스트든 VL이든 Bedrock 또는 OpenAI가 모든 면에서 우위이므로, Fireworks AI를 선택할 실질적 이유가 없다.

---

## 1. 데이터 개요

| 항목 | 내용 |
|---|---|
| 총 테스트 모델 수 | 16개 |
| Provider | Amazon Bedrock, Fireworks AI, Local, OpenAI |
| 측정 지표 | 디코딩 TPS / 인코딩 TPS (10명·30명 동시요청), 이미지분석 TPS (10명·30명) |
| VL(Vision-Language) 지원 모델 | 5개 |

### 컬럼 설명

- **VL**: 이미지 분석(Vision-Language) 기능 지원 여부 (O=지원, X=미지원)
- **디코딩 TPS**: 모델이 토큰을 생성하는 속도 (출력 처리량)
- **인코딩 TPS**: 모델이 입력 프롬프트를 처리하는 속도
- **이미지분석 TPS**: 이미지를 포함한 멀티모달 요청 처리 속도
- **X (TPS 값)**: 해당 기능 미지원 또는 미측정

---

## 2. Provider별 모델 현황

| Provider | 모델 수 | 모델명 | VL 지원 |
|---|---|---|---|
| Amazon Bedrock (Tokyo) | 4 | gpt-oss-20b, gpt-oss-120b, qwen3-32b, qwen3-coder-30b | 없음 |
| Amazon Bedrock (US) | 4 | gpt-oss-20b, gpt-oss-120b, qwen3-32b, qwen3-coder-30b | 없음 |
| Fireworks AI | 3 | gpt-oss-20b, gpt-oss-120b, qwen3-vl-30b | qwen3-vl-30b만 지원 |
| Local (Mincoding) | 1 | qwen3-14b | 없음 |
| OpenAI | 4 | gpt-5-nano, gpt-5.4-nano, gpt-5.1-codex-mini, gpt-5-mini | 전 모델 지원 |

---

## 3. VL(Vision-Language) 지원 현황

VL을 지원하는 모델은 전체 16개 중 **5개(31.3%)**이다.

| Provider | Model | 이미지분석 TPS (10명) | 이미지분석 TPS (30명) |
|---|---|---|---|
| OpenAI | gpt-5-nano | **123.91** | **106.38** |
| Fireworks AI | qwen3-vl-30b | 106.22 | 80.26 |
| OpenAI | gpt-5.4-nano | 100.91 | 81.69 |
| OpenAI | gpt-5.1-codex-mini | 68.10 | 66.39 |
| OpenAI | gpt-5-mini | 57.06 | 53.77 |

**정리:**
- 이미지분석 TPS 1위: **OpenAI gpt-5-nano** (10명: 123.91, 30명: 106.38)
- Fireworks AI qwen3-vl-30b는 OpenAI 모델보다 저렴한 가격($0.15/$0.6)으로 준수한 이미지분석 성능 제공
- OpenAI gpt-5.4-nano는 30명 기준 이미지분석 TPS(81.69)가 Fireworks AI qwen3-vl-30b(80.26)와 거의 동일하나 비용이 약 2.8배 높음

---

## 4. 비용 분석

### 4-1. 입력 비용 (Input $/1M tokens)

| 순위 | Provider | Model | Input ($/1M) |
|---|---|---|---|
| 1 (최저) | OpenAI | gpt-5-nano | **$0.05** |
| 2 | Amazon Bedrock (US) | gpt-oss-20b | $0.07 |
| 2 | Fireworks AI | gpt-oss-20b | $0.07 |
| 3 | Amazon Bedrock (Tokyo) | gpt-oss-20b | $0.08 |
| 4 | Amazon Bedrock (US) | gpt-oss-120b, qwen3-32b, qwen3-coder-30b | $0.15 |
| 4 | Fireworks AI | gpt-oss-120b, qwen3-vl-30b | $0.15 |
| 4 | Amazon Bedrock (Tokyo) | gpt-oss-120b, qwen3-32b, qwen3-coder-30b | $0.18 |
| 5 | OpenAI | gpt-5.4-nano | $0.20 |
| 6 (최고) | OpenAI | gpt-5.1-codex-mini, gpt-5-mini | **$0.25** |

### 4-2. 출력 비용 (Output $/1M tokens)

| 순위 | Provider | Model | Output ($/1M) |
|---|---|---|---|
| 1 (최저) | Amazon Bedrock (US) | gpt-oss-20b | **$0.30** |
| 1 (최저) | Fireworks AI | gpt-oss-20b | **$0.30** |
| 2 | Amazon Bedrock (Tokyo) | gpt-oss-20b | $0.36 |
| 3 | OpenAI | gpt-5-nano | $0.40 |
| 4 | Amazon Bedrock (US) | gpt-oss-120b, qwen3-32b, qwen3-coder-30b | $0.60 |
| 4 | Fireworks AI | gpt-oss-120b, qwen3-vl-30b | $0.60 |
| 4 | Amazon Bedrock (Tokyo) | gpt-oss-120b, qwen3-32b, qwen3-coder-30b | $0.73 |
| 5 | OpenAI | gpt-5.4-nano | $1.25 |
| 6 (최고) | OpenAI | gpt-5.1-codex-mini, gpt-5-mini | **$2.00** |

**정리:**
- OpenAI의 고사양 모델(gpt-5.1-codex-mini, gpt-5-mini)은 출력 비용이 Amazon Bedrock/Fireworks AI 대비 **최대 6.7배** 비쌈
- Local(Mincoding) 환경은 별도 API 과금 없음 (하드웨어 비용만 발생)
- Amazon Bedrock Tokyo 리전은 US 리전보다 Input 약 7~20%, Output 약 17~22% 비쌈

---

## 5. TPS 성능 분석

### 5-1. 디코딩 TPS 순위 (10명 동시요청)

| 순위 | Provider | Region | Model | 디코딩 TPS |
|---|---|---|---|---|
| 1 | Amazon Bedrock | Tokyo | gpt-oss-20b | **151.86** |
| 2 | Amazon Bedrock | Tokyo | gpt-oss-120b | 138.04 |
| 3 | Amazon Bedrock | Tokyo | qwen3-coder-30b | 116.81 |
| 4 | OpenAI | - | gpt-5-nano | 106.24 |
| 5 | Amazon Bedrock | US | gpt-oss-20b | 104.61 |
| 6 | Amazon Bedrock | Tokyo | qwen3-32b | 95.04 |
| 7 | OpenAI | - | gpt-5.4-nano | 89.12 |
| 8 | Fireworks AI | - | qwen3-vl-30b | 92.25 |
| 9 | Amazon Bedrock | US | qwen3-32b | 79.47 |
| 10 | Amazon Bedrock | US | gpt-oss-120b | 78.87 |
| 11 | Fireworks AI | - | gpt-oss-120b | 77.52 |
| 12 | OpenAI | - | gpt-5.1-codex-mini | 68.63 |
| 13 | OpenAI | - | gpt-5-mini | 57.71 |
| 14 | Amazon Bedrock | US | qwen3-coder-30b | 56.48 |
| 15 | Fireworks AI | - | gpt-oss-20b | 47.18 |
| 16 | Local | Mincoding | qwen3-14b | **22.68** |

### 5-2. 디코딩 TPS 순위 (30명 동시요청)

| 순위 | Provider | Region | Model | 디코딩 TPS |
|---|---|---|---|---|
| 1 | Amazon Bedrock | Tokyo | gpt-oss-20b | **135.67** |
| 2 | Amazon Bedrock | Tokyo | gpt-oss-120b | 109.47 |
| 3 | Amazon Bedrock | US | gpt-oss-20b | 89.62 |
| 4 | OpenAI | - | gpt-5.4-nano | 83.02 |
| 5 | OpenAI | - | gpt-5-nano | 70.8 |
| 6 | Amazon Bedrock | Tokyo | qwen3-32b | 73.14 |
| 7 | Fireworks AI | - | qwen3-vl-30b | 68.04 |
| 8 | Amazon Bedrock | Tokyo | qwen3-coder-30b | 65.3 |
| 9 | Amazon Bedrock | US | qwen3-32b | 64.58 |
| 10 | Amazon Bedrock | US | gpt-oss-120b | 59.89 |
| 11 | OpenAI | - | gpt-5.1-codex-mini | 58.83 |
| 12 | Fireworks AI | - | gpt-oss-120b | 51.58 |
| 13 | OpenAI | - | gpt-5-mini | 53.37 |
| 14 | Fireworks AI | - | gpt-oss-20b | 30.54 |
| 15 | Amazon Bedrock | US | qwen3-coder-30b | 19.43 |
| 16 | Local | Mincoding | qwen3-14b | **13.68** |

### 5-3. 인코딩 TPS 순위 (10명 / 30명 동시요청)

| Provider | Region | Model | 인코딩 TPS(10명) | 인코딩 TPS(30명) |
|---|---|---|---|---|
| Amazon Bedrock | Tokyo | gpt-oss-20b | **99.04** | **93.40** |
| Amazon Bedrock | Tokyo | gpt-oss-120b | 97.45 | 68.67 |
| OpenAI | - | gpt-5-nano | 86.87 | 66.22 |
| OpenAI | - | gpt-5.4-nano | 46.24 | 12.96 |
| Amazon Bedrock | Tokyo | qwen3-32b | 64.61 | 48.61 |
| Fireworks AI | - | qwen3-vl-30b | 62.97 | 52.76 |
| Amazon Bedrock | US | gpt-oss-20b | 61.3 | 40.03 |
| Amazon Bedrock | US | qwen3-32b | 45.41 | 27.41 |
| OpenAI | - | gpt-5-mini | 46.93 | 33.49 |
| Amazon Bedrock | US | gpt-oss-120b | 43.25 | 33.41 |
| OpenAI | - | gpt-5.1-codex-mini | 40.7 | 29.97 |
| Fireworks AI | - | gpt-oss-120b | 60.56 | 34.66 |
| Amazon Bedrock | Tokyo | qwen3-coder-30b | 63.77 | 44.47 |
| Amazon Bedrock | US | qwen3-coder-30b | 23.59 | 17.72 |
| Fireworks AI | - | gpt-oss-20b | 29.4 | 23.02 |
| Local | Mincoding | qwen3-14b | 29.82 | 21.94 |

**정리:**
- OpenAI gpt-5.4-nano는 인코딩 TPS가 10명(46.24) → 30명(12.96)으로 **72% 급락** — 대규모 동시요청에 취약
- Amazon Bedrock Tokyo gpt-oss-20b는 인코딩 TPS도 전 항목 최상위 유지

---

## 6. Amazon Bedrock: Tokyo vs US 리전 비교

> **서울·오사카 리전을 사용하지 않는 이유:** Amazon Bedrock 서울(ap-northeast-2) 리전과 오사카(ap-northeast-3) 리전은 본 벤치마크에서 테스트한 모델(gpt-oss-20b, gpt-oss-120b, qwen3 계열 등)을 제공하지 않는다. 해당 모델들을 지원하는 리전 중 한국에서 지리적으로 가장 가까운 곳이 **Tokyo(ap-northeast-1)** 리전이므로, 이를 기준 리전으로 채택했다.

동일 모델 기준 Tokyo 리전이 전반적으로 높은 TPS를 보이며, 비용도 소폭 높다.

| Model | 지표 | Tokyo | US | Tokyo 우위 |
|---|---|---|---|---|
| gpt-oss-20b | 디코딩 TPS (10명) | 151.86 | 104.61 | **+45.2%** |
| gpt-oss-20b | 디코딩 TPS (30명) | 135.67 | 89.62 | **+51.4%** |
| gpt-oss-20b | Input $/1M | $0.08 | $0.07 | -14.3% (비쌈) |
| gpt-oss-120b | 디코딩 TPS (10명) | 138.04 | 78.87 | **+75.0%** |
| gpt-oss-120b | 디코딩 TPS (30명) | 109.47 | 59.89 | **+82.8%** |
| qwen3-32b | 디코딩 TPS (10명) | 95.04 | 79.47 | **+19.6%** |
| qwen3-32b | 디코딩 TPS (30명) | 73.14 | 64.58 | **+13.2%** |
| qwen3-coder-30b | 디코딩 TPS (10명) | 116.81 | 56.48 | **+106.8%** |
| qwen3-coder-30b | 디코딩 TPS (30명) | 65.3 | 19.43 | **+236.1%** |

**정리:**
- **qwen3-coder-30b**는 Tokyo vs US 격차가 가장 크며, US 리전에서 30명 동시요청 시 TPS가 19.43으로 급격히 저하됨
- **gpt-oss-20b/120b**는 Tokyo 리전에서 압도적으로 높은 성능을 보이며, 한국 서비스 대상으로는 Tokyo 리전이 유리

---

## 7. 동시 요청 증가에 따른 디코딩 TPS 저하율

10명 → 30명 동시요청 증가 시 디코딩 TPS 감소율:

| Provider | Model | Region | 10명 TPS | 30명 TPS | 감소율 |
|---|---|---|---|---|---|
| OpenAI | gpt-5.4-nano | - | 89.12 | 83.02 | **6.8%** |
| OpenAI | gpt-5-mini | - | 57.71 | 53.37 | **7.5%** |
| Amazon Bedrock | gpt-oss-20b | Tokyo | 151.86 | 135.67 | 10.7% |
| Amazon Bedrock | gpt-oss-20b | US | 104.61 | 89.62 | 14.3% |
| OpenAI | gpt-5.1-codex-mini | - | 68.63 | 58.83 | 14.3% |
| Amazon Bedrock | qwen3-32b | US | 79.47 | 64.58 | 18.7% |
| Amazon Bedrock | gpt-oss-120b | Tokyo | 138.04 | 109.47 | 20.7% |
| Amazon Bedrock | qwen3-32b | Tokyo | 95.04 | 73.14 | 23.0% |
| Amazon Bedrock | gpt-oss-120b | US | 78.87 | 59.89 | 24.1% |
| Fireworks AI | qwen3-vl-30b | - | 92.25 | 68.04 | 26.2% |
| OpenAI | gpt-5-nano | - | 106.24 | 70.8 | 33.4% |
| Fireworks AI | gpt-oss-120b | - | 77.52 | 51.58 | 33.5% |
| Fireworks AI | gpt-oss-20b | - | 47.18 | 30.54 | 35.3% |
| Local | qwen3-14b | Mincoding | 22.68 | 13.68 | 39.7% |
| Amazon Bedrock | qwen3-coder-30b | Tokyo | 116.81 | 65.3 | 44.1% |
| Amazon Bedrock | qwen3-coder-30b | US | 56.48 | 19.43 | **65.6%** |

**정리:**
- **가장 안정적**: OpenAI gpt-5.4-nano(6.8%), gpt-5-mini(7.5%) — 부하 증가 시 TPS 저하 최소
- **가장 불안정**: Amazon Bedrock US qwen3-coder-30b(65.6%) — 30명 동시요청 시 성능이 약 1/3 수준으로 급락
- Amazon Bedrock Tokyo qwen3-coder-30b도 44.1% 감소하여 고부하 환경에 부적합

---

## 8. 가성비(비용 대비 성능) 분석

> 가성비 지수 = 디코딩 TPS(10명) ÷ (Input + Output 단가 합계)  
> (단, Local은 API 비용 없어 제외, 비용 'X'인 항목 제외)

| 순위 | Provider | Model | Region | 가성비 지수 | VL |
|---|---|---|---|---|---|
| 1 | Amazon Bedrock | gpt-oss-20b | Tokyo | **345.1** | X |
| 2 | Amazon Bedrock | gpt-oss-20b | US | 282.7 | X |
| 3 | OpenAI | gpt-5-nano | - | 236.1 | O |
| 4 | Amazon Bedrock | gpt-oss-120b | Tokyo | 151.7 | X |
| 5 | Amazon Bedrock | qwen3-coder-30b | Tokyo | 128.4 | X |
| 6 | Fireworks AI | gpt-oss-20b | - | 127.5 | X |
| 7 | Fireworks AI | qwen3-vl-30b | - | 123.0 | **O** |
| 8 | Amazon Bedrock | qwen3-32b | US | 106.0 | X |
| 9 | Amazon Bedrock | gpt-oss-120b | US | 105.2 | X |
| 10 | Amazon Bedrock | qwen3-32b | Tokyo | 104.4 | X |
| 11 | Fireworks AI | gpt-oss-120b | - | 103.4 | X |
| 12 | Amazon Bedrock | qwen3-coder-30b | US | 75.3 | X |
| 13 | OpenAI | gpt-5.4-nano | - | 61.5 | O |
| 14 | OpenAI | gpt-5.1-codex-mini | - | 30.5 | O |
| 15 | OpenAI | gpt-5-mini | - | 25.6 | O |

**정리:**
- **텍스트 전용 최고 가성비**: Amazon Bedrock Tokyo gpt-oss-20b (지수 345.1)
- **VL 지원 최고 가성비**: OpenAI gpt-5-nano (지수 236.1) — 이미지분석 TPS도 전체 1위
- **VL 지원 중 가성비 2위**: Fireworks AI qwen3-vl-30b (지수 123.0) — OpenAI 대비 약 49% 저렴한 단가

---

## 9. 모델별 종합 평가

### 추천 모델

> Amazon Bedrock Tokyo 리전 및 OpenAI, Local 모델.

| Provider | Region | Model | Output ($/1M) | 디코딩 TPS (10명) | 디코딩 TPS (30명) | TPS 저하율 | 가성비 지수 | VL | 판정 | 요약 |
|---|---|---|---|---|---|---|---|---|---|---|
| Amazon Bedrock | Tokyo | gpt-oss-20b | $0.36 | **151.86** | **135.67** | 10.7% | **345.1** | X | ★★★★★ | 속도·가성비 전체 1위, 단가도 합리적. 텍스트 기본 선택 |
| OpenAI | - | gpt-5-nano | $0.40 | 106.24 | 70.8 | 33.4% | **236.1** | **O** | ★★★★★ | 이미지분석 TPS 1위, VL 중 최저 단가. VL 기본 선택 |
| Amazon Bedrock | Tokyo | gpt-oss-120b | $0.73 | 138.04 | 109.47 | 20.7% | 151.7 | X | ★★★★☆ | TPS 2위, 단가 20b의 2배. 더 높은 품질 필요 시 차선택 |
| Amazon Bedrock | Tokyo | qwen3-coder-30b | $0.73 | 116.81 | 65.3 | 44.1% | 128.4 | X | ★★★★☆ | 저부하 코딩 특화 우수, 단가 합리적. 고부하 TPS 급락 주의 |
| Amazon Bedrock | Tokyo | qwen3-32b | $0.73 | 95.04 | 73.14 | 23.0% | 104.4 | X | ★★★☆☆ | 동단가 gpt-oss-120b 대비 TPS·가성비 열위. Qwen3 필수 시에만 |
| OpenAI | - | gpt-5.4-nano | $1.25 | 89.12 | 83.02 | **6.8%** | 61.5 | **O** | ★★★☆☆ | 디코딩 고부하 가장 안정, 단가 높음. 인코딩 TPS 72% 급락 주의 |
| OpenAI | - | gpt-5.1-codex-mini | **$2.00** | 68.63 | 58.83 | 14.3% | 30.5 | **O** | ★★★☆☆ | 최고 단가 대비 TPS 하위. 코딩+VL 특수 요건에만 |
| OpenAI | - | gpt-5-mini | **$2.00** | 57.71 | 53.37 | **7.5%** | 25.6 | **O** | ★★★☆☆ | 고부하 안정성 2위이나 최고 단가·최하 가성비 |
| Local | Mincoding | qwen3-14b | 없음 | 22.68 | 13.68 | 39.7% | - | X | ★★★☆☆ | API 비용 없음, TPS 최하위. 개발·테스트 전용 |

### 비추천 모델

> Amazon Bedrock US 리전은 Tokyo 대비 TPS가 최대 65% 낮으면서 비용 절감 폭이 미미하다. Fireworks AI는 동일 단가 Bedrock 대비 TPS가 절반 이하다. 모두 선택할 실질적 근거가 없다.

| Provider | Region | Model | Output ($/1M) | 디코딩 TPS (10명) | 디코딩 TPS (30명) | TPS 저하율 | 가성비 지수 | VL | 판정 | 요약 |
|---|---|---|---|---|---|---|---|---|---|---|
| Amazon Bedrock | US | gpt-oss-20b | **$0.30** | 104.61 | 89.62 | 14.3% | 282.7 | X | ★★☆☆☆ | 단가는 최저이나 Tokyo 대비 TPS 31% 낮음. 비용 이점 미미 |
| Amazon Bedrock | US | qwen3-32b | $0.60 | 79.47 | 64.58 | 18.7% | 106.0 | X | ★★☆☆☆ | Tokyo 동일 모델 대비 TPS·가성비 모두 열위 |
| Amazon Bedrock | US | gpt-oss-120b | $0.60 | 78.87 | 59.89 | 24.1% | 105.2 | X | ★★☆☆☆ | Tokyo 대비 TPS 43% 하락, 절감 폭 미미 |
| Fireworks AI | - | qwen3-vl-30b | $0.60 | 92.25 | 68.04 | 26.2% | 123.0 | **O** | ★★☆☆☆ | VL 저단가 대안이나 OpenAI gpt-5-nano에 가성비 열위 |
| Fireworks AI | - | gpt-oss-120b | $0.60 | 77.52 | 51.58 | 33.5% | 103.4 | X | ★★☆☆☆ | 동단가 Bedrock Tokyo 대비 가성비 32% 낮음 |
| Amazon Bedrock | US | qwen3-coder-30b | $0.60 | 56.48 | 19.43 | **65.6%** | 75.3 | X | ★☆☆☆☆ | 고부하 안정성 전체 최악, 단가도 불리. 사실상 사용 불가 |
| Fireworks AI | - | gpt-oss-20b | **$0.30** | 47.18 | 30.54 | 35.3% | 127.5 | X | ★☆☆☆☆ | 단가는 최저이나 동단가 Bedrock US 대비 TPS 55% 낮음 |

