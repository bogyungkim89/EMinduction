import streamlit as st
import random
import uuid

# ✅ 페이지 설정
st.set_page_config(page_title="전자기 유도 학습", layout="wide")

# ✅ 초기 세션 상태 설정
if "step" not in st.session_state:
    st.session_state.step = 0
if "scenario" not in st.session_state:
    st.session_state.scenario = random.choice(["막대자석", "코일"])
if "force_arrow_fixed" not in st.session_state:
    st.session_state.force_arrow_fixed = None

# ✅ 시나리오 설명
scenarios = {
    "막대자석": {
        "title": "막대자석이 코일로 들어가는 경우",
        "desc": "막대자석을 코일 속으로 밀어 넣을 때, 코일에 유도 전류가 생깁니다.",
        "question": "막대자석의 N극을 코일 속으로 밀어 넣을 때, 코일의 윗면은 어떤 극이 될까요?",
        "answer": "윗면이 N극",
        "explanation": "N극이 들어오면 코일은 같은 극(N극)을 만들어 밀어내려 합니다."
    },
    "코일": {
        "title": "코일 속으로 막대자석이 들어가는 경우",
        "desc": "코일 속으로 자석이 움직일 때 자기선속이 변하며 전류가 유도됩니다.",
        "question": "코일의 윗면이 N극이 되려면 전류는 어떤 방향으로 흐를까요?",
        "answer": "시계방향",
        "explanation": "윗면이 N극이 되려면 오른손 법칙에 따라 전류가 시계방향으로 흐릅니다."
    }
}

# ✅ 단계 0: 시작 화면
if st.session_state.step == 0:
    st.title("⚡ 전자기 유도 학습 앱")
    st.markdown("자기장의 변화로 유도 전류가 어떻게 생기는지 학습해봅시다!")

    if st.button("학습 시작하기 ▶️"):
        st.session_state.step = 1
        st.rerun()

# ✅ 단계 1: 첫 번째 퀴즈
elif st.session_state.step == 1:
    scenario = st.session_state.scenario
    data = scenarios[scenario]

    st.header(f"1️⃣ {data['title']}")
    st.info(data["desc"])
    st.write("")

    st.subheader("💡 문제")
    st.write(data["question"])

    # 보기 2개 (순서 랜덤)
    options = [data["answer"], "반대 극 또는 반대 방향"]
    random.shuffle(options)

    choice = st.radio("정답을 고르세요:", options, key=f"quiz1_{uuid.uuid4()}")

    if st.button("정답 확인 ▶️"):
        if choice == data["answer"]:
            st.success("✅ 정답입니다! 잘했어요.")
            st.session_state.step = 2
            st.rerun()
        else:
            st.error(f"❌ 오답이에요. {data['explanation']}")

# ✅ 단계 2: 두 번째 퀴즈 (힘 방향)
elif st.session_state.step == 2:
    st.header("2️⃣ 유도 전류에 의한 힘 방향 알아보기")

    top_pole = "N" if st.session_state.scenario == "막대자석" else "S"

    st.write(
        f"막대자석이 코일 속으로 들어갈 때, 코일의 윗면이 {top_pole}극이라면 자석에는 어떤 방향의 힘이 작용할까요?"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("위쪽 힘 ⬆️"):
            answer2 = "위쪽"
        else:
            answer2 = None
    with col2:
        if st.button("아래쪽 힘 ⬇️"):
            answer2 = "아래쪽"
        else:
            answer2 = answer2 or None

    if answer2:
        correct_answer = "위쪽" if top_pole == "N" else "아래쪽"
        explanation = "렌츠의 법칙에 따라 자석의 운동을 방해하는 방향으로 힘이 작용합니다."

        if answer2 == correct_answer:
            st.success(f"✅ 정답입니다! 힘은 {correct_answer}으로 작용합니다.")
            st.session_state.step = 3
            st.rerun()
        else:
            st.error(f"❌ 오답입니다. {explanation}")
            st.info("힘은 자석이 들어오는 방향을 방해하는 방향으로 작용합니다.")

# ✅ 단계 3: 정리 단계
elif st.session_state.step == 3:
    st.header("3️⃣ 학습 정리")

    st.success("✅ 오늘 배운 내용을 정리해볼까요?")
    st.markdown("""
    - **자기장이 변하면 코일에 유도 전류가 생깁니다.**  
    - **렌츠의 법칙:** 유도 전류는 자기장의 변화를 방해하는 방향으로 흐릅니다.  
    - **자석이 들어올 때** → 코일은 같은 극을 만들어 **밀어냅니다.**  
    - **자석이 나갈 때** → 코일은 반대 극을 만들어 **당깁니다.**  
    """)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 다시 학습하기"):
            st.session_state.step = 0
            st.session_state.scenario = random.choice(list(scenarios.keys()))
            st.rerun()
    with col2:
        st.write("")

# ✅ 마지막: 혹시 step이 잘못 설정된 경우 초기화
else:
    st.session_state.step = 0
    st.rerun()
