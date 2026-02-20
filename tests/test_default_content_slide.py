from slide_forge.default import get_presentation
from slide_forge.default.slide import (
    add_bullet,
    add_content_box,
    add_section,
    add_slide_title,
    add_spacer,
    create_slide,
)

prs = get_presentation()
slide = create_slide(prs)

add_slide_title(slide, "주행 환경 적응을 위한 Self-Evolving AI")

tf = add_content_box(slide)

add_section(tf, "클라우드 시스템 기반 Continual Learning 선행 연구")
add_bullet(tf, "[문제 상황] 엣지 모델이 동적 환경 변화에 적응하지 못하는 문제 발생")
add_bullet(
    tf, "새로 생기는 표지판과 날씨가 달라지면 제한된 리소스를 가진 엣지 환경에서 새로운 데이터 학습 진행", level=1
)
add_bullet(tf, "이 학습 과정은 이전 학습 정보를 급격히 잊어버림(Catastrophic Forgetting)", level=1)
add_spacer(tf)

add_section(tf, "접근법")
add_bullet(tf, "[접근법] 라벨과 예측의 불일치를 기반으로 Continual Learning으로 강건한 모델 학습")
add_bullet(tf, "Edge에서 예측 불일치 데이터를 수집하고 드리프트 탐지 혹은 시간 임계치를 만족하면 Cloud에 전송", level=1)
add_bullet(tf, "Cloud에서 엣지용 소형 모델을 Baseline 데이터와 섞어 배치 학습 진행(Replay 기반 CL)", level=1)
add_spacer(tf)

add_section(tf, "결론")
add_bullet(tf, "[결론] 클라우드 협력을 통해 엣지 모델의 지식 확장 및 분류 성능의 안정성 확보")
add_bullet(tf, "Static와 달리 동적 환경 변화 적응 및 기존 CL의 Catastrophic Forgetting 문제 해결", level=1)
add_bullet(tf, "일부 부정확한 데이터은 클라우드 Annotator 기반 라벨링으로 성능 유지", level=1)

prs.save(".tmp-00.pptx")
