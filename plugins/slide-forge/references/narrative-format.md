# Narrative Document Format — `narrative-full.md`

This document defines the format for the Storyteller agent's primary output.

---

## Structure

```markdown
# [프레젠테이션 제목]

## 메타
- 청중: [대상 — 기술 수준, 직급, 관심사]
- 목적: [논증형/의사결정형/인사이트형/보고형]
- 핵심 메시지: [한 문장]
- 서사 구조: [문제→원인→해법 / 해법→근거→리스크 / etc.]

## 아웃라인
| Slide | Major Title | 주제 (2-8 단어) | So What? |
|-------|------------|-----------------|----------|
| 1 | [목차 또는 첫 내용 슬라이드] | [목차면 "—"] | [목차면 "—"] |
| 2 | [Major Title] | [주제] | [핵심 메시지] |
| ... | ... | ... | ... |

---

## Slide 2: [Major Title]
### 주제: [슬라이드가 다루는 주제 — 2-8 단어 명사구]
### So What?: [이 슬라이드의 핵심 메시지 — 한 문장]

[논문급 서술 본문]

### 근거 자료
- [src-001] Table 3: 구체적 데이터 인용

### 비주얼 제안
- 유형: [bar chart / line chart / diagram / table / figure]
- 데이터: [차트에 들어갈 구체적 데이터]
- 근거: [왜 이 비주얼이 텍스트를 보충하는지]

### 이전 슬라이드와의 연결
- [Slide N에서 제기된 문제/발견을 기반으로...]

---
```

## Per-Slide Narrative Requirements

### Length
- **Minimum**: 200자 (Korean characters)
- **Maximum**: 800자
- Slides under 200자 are flagged as `[SHALLOW]` by the Assayer

### Quality Standards
- **완전한 문장**: 명사형 종결이 아닌 서술체. 학술 논문의 한 섹션처럼 작성.
- **데이터 근거**: 주장에는 반드시 출처 ID (`[src-###]`)를 명시.
- **연결 고리**: 각 슬라이드 서두에 "이 슬라이드가 나올 수밖에 없는 이유"를 설명.
- **So What?**: 매 슬라이드 내러티브의 말미에서 핵심 메시지(한 문장)를 명시적으로 서술.
- **정직한 한계**: 데이터 부족이나 해석의 한계를 숨기지 않음.

### Data Gap Markers
- `[TBD: 출처/데이터 필요]` — 수치나 근거가 부족한 경우
- `[SHALLOW: 추가 소스 필요]` — 내러티브가 200자 미만으로 충분히 채워지지 않는 경우
- `[IMAGE-NEEDED: 설명]` — 비주얼 제안에서 이미지가 필요하지만 수집하지 못한 경우
- `[CONTRADICTION: src-001 vs src-002]` — 소스 간 모순이 발견된 경우

### Meta Section Requirements
- **청중**: 구체적 (예: "ML 엔지니어, 3년+ 경력, 사내 기술 리뷰 참석자"), not generic ("기술 담당자")
- **목적**: 4가지 유형 중 하나를 명시적으로 선택하고 이유 기술
- **서사 구조**: 선택한 구조의 근거 (청중/목적에 맞는 이유)

### Outline Table Requirements
- **주제**: 2-8 단어 명사구. 문장 형태 금지.
- **So What?**: 각 슬라이드의 핵심 메시지를 한 문장으로. 단순 사실이 아닌 주장/해석/결론.
- Slide 1은 목차 또는 첫 내용 슬라이드. 목차를 사용하는 경우 So What?은 "—"로 표시. 5장 이상의 덱에서는 목차 권장.

### Visual Suggestion Requirements
- **유형**: bar chart, line chart, scatter plot, diagram, table, figure, process flow 중 선택
- **데이터**: 차트에 들어갈 구체적 수치/라벨 명시 (빈 차트 금지)
- **근거**: "이 비주얼이 텍스트에 없는 새로운 정보를 추가하는 이유"를 1문장으로 설명
- **자문 질문 (반드시 체크)**:
  1. "이 그림이 텍스트에 없는 새로운 정보를 전달하는가?" — No면 다른 비주얼 선택
  2. "청중이 3초 만에 핵심 메시지를 파악할 수 있는가?" — No면 단순화
  3. "박스 안의 텍스트를 불릿으로 옮기면 정보가 줄어드는가?" — No면 실제 데이터 차트로 교체
