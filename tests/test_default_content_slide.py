from slide_forge.default import get_presentation
from slide_forge.default.slide import (
    add_bullet,
    add_chart,
    add_content_box,
    add_cover_info,
    add_cover_title,
    add_figure,
    add_line,
    add_section,
    add_shape,
    add_slide_title,
    add_spacer,
    add_table,
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
add_cover_info(cover, date="2026년 02월 06일", presenter="홍길동")

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

# ── Bullet Style 테스트 (별도 슬라이드 — add_section은 TextFrame당 1회만 허용) ──
bullet_slide = create_slide(prs)
add_slide_title(bullet_slide, "Bullet Style 테스트")
tf2 = add_content_box(bullet_slide)
add_section(tf2, "Bullet Style 테스트")
add_bullet(tf2, "Level 0: dash (기본값)", level=0)
add_bullet(tf2, "Level 1: arrow (기본값)", level=1)
add_bullet(tf2, "Level 2: square (기본값)", level=2)
add_bullet(tf2, "Level 3: circle (기본값)", level=3)
add_bullet(tf2, "Level 4: check (기본값)", level=4)
add_spacer(tf2)
add_bullet(tf2, "Number 테스트 항목 A", bullet="number")
add_bullet(tf2, "Number 테스트 항목 B", bullet="number")
add_bullet(tf2, "None: 글머리 기호 없음", bullet="none")

# ── 테이블 슬라이드 ──────────────────────────────────────────
tbl_slide = create_slide(prs)
add_slide_title(tbl_slide, "테이블 테스트")

add_table(
    tbl_slide,
    data=[
        ["Group", "Hidden\nSize", "Num\nLayer"],
        ["접근", "512", "4"],
        ["미소", "256", "2"],
        ["감정", "256", "2"],
    ],
    left=972000,
    top=1989000,
    width=3960000,
    first_row=True,
    first_col=False,
)

# first_col 옵션 테스트
add_table(
    tbl_slide,
    data=[
        ["항목", "값A", "값B"],
        ["Alpha", "100", "200"],
        ["Beta", "300", "400"],
    ],
    left=5200000,
    top=1989000,
    width=3600000,
    first_row=True,
    first_col=True,
)

# ── 차트 슬라이드 1: Category 계열 ─────────────────────────────
chart_slide1 = create_slide(prs)
add_slide_title(chart_slide1, "Category 차트 테스트")

add_chart(
    chart_slide1,
    "column",
    categories=["Q1", "Q2", "Q3", "Q4"],
    series={"매출": [120, 150, 180, 200], "비용": [80, 90, 100, 110]},
    left=200000,
    top=800000,
    width=4200000,
    height=3200000,
    title="분기별 매출/비용",
)

add_chart(
    chart_slide1,
    "line_markers",
    categories=["1월", "2월", "3월", "4월", "5월"],
    series={"정확도": [92, 94, 93, 96, 97], "재현율": [88, 90, 89, 93, 95]},
    left=4700000,
    top=800000,
    width=4200000,
    height=3200000,
    title="월별 모델 성능",
)

# ── 차트 슬라이드 2: Pie / Radar / Bar ────────────────────────
chart_slide2 = create_slide(prs)
add_slide_title(chart_slide2, "Pie / Radar / Bar 차트")

add_chart(
    chart_slide2,
    "pie",
    categories=["클라우드", "엣지", "하이브리드"],
    series={"비율": [45, 35, 20]},
    left=200000,
    top=800000,
    width=2800000,
    height=3200000,
    title="배포 환경 비율",
)

add_chart(
    chart_slide2,
    "radar_filled",
    categories=["정확도", "속도", "메모리", "확장성", "안정성"],
    series={"모델A": [90, 70, 85, 60, 95], "모델B": [75, 95, 70, 90, 80]},
    left=3200000,
    top=800000,
    width=2800000,
    height=3200000,
    title="모델 비교 레이더",
)

add_chart(
    chart_slide2,
    "bar_stacked",
    categories=["팀A", "팀B", "팀C"],
    series={"완료": [30, 25, 40], "진행중": [10, 15, 5], "대기": [5, 10, 8]},
    left=6200000,
    top=800000,
    width=2800000,
    height=3200000,
    title="팀별 작업 현황",
)

# ── 차트 슬라이드 3: Scatter / Bubble / Doughnut ───────────────
chart_slide3 = create_slide(prs)
add_slide_title(chart_slide3, "Scatter / Bubble / Doughnut 차트")

add_chart(
    chart_slide3,
    "scatter",
    series={
        "실험군": [(1.2, 3.4), (2.1, 4.5), (3.0, 5.1), (4.2, 6.8)],
        "대조군": [(1.0, 2.0), (2.5, 3.2), (3.5, 4.0), (4.0, 5.5)],
    },
    left=200000,
    top=800000,
    width=2800000,
    height=3200000,
    title="산점도",
)

add_chart(
    chart_slide3,
    "bubble",
    series={
        "GPU": [(4, 90, 30), (8, 95, 50), (16, 97, 80)],
        "CPU": [(2, 70, 10), (4, 80, 20), (8, 85, 35)],
    },
    left=3200000,
    top=800000,
    width=2800000,
    height=3200000,
    title="리소스별 성능",
)

add_chart(
    chart_slide3,
    "doughnut",
    categories=["학습", "검증", "테스트"],
    series={"데이터 분할": [70, 15, 15]},
    left=6200000,
    top=800000,
    width=2800000,
    height=3200000,
    title="데이터셋 분할",
    caption="[Figure 2] 데이터셋 구성 비율",
)

# ── 이미지 슬라이드 ─────────────────────────────────────────
fig_slide = create_slide(prs)
add_slide_title(fig_slide, "Figure 테스트")

add_figure(
    fig_slide,
    ".tmp-00-figure.png",
    left=1500000,
    top=1200000,
    width=6000000,
    caption="[Figure 1] 실험 결과 시각화",
)

# ── 도형 슬라이드 ──────────────────────────────────────────
shape_slide = create_slide(prs)
add_slide_title(shape_slide, "Shape / Line 테스트")

# 섹션 헤더 바 (pptxgenjs.md 패턴: 배경 바 + 액센트 스트라이프)
add_shape(
    shape_slide,
    "rectangle",
    left=166261,
    top=724090,
    width=8870234,
    height=400000,
    fill="E7E6E6",
)
add_shape(
    shape_slide,
    "rectangle",
    left=166261,
    top=724090,
    width=70000,
    height=400000,
    fill="1B3765",
)

# 테두리 + 채우기 카드
add_shape(
    shape_slide,
    "rounded_rectangle",
    left=200000,
    top=1300000,
    width=4000000,
    height=1200000,
    fill="FFFFFF",
    line_color="BFBFBF",
    line_width=1,
    shadow={"blur": 4, "offset": 2, "angle": 135, "opacity": 0.12},
    text="카드 레이아웃 예시",
    font_size=14,
    color="404040",
    bold=True,
)

# 반투명 오버레이
add_shape(
    shape_slide,
    "rectangle",
    left=4800000,
    top=1300000,
    width=4000000,
    height=1200000,
    fill="072A5E",
    transparency=40,
)

# 다양한 도형
add_shape(
    shape_slide,
    "oval",
    left=200000,
    top=2800000,
    width=1200000,
    height=1200000,
    fill="00B050",
    text="Oval",
    color="FFFFFF",
    font_size=12,
)
add_shape(
    shape_slide,
    "diamond",
    left=1700000,
    top=2800000,
    width=1200000,
    height=1200000,
    fill="FF7F00",
)
add_shape(
    shape_slide,
    "hexagon",
    left=3200000,
    top=2800000,
    width=1200000,
    height=1200000,
    fill="7030A0",
)
add_shape(
    shape_slide,
    "chevron",
    left=4700000,
    top=2800000,
    width=1500000,
    height=1200000,
    fill="0070C0",
    text="Next",
    color="FFFFFF",
    font_size=12,
)
add_shape(
    shape_slide,
    "triangle",
    left=6500000,
    top=2800000,
    width=1200000,
    height=1200000,
    fill="C00000",
)

# 구분선
add_line(
    shape_slide,
    left=200000,
    top=4200000,
    width=8800000,
    color="BFBFBF",
    line_width=1,
)
add_line(
    shape_slide,
    left=200000,
    top=4400000,
    width=8800000,
    color="C00000",
    line_width=2,
    dash="dash",
)

prs.save(".tmp-00.pptx")
print("\n[OK] .tmp-00.pptx 저장 완료")
