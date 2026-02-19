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

### Arrow (→) Notation

Used extensively for:
- **Logical implication**: `"학습 데이터 = 테스트 데이터 가정 → 실제 환경에서 성능 저하"`
- **Process step result**: `"3D 공간 재구성 → 3D Reconstruction"`
- **Trade-off**: `"Block Size 증가 → 정확도 향상, 실시간성 저하"`
- **Derived conclusion**: `"→ Domain Adaptation은 필수적"`

Arrows always imply "therefore" or "which leads to." They are NOT decorative.

### Structuring Content Within a Slide

Use the 3-level hierarchy (section header → main bullet → sub-bullet) to organize content. The structure should emerge naturally from the content's logic, not from formatting conventions.

### Bullet Length and Density

- Main bullets: 15-40 Korean characters (1-2 lines on screen)
- Sub-bullets: 10-25 characters (1 line)
- Per slide: 3-6 main bullets, 0-3 sub-bullets per main bullet
- Total readable lines: 8-15 per content slide
- Total word count: 150-300 words per content slide

**This is dense.** Don't fear information density. Sparse slides with 2-3 shallow bullets waste the audience's time and don't match real Slide Forge presentations.

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

## Visual-Text Relationship

### Layout Rule

**Top = Text (40-60%), Bottom = Visuals (40-60%).** This is the dominant pattern across all Slide Forge presentations.

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
