# /// script
# requires-python = ">=3.12"
# dependencies = ["slide-forge"]
#
# [tool.uv.sources]
# slide-forge = { path = "../" }
# ///

"""visual_area 데모 — 실제 PPTX 생성."""

from slide_forge import (
    add_bullet,
    add_content_box,
    add_section,
    add_slide_title,
    add_spacer,
    create_slide,
    visual_area,
)
from slide_forge.default import get_presentation
from slide_forge.default.slide import add_chart, add_figure, add_shape, add_table

prs = get_presentation()

# ── 슬라이드 1: 차트 1개 (전체 너비) ─────────────────────────
s1 = create_slide(prs)
add_slide_title(s1, "Visual Area — 차트 1개")
tf = add_content_box(s1)
add_section(tf, "단일 차트 배치")
add_bullet(tf, "visual_area(slide) → add_chart → render()")
add_bullet(tf, "차트가 하단 영역 전체 너비를 차지", level=1)

area = visual_area(s1)
area.add_chart(
    "column",
    categories=["J1", "J2", "J3", "J4", "J5", "J6"],
    series={"R²": [93.5, 23.2, 91.8, 45.6, 78.9, 95.1]},
    title="Per-Joint R² Score",
    legend=False,
    caption="[Figure 1] Joint별 예측 정확도",
)
area.render()

# ── 슬라이드 2: 차트 + 테이블 (1:1) ─────────────────────────
s2 = create_slide(prs)
add_slide_title(s2, "Visual Area — 차트 + 테이블 (1:1)")
tf2 = add_content_box(s2)
add_section(tf2, "두 요소 균등 배치")
add_bullet(tf2, "차트와 테이블이 동일한 너비로 나란히 배치")
add_bullet(tf2, "gap=150,000 EMU (~0.17 inch) 자동 적용", level=1)

area2 = visual_area(s2)
area2.add_chart(
    "column",
    categories=["Q1", "Q2", "Q3", "Q4"],
    series={"매출": [120, 150, 180, 200], "비용": [80, 90, 100, 110]},
    title="분기별 매출/비용",
)
area2.add_table(
    [
        ["항목", "Q1", "Q2", "Q3", "Q4"],
        ["매출", "120", "150", "180", "200"],
        ["비용", "80", "90", "100", "110"],
        ["이익", "40", "60", "80", "90"],
    ],
    first_row=True,
)
area2.render()

# ── 슬라이드 3: 차트 + 테이블 (2:1 가중치) ──────────────────
s3 = create_slide(prs)
add_slide_title(s3, "Visual Area — 가중치 2:1")
tf3 = add_content_box(s3)
add_section(tf3, "가중치 기반 너비 할당")
add_bullet(tf3, "weight=2 → 차트가 전체 너비의 2/3 차지")
add_bullet(tf3, "weight=1 → 테이블이 전체 너비의 1/3 차지", level=1)

area3 = visual_area(s3)
area3.add_chart(
    "line_markers",
    categories=["Week1", "Week2", "Week3", "Week4"],
    series={"Accuracy": [85.2, 87.1, 89.5, 91.0], "Recall": [78.3, 82.4, 84.0, 86.5]},
    weight=2,
    title="Training Progress",
)
area3.add_table(
    [
        ["Metric", "Value"],
        ["Best Epoch", "47"],
        ["LR", "1e-4"],
        ["Batch", "64"],
        ["Dropout", "0.3"],
    ],
    weight=1,
    first_row=True,
)
area3.render()

# ── 슬라이드 4: 3개 차트 나란히 ─────────────────────────────
s4 = create_slide(prs)
add_slide_title(s4, "Visual Area — 3개 요소")
tf4 = add_content_box(s4)
add_section(tf4, "세 요소 균등 배치")
add_bullet(tf4, "Pie + Column + Radar 차트가 각각 1/3 너비")

area4 = visual_area(s4)
area4.add_chart(
    "pie",
    categories=["클라우드", "엣지", "하이브리드"],
    series={"비율": [45, 35, 20]},
    title="배포 환경",
)
area4.add_chart(
    "column",
    categories=["J1", "J2", "J3"],
    series={"F1": [90.1, 45.2, 88.7]},
    title="Per-Joint F1",
)
area4.add_chart(
    "radar_filled",
    categories=["정확도", "속도", "메모리", "확장성", "안정성"],
    series={"모델A": [90, 70, 85, 60, 95]},
    title="모델 평가",
)
area4.render()

# ── 슬라이드 5: 도형 + 차트 혼합 ────────────────────────────
s5 = create_slide(prs)
add_slide_title(s5, "Visual Area — 도형 + 차트 혼합")
tf5 = add_content_box(s5)
add_section(tf5, "다양한 요소 타입 혼합")
add_bullet(tf5, "도형(rectangle)과 차트를 함께 배치")
add_bullet(tf5, "도형은 container height 사용, 차트도 동일", level=1)

area5 = visual_area(s5)
area5.add_shape(
    "rounded_rectangle",
    fill="E7E6E6",
    line_color="BFBFBF",
    text="핵심 요약\n\nF1-Score: 90.1%\nPrecision: 92.3%",
    font_size=12,
    color="404040",
    bold=True,
)
area5.add_chart(
    "column",
    categories=["Precision", "Recall", "F1"],
    series={"Score": [92.3, 88.0, 90.1]},
    title="Detection Metrics",
    caption="[Figure 3] 이상 탐지 성능",
)
area5.render()

# ── 슬라이드 6: 체이닝 문법 ─────────────────────────────────
s6 = create_slide(prs)
add_slide_title(s6, "Visual Area — 체이닝 문법")
tf6 = add_content_box(s6)
add_section(tf6, "메서드 체이닝")
add_bullet(tf6, "area.add_chart(...).add_table(...).render()")
add_bullet(tf6, "각 add_* 메서드가 self를 반환하여 체이닝 가능", level=1)

(
    visual_area(s6)
    .add_chart(
        "doughnut",
        categories=["학습", "검증", "테스트"],
        series={"분할": [70, 15, 15]},
        title="데이터셋 분할",
    )
    .add_table(
        [
            ["세트", "비율", "건수"],
            ["학습", "70%", "840K"],
            ["검증", "15%", "180K"],
            ["테스트", "15%", "180K"],
        ],
        first_row=True,
    )
    .render()
)

# ── 저장 ───────────────────────────────────────────────────
out = ".tmp-visual-area-demo.pptx"
prs.save(out)
print(f"\n[OK] {out} 저장 완료 (슬라이드 {len(prs.slides)}장)")
