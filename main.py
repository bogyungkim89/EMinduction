import streamlit as st
import random

st.set_page_config(page_title="전자기 유도 학습", layout="centered")

st.title("🧲 전자기 유도 현상 학습 앱")

st.markdown("### 자석과 코일의 상호작용을 관찰하고, 세 가지 퀴즈를 풀어보세요!")

# 상황 정의
scenarios = {
    1: {"desc": "N극이 코일에 가까워지는 경우", "motion": "down", "pole": "N"},
    2: {"desc": "S극이 코일에 가까워지는 경우", "motion": "down", "pole": "S"},
    3: {"desc": "N극이 코일에서 멀어지는 경우", "motion": "up", "pole": "N"},
    4: {"desc": "S극이 코일에서 멀어지는 경우", "motion": "up", "pole": "S"},
}

# 세션 상태
if "step" not in st.session_state:
    st.session_state.step = 0
if "scenario" not in st.session_state:
    st.session_state.scenario = random.choice(list(scenarios.keys()))

scenario = scenarios[st.session_state.scenario]


def draw_animation(motion, pole):
    # 색상 지정
    pole_color = "red" if pole == "N" else "blue"
    arrow_dir = "↑" if motion == "up" else "↓"
    arrow_offset = "-70px" if motion == "up" else "70px"
    move_distance = "-100px" if motion == "up" else "100px"

    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:30px;">
      
      <!-- 애니메이션 영역 -->
      <div style="display:flex; align-items:center; justify-content:center;">
        <!-- 자석 -->
        <div style="width:60px; height:140px; background:#999; border:3px solid #333;
                    border-radius:4px; position:relative; animation:moveMagnet 3s ease-in-out infinite;">
            <div style="position:absolute; bottom:0; width:100%; text-align:center;
                        font-weight:bold; color:{pole_color}; background-color:#fff;">{pole}</div>
        </div>

        <!-- 자석 이동 화살표 -->
        <div style="font-size:42px; color:#333; margin-left:20px;">{arrow_dir}</div>
      </div>

      <!-- 코일 (입체 원통, 수평 감김) -->
      <svg width="220" height="160" viewBox="0 0 220 160" style="margin-top:40px;">
        <!-- 윗면 -->
        <ellipse cx="110" cy="50" rx="70" ry="20" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        <!-- 원통 측면 -->
        <rect x="40" y="50" width="140" height="60" fill="#ffe7a8" stroke="#b97a00" stroke-width="2"/>
        <!-- 아랫면 -->
        <ellipse cx="110" cy="110" rx="70" ry="20" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        <!-- 가로 방향 감긴 전선 -->
        {"".join([f'<line x1="40" y1="{55+i*5}" x2="180" y2="{55+i*5}" stroke="#cc6600" stroke-width="2"/>' for i in range(10)])}
      </svg>
    </div>

    <style>
    @keyframes moveMagnet {{
        0% {{ transform: translateY(0); }}
        40% {{ transform: translateY({move_distance}); }}
        60% {{ transform: translateY({move_distance}); }}
        100% {{ transform: translateY(0); }}
    }}
    </style>
    """
    st.components.v1.html(html, height=480)


# 단계별 진행
if st.session_state.step == 0:
    st.subheader("🎬 상황 관찰하기")
    st.write(f"**상황:** {scenario['desc']}")
    draw_animation(scenario["motion"], scenario["pole"])
    if st.button("퀴즈 시작하기 ➡️"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.subheader("퀴즈 ①: 코일이 막대자석에 가하는 자기력 방향")
    options = ["위쪽(밀어냄)", "아래쪽(끌어당김)"]
    answer1 = st.radio("방향을 선택하세요", options)
    correct = "위쪽(밀어냄)" if scenario["motion"] == "down" else "아래쪽(끌어당김)"
    if st.button("다음 단계 ➡️"):
        if answer1 == correct:
            st.session_state.step = 2
        else:
            st.error("❌ 오답이에요. 자기력 방향을 다시 생각해보세요!")
        st.rerun()

elif st.session_state.step == 2:
    st.subheader("퀴즈 ②: 코일의 윗면 자극은?")
    if scenario["motion"] == "down":
        top_pole = "N" if scenario["pole"] == "N" else "S"
    else:
        top_pole = "S" if scenario["pole"] == "N" else "N"
    options = ["윗면이 N극", "윗면이 S극"]
    answer2 = st.radio("코일의 윗면 자극을 선택하세요", options)
    if st.button("다음 단계 ➡️"):
        if answer2 == f"윗면이 {top_pole}극":
            st.session_state.step = 3
        else:
            st.error("❌ 오답이에요. 렌츠의 법칙을 떠올려보세요!")
        st.rerun()

elif st.session_state.step == 3:
    st.subheader("퀴즈 ③: 코일에 흐르는 전류의 방향")
    if scenario["motion"] == "down" and scenario["pole"] == "N":
        current = "시계방향"
    elif scenario["motion"] == "down" and scenario["pole"] == "S":
        current = "반시계방향"
    elif scenario["motion"] == "up" and scenario["pole"] == "N":
        current = "반시계방향"
    else:
        current = "시계방향"
    options = ["시계방향", "반시계방향"]
    answer3 = st.radio("전류의 방향을 선택하세요", options)
    if st.button("결과 보기 🎯"):
        if answer3 == current:
            st.success("✅ 모든 퀴즈를 정확히 풀었어요! 전자기 유도 현상을 완벽히 이해했네요 🎉")
        else:
            st.error("❌ 마지막 단계에서 오답이에요. 전류 방향을 다시 생각해보세요!")
