from slide_forge.default import get_presentation
from slide_forge.default.slide import (
    add_bullet,
    add_content_box,
    add_cover_info,
    add_cover_title,
    add_section,
    add_slide_title,
    add_spacer,
    create_cover_slide,
    create_slide,
)

prs = get_presentation()

# ── 표지 슬라이드 ───────────────────────────────────────────
cover = create_cover_slide(prs)
add_cover_title(
    cover,
    "Vision-Language-Action 모델의\n\nSim-to-Real 전이를 통한 공간 지능 구현",
)
add_cover_info(cover, date="2026년 02월 06일", presenter="최성빈")

# 표지 슬라이드에 내용 함수를 호출하면 오류 발생 확인
try:
    add_slide_title(cover, "잘못된 호출")
    raise AssertionError("표지에서 add_slide_title 호출이 허용됨")
except TypeError as e:
    print(f"[OK] 표지 → add_slide_title 차단: {e}")

try:
    add_content_box(cover)
    raise AssertionError("표지에서 add_content_box 호출이 허용됨")
except TypeError as e:
    print(f"[OK] 표지 → add_content_box 차단: {e}")

# ── 내용 슬라이드 ───────────────────────────────────────────
slide = create_slide(prs)

# 내용 슬라이드에 표지 함수를 호출하면 오류 발생 확인
try:
    add_cover_title(slide, "잘못된 호출")
    raise AssertionError("내용에서 add_cover_title 호출이 허용됨")
except TypeError as e:
    print(f"[OK] 내용 → add_cover_title 차단: {e}")

try:
    add_cover_info(slide, date="X", presenter="X")
    raise AssertionError("내용에서 add_cover_info 호출이 허용됨")
except TypeError as e:
    print(f"[OK] 내용 → add_cover_info 차단: {e}")

add_slide_title(slide, "주행 환경 적응을 위한 Self-Evolving AI")

tf = add_content_box(slide)

add_section(tf, "클라우드 시스템 기반 Continual Learning 선행 연구")
add_bullet(tf, "[문제 상황] 엣지 모델이 [green]동적 환경 변화에 적응하지 못하는 문제 발생[/green]")
add_bullet(
    tf,
    "새로 생기는 표지판과 날씨가 달라지면 제한된 리소스를 가진 엣지 환경에서 새로운 데이터 학습 진행",
    level=1,
)
add_bullet(
    tf,
    "이 학습 과정은 이전 학습 정보를 급격히 잊어버림([green]Catastrophic Forgetting[/green]) [purple]-> 모델 성능의 신뢰성을 훼손[/purple]",
    level=1,
)
add_spacer(tf)

add_bullet(tf, "[접근법] 라벨과 예측의 불일치를 기반으로 [green]Continual Learning(CL)으로 강건성 확보[/green]")
add_bullet(
    tf,
    "Edge에서 [purple]예측 불일치 데이터[/purple]를 수집하고 드리프트 탐지 혹은 시간 임계치를 만족하면 Cloud에 데이터 업데이트",
    level=1,
)
add_bullet(
    tf,
    "Cloud에서 엣지용 소형 모델을 [purple]Baseline 데이터와 섞어 배치 학습 진행(Replay)[/purple] -> 모델 업데이트",
    level=1,
)
add_spacer(tf)

add_bullet(tf, "[결론] 클라우드 협력을 통해 엣지 모델의 지식 확장 및 분류 성능의 안정성 확보")
add_bullet(
    tf,
    "Static와 달리 동적 환경 변화 적응 및 기존 CL의 [purple]Catastrophic Forgetting[/purple] 현상 방지",
    level=1,
)
add_bullet(
    tf,
    "일부 부정확한 데이터은 [green]클라우드 Annotator 기반 라벨링으로[/green] 성능 유지 -> 강건한 모델 구축 가능",
    level=1,
)
add_spacer(tf)

add_section(tf, "Bullet Style 테스트")
add_bullet(tf, "Level 0: dash (기본값)", level=0)
add_bullet(tf, "Level 1: arrow (기본값)", level=1)
add_bullet(tf, "Level 2: square (기본값)", level=2)
add_bullet(tf, "Level 3: circle (기본값)", level=3)
add_bullet(tf, "Level 4: check (기본값)", level=4)
add_spacer(tf)
add_bullet(tf, "Number 테스트 항목 A", bullet="number")
add_bullet(tf, "Number 테스트 항목 B", bullet="number")
add_bullet(tf, "None: 글머리 기호 없음", bullet="none")

prs.save(".tmp-00.pptx")
print("\n[OK] .tmp-00.pptx 저장 완료")
