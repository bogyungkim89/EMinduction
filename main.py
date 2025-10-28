import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Arc

# ---------------------------------------
# Streamlit 기본 설정
# ---------------------------------------
st.set_page_config(page_title="전자기 유도 학습", page_icon="⚡", layout="centered")

st.title("⚡ 전자기 유도 학습 웹앱 (시각화 버전)")
st.markdown("#### 자석과 코일의 상호작용을 보고, 자기력・자극・전류 방향을 추론해보세요!")

# ---------------------------------------
# 상황 정의
# ---------------------------------------
cases = {
    1: "N극이 코일에 가까워진다",
    2: "S극이 코일에 가까워진다",
    3: "N극이 코일에서 멀어진다",
    4: "S극이 코일에서 멀어진다"
}

answers = {
    1: {"force": "위쪽", "coil_pole": "윗면 N극, 아랫면 S극", "current": "시계방향"},
    2: {"force": "위쪽", "coil_pole": "윗면 S극, 아랫면 N극", "current": "반시계방향"},
    3: {"force": "아래쪽", "coil_pole": "윗면 S극, 아랫면 N극", "current": "반시계방향"},
    4: {"force": "아래쪽", "coil_pole": "윗면 N극, 아랫면 S극", "current": "시계방향"},
}

# ---------------------------------------
# 랜덤 상황 선택
# ---------------------------------------
if "selected_case" not in st.session_state:
    st.session_state.selected_case = random.choice(list(cases.keys()))

case_num = st.session_state.selected_case
st.subheader(f"📘 상황: **{cases[case_num]}**")

# ---------------------------------------
# 시각화 함수
# ---------------------------------------
def draw_scene(case_num):
    fig, ax = plt.subplots(figsize=(4,6))
    ax.set_xlim(-2,2)
    ax.set_ylim(-1,5)
    ax.axis("off")

    # 코일 (원통)
    coil = patches.Rectangle((-0.8, 0), 1.6, 2, linewidth=2, edgecolor="orange", facecolor="none")
    ax.add_patch(coil)
    ax.text(0, -0.3, "코일", ha="center", va="top", fontsize=12)

    # 코일 전선 (시계방향 감김 표현: 앞면 -> 오른쪽으로)
    ax.arrow(-0.8, 0.5, 1.6, 0, head_width=0.05, head_length=0.1, fc='orange', ec='orange')
    ax.arrow(0.8, 1.5, -1.6, 0, head_width=0.05, head_length=0.1, fc='orange', ec='orange')

    # 막대 자석
    magnet_y = 3.5
    ax.add_patch(patches.Rectangle((-0.5, magnet_y), 1, 0.5, facecolor="lightgray", edgecolor="black"))
    if "N극" in cases[case_num]:
        ax.text(-0.3, magnet_y + 0.25, "N", color="red", fontsize=16, fontweight="bold", ha="center")
        ax.text(0.3, magnet_y + 0.25, "S", color="blue", fontsize=16, fontweight="bold", ha="center")
    else:
        ax.text(-0.3, magnet_y + 0.25, "S", color="blue", fontsize=16, fontweight="bold", ha="center")
        ax.text(0.3, magnet_y + 0.25, "N", color="red", fontsize=16, fontweight="bold", ha="center")

    # 자석 이동 방향 화살표
    move_dir = -1 if "가까워" in cases[case_num] else 1
    ax.arrow(0, magnet_y + 0.7 if move_dir < 0 else magnet_y - 0.3, 0, move_dir * 0.4,
             head_width=0.2, head_length=0.2, fc="gray", ec="gray")
    ax.text(0.5, magnet_y + (0.5 if move_dir < 0 else -0.5),
            "가까워짐" if move_dir < 0 else "멀어짐", fontsize=11, color="gray")

    return fig

# 시각화 표시
fig = draw_scene(case_num)
st.pyplot(fig)

st.info("🌀 코일은 원통의 위에서 보면 **시계방향으로 감긴 형태**입니다.")

st.write("---")

# ---------------------------------------
# 퀴즈 1: 자기력 방향
# ---------------------------------------
st.markdown("### 🧭 1단계: 코일이 막대자석에 가하는 자기력의 방향은?")
force_answer = st.radio(
    "막대자석의 움직임을 방해하는 방향을 선택하세요:",
    ["위쪽 (밀어냄)", "아래쪽 (끌어당김)"]
)

# ---------------------------------------
# 퀴즈 2: 코일의 자극
# ---------------------------------------
st.markdown("### 🧲 2단계: 코일의 자극은 어디일까?")
pole_answer = st.radio(
    "코일의 윗면과 아랫면의 자극을 선택하세요:",
    ["윗면 N극, 아랫면 S극", "윗면 S극, 아랫면 N극"]
)

# ---------------------------------------
# 퀴즈 3: 전류 방향
# ---------------------------------------
st.markdown("### 🔄 3단계: 코일에 흐르는 전류의 방향은?")
current_answer = st.radio(
    "코일 윗면에서 바라봤을 때 전류의 방향을 선택하세요:",
    ["시계방향", "반시계방향"]
)

st.write("---")

# ---------------------------------------
# 정답 확인
# ---------------------------------------
if st.button("✅ 정답 확인"):
    correct = answers[case_num]

    result_stage = 0

    if ("위쪽" in force_answer and correct["force"] != "위쪽") or \
       ("아래쪽" in force_answer and correct["force"] != "아래쪽"):
        result_stage = 1
    elif pole_answer != correct["coil_pole"]:
        result_stage = 2
    elif current_answer != correct["current"]:
        result_stage = 3

    # 결과 피드백
    if result_stage == 0:
        st.success("🎉 정답이에요! 세 단계를 모두 정확히 이해했어요.")
    elif result_stage == 1:
        st.error(f"❌ 1단계 오답이에요. 올바른 자기력 방향은 **{correct['force']}** 입니다.")
    elif result_stage == 2:
        st.error(f"❌ 2단계 오답이에요. 코일의 자극은 **{correct['coil_pole']}** 입니다.")
    elif result_stage == 3:
        st.error(f"❌ 3단계 오답이에요. 전류의 방향은 **{correct['current']}** 입니다.")

    with st.expander("💡 정답 및 해설 보기"):
        st.markdown(f"""
        - **자기력 방향:** {correct['force']}
        - **코일의 자극:** {correct['coil_pole']}
        - **전류 방향:** {correct['current']}
        """)
        st.info("""
        🧲 **렌츠의 법칙**  
        유도 전류는 항상 **자석의 움직임을 방해하는 방향**으로 흐릅니다.  
        자석이 가까워질 때는 밀어내고, 멀어질 때는 끌어당기는 방향이에요.
        """)

# ---------------------------------------
# 새 상황 버튼
# ---------------------------------------
if st.button("🔄 새 상황 받기"):
    st.session_state.selected_case = random.choice(list(cases.keys()))
    st.experimental_rerun()

st.write("---")
st.caption("© 2025 전자기 유도 학습 시각화 앱 — Streamlit + Matplotlib")
