# Slide Forge — Presentation Content & Style Guide

Comprehensive content patterns for lab-style technical presentations. Originally derived from reference materials of the Sustainable Design and Manufacturing Laboratory, Sungkyunkwan University.

**This guide prioritizes content quality over visual decoration.** A slide with perfect branding but generic text is worse than a plain slide with authentic, specific content.

---

## Table of Contents

1. [Writing Style](#writing-style)
2. [Korean/English Mixing](#koreanenglish-mixing)
3. [Information Hierarchy](#information-hierarchy)
4. [Slide Structure Patterns](#slide-structure-patterns)
5. [Visual-Text Relationship](#visual-text-relationship)
6. [Typography](#typography)
7. [Color Palette](#color-palette)
8. [Authenticity Markers](#authenticity-markers)
9. [Anti-Patterns (What NOT to Do)](#anti-patterns)
10. [PptxGenJS Quick Reference](#pptxgenjs-quick-reference)

---

## Writing Style

### Sentence Endings: Nominalized (명사형 종결)

The single most important writing rule. Every bullet point ends with a **Sino-Korean noun or nominalized form**. Never use polite sentence endings (-습니다, -합니다, -입니다) or literary endings (-하였다, -이다).

**Catalog of common ending nouns:**

| Ending | Meaning | Example |
|--------|---------|---------|
| ~수행 | execution | "로봇 동역학 모델 성능 개선 작업 수행" |
| ~구축 | construction | "RMS 데이터 분석 및 가공 프로세스 구축" |
| ~확인 | confirmation | "Job_name 값 변동 확인" |
| ~개발 | development | "통합 이상탐지 프레임워크 개발" |
| ~학습 | training | "ML/DL 기반 모델 구축 및 학습" |
| ~진행 | proceeding | "파라미터 조합 탐색 진행" |
| ~필요 | necessity | "토크 예측 정확도의 개선 필요" |
| ~가능 | possibility | "실시간에 가까운 이상탐지 가능" |
| ~존재 | existence | "하중 효과를 반영하지 못한 한계점 존재" |
| ~분석 | analysis | "Clamp-to-Clamp 단위 동작 패턴 분석" |
| ~적용 | application | "정규화(Normalization) 적용" |
| ~고도화 | advancement | "MDPS 열화 예측 알고리즘 고도화" |
| ~추출 | extraction | "핵심 열화 물리 특징 인자 도출" |
| ~불가 | impossibility | "85% 이상의 성능 구현 불가" |
| ~저하 | degradation | "Block Size 증가 시 실시간성 저하" |
| ~선정 | selection | "Top-k 패턴 선정" |
| ~도입 | introduction | "Physics Model & DL Hybrid 접근법 도입" |

**Exception:** Sub-bullets that explain reasoning may use slightly more natural Korean, but still avoid polite endings:
```
→ 차이점: 구조적 제약으로 기존 물리 법칙 준수, 손실함 제약으로 추가 강화
→ 대부분 큰 잔차의 지배항으로 작용, 마찰관련 규칙이 나타남
```

**✅/❌ Examples:**
```
✅ "진동 데이터 기반 이상 탐지 모델 구축"          ← ends with 구축 (noun)
✅ "하중 효과를 반영하지 못한 한계점 존재"          ← ends with 존재 (noun)
✅ "Block Size 증가 시 정확도 향상, 실시간성 저하"   ← ends with 저하 (noun)

❌ "진동 데이터 기반 이상 탐지 모델을 구축하였습니다"  ← polite ending
❌ "이상 탐지 모델을 개발하여 적용함"                ← too literary
```

### Arrow (→) Notation — Use Sparingly

Arrows always imply "therefore" or "which leads to." They are **NOT** decorative and must **NOT** appear on every sub-bullet.

**Allowed uses:**
- **Derived conclusion** (at end of bullet group): `"→ Domain Adaptation은 필수적"`
- **Logical implication** (within a sentence): `"학습 데이터 = 테스트 데이터 가정 → 실제 환경에서 성능 저하"`
- **Trade-off result**: `"Block Size 증가 → 정확도 향상, 실시간성 저하"`
- **Essential "So what?"**: interpretation after presenting data

**Use `-` (not `→`) for:** examples, enumerations, definitions, specifications, and any sub-bullet that doesn't have a "therefore" relationship.

**❌ BAD — arrow on every sub-bullet (the #1 mistake):**
```
– 산업용 로봇 조립 라인에서 동일 카테고리 부품이 수십 개 공존
  → 예: T-LESS 데이터셋 — 동일 형상 산업 부품 30종
  → 카테고리 인식만으로는 "어느 물체"인지 특정 불가
– 기존 6DoF 포즈 추정 파이프라인의 한계
  → 포즈 추정은 "이 물체가 무엇인가"에 답하지만 "어디에 있어야 하는가"에는 무답
  → 동일 외형 부품이 위치만 다를 때, 비전 단독으로 인스턴스 구분 불가
```
→ 문제: 6개 서브불릿 전부 `→`를 사용. 예시도 →, 사실 서술도 →, 결론도 →로 구분이 불가.

**✅ GOOD — arrows only for conclusions:**
```
– 산업용 로봇 조립 라인에서 동일 카테고리 부품이 수십 개 공존
  - 예: T-LESS 데이터셋 — 동일 형상 산업 부품 30종, 장면당 평균 7.5개 인스턴스
  → 카테고리 인식만으로는 "어느 물체"인지 특정 불가
– 기존 6DoF 포즈 추정 파이프라인의 한계
  - 포즈 추정은 "이 물체가 무엇인가"에 답하지만 "어디에 있어야 하는가"에는 무답
  - 동일 외형 부품이 위치만 다를 때, 비전 단독으로 인스턴스 구분 불가
  → 인스턴스 식별 실패 → 잘못된 부품 피킹 → 라인 정지 비용 발생
```
→ 핵심: 각 불릿 그룹의 마지막에만 `→`로 결론. 나머지 서브불릿은 `-`로 사실/예시 나열.

**Self-check:** `→`를 제거해도 의미가 변하지 않으면, 그 자리에 `-`를 써야 한다.

### Structuring Content Within a Slide

Use the 3-level hierarchy (section header → main bullet → sub-bullet) to organize content. The structure should emerge naturally from the content's logic, not from formatting conventions.

```
[Section Header — dark bar with left accent]           ← Level 1: 16-18pt bold
– Main bullet: 핵심 내용 명사구                          ← Level 2: 12-14pt, dash prefix
  - Sub-bullet: 세부 사항, 예시, 사양                    ← Level 3: 10-12pt, detail/example
  → Sub-bullet: 결론 or 함의 (sparingly)                ← Level 3: 10-12pt, conclusion only
    (1) Numbered detail when sequential                 ← Level 3 variant
```

### Bullet Length and Density

- Main bullets: 15-40 Korean characters (1-2 lines on screen)
- Sub-bullets: 10-25 characters (1 line)
- Per slide: 3-6 main bullets, 0-3 sub-bullets per main bullet
- Total readable lines: 8-15 per content slide
- Total word count: 150-300 words per content slide

**This is dense.** Don't fear information density. Sparse slides with 2-3 shallow bullets waste the audience's time and don't match real Slide Forge presentations.

### Audience Perspective (청중 관점 서술)

Write as if the audience has **zero prior context** about your project. You developed this code — the audience did not. Every technical name must earn its place by being explained.

```
❌ "T_CLAMP 신호와 BACK_POS를 활용한 이상 탐지"
   → 듣는 사람은 T_CLAMP, BACK_POS가 뭔지 모름

✅ "클램핑 토크(T_CLAMP)와 후진 위치(BACK_POS) 신호를 활용한 이상 탐지"
   → 변수가 무엇을 의미하는지 먼저 설명한 뒤 괄호로 원래 이름 표기

❌ "get_features() 함수로 27개 피처 추출 후 train_model()로 학습"
   → 코드 리뷰가 아닌 발표임. 함수명은 청중에게 무의미

✅ "잔차 기반 11개 + 동역학 기반 16개, 총 27개 피처를 추출하여 모델 학습"
   → 코드 구현이 아닌 내용 자체를 설명

❌ "pos, spd, trq 데이터를 입력으로 사용"
   → 축약 변수명만으로는 무슨 데이터인지 알 수 없음

✅ "위치(pos), 속도(spd), 토크(trq) 데이터를 입력으로 사용"
   → 의미를 먼저, 약어를 괄호에
```

Rules:
- **변수/신호명**: 처음 등장 시 반드시 의미 설명 + 괄호로 원래 이름 — `"클램핑 토크(T_CLAMP)"`, `"위치(pos)"`
- **함수/클래스명**: 발표에서는 절대 사용하지 않음. 그 함수가 **하는 일**을 설명 — `"피처 추출"` not `"get_features()"`
- **약어/축약어**: 청중이 모를 수 있는 약어는 풀어서 설명 후 사용 — `"마할라노비스 거리(MCD)"` then `"MCD"`
- **Self-check**: "이 이름을 처음 보는 사람이 이 문장만으로 이해할 수 있는가?" → No면 설명 추가

---

## Korean/English Mixing

English makes up approximately 30-40% of text by word count on technical slides. The mixing follows specific patterns:

### Pattern A: English Term with Korean Particles Attached

Korean grammar particles attach directly to English words — no space between English word and particle:

```
"Domain Adaptation을 적용하지 않았을 경우"        (을 = object particle)
"VoxelMap에 Vision AI 모델을 적용하여"           (에 = locative particle)
"Bounding Box로 탐지"                          (로 = instrumental particle)
"Twinverse 내 객체들을 개별 이미지로 렌더링"       (내 = within)
"JSON 형태로 점수를 산출"                        (형태로 = in the form of)
"Rendering을 통한 객체 분할"                     (을 = object particle)
"Threshold를 초과할 경우 이상으로 판정"            (를 = object particle)
```

### Pattern B: Korean Concept + English in Parentheses

First introduction of a concept uses Korean first, English clarification in parentheses:

```
"의미 정보(Semantic Embedding)"
"기반 메모리(Semantic Memory)"
"위치 추정(Object Localization)"
"이상 탐지(Anomaly Detection)"
"구조화된 출력(Structured Output)"
"최소 공분산 행렬(Minimum Covariance Determinant)"
"마찰계수 조작(Signal Manipulation & Injection)"
```

After the first mention, use the English term alone.

### Pattern C: English Acronyms Inline Without Translation

Established technical acronyms are used directly in Korean text without translation:

```
"LSTM 기반 Pos2Trq과 같은 Pilot 모델"
"RMS 데이터 분석"
"ML/DL 기반 모델 구축"
"SOTA 방법론 탐색"
"MCD 기반 이상 탐지"
"PCA Whitening 적용"
"MDPS 열화 예측"
```

Only define an acronym if the specific audience is unlikely to know it. Common ones (LSTM, PCA, MCD, RMS, ML/DL) need no definition.

### Pattern D: Full English for Framework/Model/Product Names

```
"OK-Robot Framework"
"Agentic Object Mapping"
"Grid Search"
"Robust Scaling"
"Block Averaging"
"Permutation Importance"
"Catastrophic Forgetting"
```

### Pattern E: Variable/Parameter Names Preserved As-Is

```
"pos, spd, trq, job_name"
"Block Size = 64 → 6.4초"
"R² 예측 정확도 J1: 93.5%"
"det(Cov)"
"e.g. MODEL-4 w/ load 구간"
"F_z(Vertical Load) 수직 하중"
```

### Pattern F: Academic Citations (English)

At slide bottom in small font:
```
"H. Li, Sun, T., Jiang, H., et al., 2024, ..."
"Lu, P. et al. (2024). 'Ok-robot: What really matters...' arXiv preprint"
"Lopez de Calle, K., et al. (2019). 'A context-aware oil debris-based...' Energies."
```

---

## Information Hierarchy

### Level 1: Section Header

A bold header, often in a dark-filled rectangular bar with a vertical accent on the left side. Persists across multiple slides in the same section.

```
▌로봇 역동역학 기반 이상 모사 모델(RIDGE) 개발의 필요성
▌SOTA 방법론 탐색 및 학습
▌2차년도 연구 전체 아키텍처
```

The `▌` represents a visual vertical accent bar (dark blue or navy rectangle at the left edge of the header).

### Level 2: Main Bullets

Prefixed with a dash `–` (en-dash). These carry the core information.

```
– OK-Robot Framework
– 비전 언어 융합 기반 3D 공간 상 객체 위치 특정
– Selective Rendering을 통한 객체 분할 및 VLM 기반 Object Localization
– 진동 데이터 기반 이상 탐지 모델 구축
```

### Level 3: Sub-Bullets

Multiple formats used, all indented under a main bullet:

**Arrow sub-bullets** (for conclusions/implications):
```
→ 토크 예측 오차(Payload effect) 확인
→ 실시간에 가까운 이상탐지 가능
→ Domain Adaptation은 필수적
```

**Numbered sub-items** (for sequential steps):
```
(1) Selective Rendering: 시야 내 모든 객체를 개별 이미지로 렌더링
(2) VLM 기반 Object Localization: 각 객체에 매칭 점수 산출
(3) 최고점 객체를 최종 선정
```

**Indented dashes** (for additional detail):
```
  - 노이즈 제거(Low-pass Filter, 5 kHz)
  - 특징 추출: RMS, Peak, Kurtosis, FFT 스펙트럼
  - 정규화(Normalization) 적용
```

### Cross-Slide Navigation

For multi-slide sequences, add a persistent process bar at the bottom showing the current step:

```
[데이터 수집] → [패턴 분석] → [모델 학습] → [이상 판정]
                  ^^^^^^^^ (highlighted = current slide)
```

---

## Slide Structure Patterns

### Pattern: Literature Review Slide

For reviewing prior work or papers:

```
Title: "기계 건강 상태 진단 선행 연구 리뷰"

– 운전 조건 변동이 열화 신호를 가리는 교란 원인으로 작용
– 각 운전 영역별 데이터를 분리하여 개별 열화 지표 생성
  → 운전 조건 인식 후 조건별 분리 분석이 효과적

본 연구의 의의:
  → 다차종 확장성 관점에서 Driving Context 인식이 핵심

Citation at bottom: "Lopez de Calle, K., et al. (2019). Energies."
Visual: Paper's key figure/chart reproduced at bottom
```

### Pattern: Methodology Slide

```
Title: "MCD 기법 기반 이상 탐지 프로세스"

– (1) 정상 데이터로 MCD 모델 학습
  → Robust한 공분산 행렬 추정
– (2) 임계값 설정 (Chi-square 분포 기반)
  → 신뢰 구간 99.7% 기준
– (3) 신규 데이터의 마할라노비스 거리 산출
  → 임계값 초과 시 이상으로 판정

Visual: Process flow diagram with pastel boxes and arrows
```

### Pattern: Results Slide

```
Title: "MCD 기반 이상 탐지 성능 평가"

– 대상: CNC 가공기 스핀들 진동 데이터 (25.05.27~25.06.22)
– 정상 데이터 1,198,500건(96.3%), 이상 데이터 46,500건(3.7%)
– 주요 결과:
  → Precision: 92.3%, Recall: 88.0%, F1-Score: 90.1%
  → Joint 1/3/6에 대해 높은 정확도 (R² > 93%)
  → Joint 2/4 정확도 상대적 저조 (R² = 23.2%) → 개선 필요
– 하중 효과를 반영하지 못한 한계점 존재

Visual: Bar chart (performance metrics) + Table (per-joint R² values)
```

### Pattern: Future Works Slide

```
Title: "향후 연구 계획"

① 딥러닝 기반 모델 비교 실험
   – LSTM, Autoencoder 등 적용 및 성능 비교
   – 하이퍼파라미터 최적화를 통한 정확도 향상

② 다중 센서 융합(Multi-Sensor Fusion)
   – 온도, 전류 등 추가 센서 데이터 결합
   – Feature-level fusion 및 Decision-level fusion 비교

③ 실시간 모니터링 시스템 구축
   – Edge Computing 기반 실시간 판정 파이프라인
   – CPU inference 최적화 (목표: < 100ms/block)

[Visual: Timeline with month-based milestones]
```

### Pattern: Overview/Progress Slide

Uses "(지난 보고)" prefix for previously reported content, Gantt chart for timeline:

```
Title: "연구 진행 상황"

(지난 보고) 물리 기반 MDPS 예측을 위한 알고리즘 구현
– 단순화 토크 모델 기반 Driving Context Conditioning 검증 완료
– 1차년도 연구 성과 리뷰 및 2차년도 방향 설정

(금주 보고) 전이학습 기반 차종별 맞춤형 토크 예측 모델 개발
– Domain Adaptation 기법 적용
– RS4(G90) 데이터 기반 검증 진행 중

[Visual: Gantt chart with current milestone highlighted in green]
```

---

## Inter-Slide Transitions & Slide-Level Message

### Every Slide Needs a "So What?"

Each content slide must make a **point**, not just present information. If the audience asks "So what?" after reading the slide, the answer must be findable IN the slide.

```
❌ BAD (fact-listing, no argument):
  T-LESS 데이터셋 선정 이유: 동일 형상 산업 부품 30종의 인스턴스 식별 난제
  → 실제 공장 조립 라인과 유사한 다중 동일 부품 배치 장면
  → BOP Challenge 공식 벤치마크 — 6DoF 포즈 추정 커뮤니티 표준

→ 문제: 사실만 나열. "그래서 뭐?" 에 대한 답이 없음.
  이 데이터셋을 선택한 것이 결과에 어떤 의미가 있는지 알 수 없음.

✅ GOOD (fact + argument):
  T-LESS 데이터셋 선정: "가장 어려운 조건에서 검증해야 의미가 있다"
  - 동일 형상 산업 부품 30종 — 실제 공장 조립 라인의 난제를 그대로 재현
  - 장면당 평균 7.5개 인스턴스, 최대 3개 동일 카테고리 공존
  → 외형 유사도가 극단적으로 높아, 비전 단독 방법의 한계가 가장 극명하게 드러나는 환경
  → 이 벤치마크에서 유의미한 개선이면, 실제 배포 환경에서도 효과를 기대할 수 있는 근거
```

### Inter-Slide Connections

Slides must not feel like independent Wikipedia articles. Each slide (except TOC) must connect to its predecessor.

**Connection types (at least one per slide):**
- **Implicit bridge**: subtitle or first bullet naturally continues the previous slide's thread.
- **Explicit bridge**: direct reference — "Slide 03에서 확인된 54.6%p 격차를 해소하기 위한 접근"
- **Question-answer chain**: previous slide raises a question/problem, current slide answers it.

```
❌ BAD (no connection — slides feel independent):
  Slide 03 subtitle: "식별 가능성 격차(Identifiability Gap) 정량화"
  Slide 04 subtitle: "Digital Twin(DT)을 기하 사전 정보(Geometric Prior)로 활용"

→ 문제: Slide 03이 격차를 보여줬는데, Slide 04가 왜 DT인지 연결이 없음.

✅ GOOD (natural flow):
  Slide 03 subtitle: "식별 가능성 격차(Identifiability Gap) 정량화"
  Slide 04 subtitle: "Slide 03의 격차 해소 — Digital Twin(DT) 기하 사전 정보 활용"
  또는 첫 불릿에서: "비전 단독 54.6%p 격차(Slide 03) → 추가 정보원이 필수"
```

---

## Visual-Text Relationship

### Layout Rule

**Top = Text (40-60%), Bottom = Visuals (40-60%).** This is the dominant pattern across all Slide Forge presentations.

```
┌──────────────────────────────────┐
│ Slide Title (20-24pt bold)       │
│                                  │
│ – Bullet text                    │  ← Upper 40-60%: TEXT
│   → Sub-bullet                   │
│ – More bullets                   │
│                                  │
│ ┌──────────┐  ┌──────────┐      │  ← Lower 40-60%: VISUALS (1-3)
│ │  Chart    │  │  Diagram  │     │
│ │           │  │           │     │
│ └──────────┘  └──────────┘      │
└──────────────────────────────────┘
```

This is the **only** default layout. Use left-right splits only for side-by-side comparison where it's clearly better.

When 2-3 visuals are present, arrange them **side-by-side horizontally** in the lower area.

### Visual Types by Purpose

| Purpose | Visual Type | Real Examples |
|---------|------------|---------------|
| System design | Architecture/pipeline diagram | 3-stage pipeline, model architecture, data flow |
| Experimental results | Line/bar/scatter plots, ROC curves | Time-series data, F1 scores, residual distributions |
| Parameter comparison | Tables with navy/purple header | R² per joint, feature importance rankings |
| Mathematical model | Rendered equations | τ = M(q)q̈ + C(q,q̇)q̇ + G(q) + f(q) |
| Real-world context | Photos, screenshots | Robot arms, hardware, JSON output, UI |
| Process explanation | Flow diagram with pastel boxes | Step-by-step methodology, data processing pipeline |

### Annotation Rules

- Charts include Korean labels with English terms inline
- Highlight regions of interest with red boxes/circles
- Add specific numeric annotations directly on chart data points
- Citations for reproduced figures at slide bottom (8-9pt gray)

### Diagram Style

- Rounded rectangles with pastel fills (`B4C7E7`, `D5BDDB`, `C5E0B4`, `FFD699`)
- Arrows: 3-4pt, light blue (`5B9BD5`)
- Labels inside boxes: centered, 10-12pt
- Color-code different phases/components

---

## Typography

### Font Families

| Context | Font |
|---------|------|
| Korean text | Malgun Gothic (맑은 고딕) |
| English text | Calibri |
| Equations | Times New Roman |
| Code/variables | Consolas |

### Size Hierarchy

| Element | Size (pt) | Weight |
|---------|-----------|--------|
| Slide title | 20-24 | Bold |
| Section header (bar) | 16-18 | Bold |
| Main bullet | 12-14 | Regular |
| Sub-bullet | 10-12 | Regular |
| Table cell | 9-11 | Regular |
| Chart labels | 8-10 | Regular |
| Citations/footnotes | 8-9 | Regular |

These are intentionally smaller than typical "presentation" sizes. Slide Forge presentations prioritize information density over readability-at-distance.

---

## Color Palette

### Core Colors

| Role | Hex | Usage |
|------|-----|-------|
| **Navy** (primary) | `1B3765` | Titles, headers, emphasis |
| **Light blue** | `5B9BD5` | Arrows, dividers, secondary |
| **Black** | `000000` | Body text |
| **Dark gray** | `666666` | Captions, secondary text |
| **Body gray** | `333333` | Sub-bullet text |

### Background

| Role | Hex |
|------|-----|
| Slide background | `FFFFFF` |
| Subtle contrast | `F5F5F5` |
| Section header bar | `E7E6E6` or `1B3765` |

### Data Visualization

| Color | Hex | Usage |
|-------|-----|-------|
| Navy | `1B3765` | Primary series |
| Light blue | `5B9BD5` | Secondary series |
| Purple | `7030A0` | Table headers, tertiary |
| Coral/Red | `C84545` | Alerts, anomalies |
| Green | `00B050` | Positive indicators |
| Orange | `FFA500` | Highlights |
| Yellow | `FFC000` | Key findings |

### Pastel Fills (for diagrams/process boxes)

| Color | Hex |
|-------|-----|
| Pastel blue | `B4C7E7` |
| Pastel purple | `D5BDDB` |
| Pastel green | `C5E0B4` |
| Pastel orange | `FFD699` |

---

## Authenticity Markers

What separates real Slide Forge presentations from AI-generated ones:

### Specificity

- **Exact numbers, not round**: `"R² = 93.5%"` not `"약 90%"`
- **Specific date ranges**: `"25.05.27~25.06.22"` not `"최근 데이터"`
- **Real system identifiers**: `"MODEL-4 w/ load"`, `"GP25"`, `"RS4(G90)"`
- **Actual signal names**: `"T_CLAMP"`, `"BACK_POS"`, `"SPEED_SET"`, `"pos, spd, trq"`
- **Software versions**: `"Python 3.12.11"`, `"PyTorch 2.9.0+cpu"`
- **Hardware specs**: `"CPU inference (Ryzen 7 8845HS) 및 Mini PC"`

### Honest Imperfection

- Acknowledge limitations: `"한계점 존재"`, `"개선 필요"`
- Report uneven results: some metrics good, some bad
- Describe trade-offs: `"정확도 향상되지만 실시간성 저하"`
- Mark incomplete work: `"재점도 필요"`, `"검증 진행 중"`

### Domain Depth

- Use jargon appropriate to audience (don't over-explain)
- Selectively define terms: define unusual ones, skip common ones
- Include academic citations with full bibliographic data
- Show actual output: JSON responses, code snippets, raw plots

### Temporal Context

- Reference previous reports: `"(지난 보고)"`, `"1차년도 연구 Review"`
- Gantt charts with progress markers (green highlight = current)
- Cross-slide process bars showing "you are here"

---

## Anti-Patterns

### Text Content

| Don't | Do Instead |
|-------|------------|
| End bullets with -습니다/-합니다 | End with nouns: ~수행, ~구축, ~확인 |
| Write generic placeholder text | Use specific data, names, versions |
| Define every single acronym | Define only unfamiliar ones |
| Use flat bullet lists (all same level) | Use 2-3 level hierarchy (main → sub → detail) |
| Write full sentences as bullets | Write noun-phrase fragments |
| Make all metrics look perfect | Show honest mixed results with limitations |
| Over-explain well-known concepts | Assume appropriate audience knowledge |
| Use "약", "대략", "거의" when exact data exists | Use exact numbers |

### Layout

| Don't | Do Instead |
|-------|------------|
| Left-right text/visual split (default) | Top text, bottom visuals |
| Sparse slides (2-3 bullets) | Dense slides (8-15 lines) |
| Giant font sizes (28-32pt body) | Correct sizes (12-14pt body) |
| Decorative elements, clipart | Functional visuals only |
| Text-only slides | Always include 1-3 visuals |
| Center-aligned body text | Left-align everything |

### Visual

| Don't | Do Instead |
|-------|------------|
| Default chart colors | Slide Forge palette colors |
| Charts without data labels | Annotate specific values |
| Generic stock photos | Real equipment/output screenshots |
| Diagrams without labels | Label every box and arrow |
| Single visual when data demands more | 2-3 visuals side-by-side when appropriate |

### Detailed BAD/GOOD Examples

아래는 AI가 만든 슬라이드에서 반복적으로 나타나는 문제 패턴이다. 하나라도 해당되면 즉시 수정.

**Anti-Pattern 1: 숫자 투하 (Number Dumping)**
```
❌ BAD:
  – 동일 물체 1개: +20.9pp / 2개: +37.8pp / 3+: +56.1pp (Vision 8.2% → DT 64.3%)
  – 평균 24.3pp 우위, Bootstrap 95% CI 모두 양수 → strict dominance 확인

→ 문제: 숫자는 있지만 해석이 없음.
  "pp"가 뭔지, 왜 이 숫자가 중요한지, 청중이 뭘 기억해야 하는지 전혀 모름.

✅ GOOD:
  – 동일 물체가 여러 장면에 등장할수록 DT의 이점이 급격히 증가
    → 1개 등장: +20.9%p / 2개: +37.8%p / 3개 이상: +56.1%p
    → 다중 인스턴스가 많은 실제 환경일수록 DT가 유리한 구조
  – 16개 전 커버리지 수준에서 DT가 Vision 대비 평균 24.3%p 높은 정확도
    → 특정 조건이 아닌 전 구간에서의 일관된 우위 (통계적으로 유의)

→ 핵심: "숫자가 무엇을 의미하는가"를 반드시 한 줄 덧붙인다.
```

**Anti-Pattern 2: 전문용어 폭격 (Jargon Bombardment)**
```
❌ BAD:
  – Bootstrap 95% CI 모두 양수 → strict dominance 확인
  – τ=0.35: Coverage 90.15%, Wrong-Pick 21.51%

→ 문제: Bootstrap CI, strict dominance, τ, Coverage, Wrong-Pick
  — 한 슬라이드에 설명 없는 전문용어가 5개 이상. 개발자 본인만 이해 가능.

✅ GOOD:
  – 부트스트랩 신뢰구간(Bootstrap 95% CI) 분석 결과, 모든 조건에서 DT 우위 확인
    → 통계적으로 "우연이 아닌 구조적 차이"임을 입증
  – 위험 허용 수준(τ) 0.35 기준:
    → 커버리지(판단 가능 비율) 90.15%, 오판율(Wrong-Pick) 21.51%

→ 핵심: 한 슬라이드에 미설명 전문용어가 3개 이상이면 위험 신호.
  모든 영문 용어에 한국어 의미를 먼저 제시.
```

**Anti-Pattern 3: 얇은 슬라이드 (Thin Slide)**
```
❌ BAD:
  불릿 3개 + 서브불릿 3개 = 텍스트 6줄. 나머지는 빈 공간.
  → 슬라이드 상단 30%만 텍스트, 하단은 차트+테이블이지만
    차트/테이블도 설명 없이 던져져 있음.

→ 문제: 청중은 차트를 보고 스스로 해석해야 함. 발표자가 해석을 제공하지 않음.

✅ GOOD:
  불릿 4-6개 + 서브불릿 6-10개 = 텍스트 10-15줄.
  차트/테이블 아래 또는 옆에 핵심 해석 1-2줄 반드시 포함:
  "→ 동일 물체 3개 이상 장면에서 DT가 Vision 대비 7배 이상 정확"

→ 핵심: 시각 자료는 스스로 말하지 않는다. 반드시 해석 문장을 함께 제시.
```

**Anti-Pattern 4: 텍스트 위장 다이어그램 (Text-in-Boxes Disguised as Diagram)**
```
❌ BAD:
  "비교 다이어그램"이라고 하면서 실제로는:
  ┌─────────────────┐         ┌─────────────────┐
  │ ✗ 외형 기반       │   →    │ ✓ 기하 기반       │
  │ 동일 외형 → 구분불가│         │ 공간 정보 → 구분가능│
  │ Acc: 41.4%       │         │ Acc: 77.0%       │
  └─────────────────┘         └─────────────────┘
  → 색상 박스 안에 텍스트를 넣고 화살표로 연결한 것.
    불릿을 박스에 옮겨 담은 것일 뿐, "그림"이 아님.

→ 판별법: 박스 안의 내용을 그대로 불릿으로 옮겨도 정보 손실이 없으면
  그것은 다이어그램이 아니라 장식된 텍스트이다.

✅ GOOD — 진짜 시각 자료의 기준:
  시각 자료는 텍스트로 표현할 수 없는 정보를 전달해야 한다:
  - 데이터 차트: 막대/선/산점도로 수치 간 크기·추이·분포를 비교
  - 프로세스 플로우: 단계 간 분기/합류/피드백 루프를 시각적으로 표현
  - 아키텍처 다이어그램: 모듈 간 데이터 흐름, 입출력 관계
  - 테이블: 다차원 수치 비교 (3개 이상의 항목 × 2개 이상의 메트릭)
  - 어노테이션 이미지: 실제 사진/스크린샷 위에 영역 표시

→ Self-check: "이 그림의 박스 안 텍스트를 불릿으로 옮기면 정보가 줄어드는가?"
  → No면 그림이 아님. 실제 데이터 차트나 구조도로 교체.
```

**Anti-Pattern 5: 화살표 남발 (Arrow Overuse)**
```
❌ BAD:
  – 객체 정확도(object_acc)와 인스턴스 정확도(instance_acc)를 분리 측정
    → object_acc: 올바른 카테고리의 물체를 선택했는가 ("무엇")
    → instance_acc: 올바른 개별 인스턴스를 선택했는가 ("어느 것")
  – 격차 지수(Delta) = 객체 정확도 - 인스턴스 정확도
    → Delta가 클수록 "무엇인지는 알지만 어느 것인지 모르는" 상태
    → 비전 단독 모델의 Delta: 최대 54.6%p — 구조적 한계 노출

→ 문제: 정의/설명에도 `→`를 사용. "object_acc: 올바른 카테고리..." 는 정의이지
  "그러므로"가 아니다. 전부 → 이면 진짜 결론이 어디인지 구분 불가.

✅ GOOD:
  – 객체 정확도(object_acc)와 인스턴스 정확도(instance_acc)를 분리 측정
    - object_acc: 올바른 카테고리의 물체를 선택했는가 ("무엇")
    - instance_acc: 올바른 개별 인스턴스를 선택했는가 ("어느 것")
  – 격차 지수(Delta) = 객체 정확도 - 인스턴스 정확도
    - 비전 단독 모델의 Delta: 최대 54.6%p
    → "무엇인지는 알지만 어느 것인지 모르는" 상태 — 비전만으로는 구조적 한계

→ 핵심: 정의·예시·사양은 `-`, 결론·함의·해석만 `→`.
  슬라이드당 `→` 비율이 50%를 넘으면 남발 의심.
```

**Last Resort — 적합한 시각 자료를 만들 데이터가 정말 없는 경우:**
회색 점선 테두리의 플레이스홀더 박스를 배치하고, 그 안에 "이 자리에 들어갈 시각 자료"를 설명하는 문구를 넣는다.
예: `"※ 실제 실험 데이터 확보 후, Joint별 R² 비교 막대 차트 삽입 예정"`
이것은 가짜 다이어그램을 만드는 것보다 정직하고, 발표자에게 어떤 자료를 준비해야 하는지 명확한 가이드를 제공한다.

---

## PptxGenJS Quick Reference

Hex values (no `#` prefix):

```javascript
// Core
const NAVY = "1B3765";
const LIGHT_BLUE = "5B9BD5";
const WHITE = "FFFFFF";
const OFF_WHITE = "F5F5F5";
const LIGHT_GRAY = "E7E6E6";
const BLACK = "000000";
const DARK_GRAY = "666666";
const BODY_GRAY = "333333";

// Data visualization
const PURPLE = "7030A0";
const CORAL = "C84545";
const GREEN = "00B050";
const ORANGE = "FFA500";
const YELLOW = "FFC000";

// Pastel fills
const PASTEL_BLUE = "B4C7E7";
const PASTEL_PURPLE = "D5BDDB";
const PASTEL_GREEN = "C5E0B4";
const PASTEL_ORANGE = "FFD699";
```
