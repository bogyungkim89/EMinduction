import streamlit as st
import random
import time

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

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
if "scenario" not in st.session_state:
    st.session_state.scenario = random.choice(list(scenarios.keys()))

scenario = scenarios[st.session_state.scenario]

# HTML/SVG 애니메이션 함수
def draw_animation(motion, pole):
    direction = "translateY(60px)" if motion == "down" else "translateY(-60px)"
    arrow_dir = "↓" if motion == "down" else "↑"
    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:40px;">
      <!-- 자석 -->
      <div style="width:50px; height:120px; background:linear-gradient(to top, #d9534f 0%, #f9f9f9 100%);
                  border:2px solid #333; border-radius:8px; position:relative; animation:moveMagnet 2s ease-in-out infinite alternate;">
          <div style="position:absolute; bottom:0; width:100%; text-align:center; font-weight:bold; color:white; background-color:#333;">{pole}</div>
      </div>

      <!-- 자석 이동 화살표 -->
      <div style="font-size:48px; color:#333; margin:20px 0;">{arrow_dir}</div>

      <!-- 코일 (입체 원통) -->
      <svg width="180" height="120" viewBox="0 0 180 120">
        <!-- 윗면 -->
        <ellipse cx="90" cy="30" rx="60" ry="15" fill="#f2b84b" stroke="#b97a00" stroke-width="2"/>
        <!-- 원통 측면 -->
        <rect x="30" y="30" width="120" height="60" fill="#ffd36e" stroke="#b97a00" stroke-width="2"/>
        <!-- 아랫면 -->
        <ellipse cx="90" cy="90" rx="60" ry="15" fill="#f2b84b" stroke="#b97a00" stroke-width="2"/>
        <!-- 감긴 전선 -->
        {"".join([f'<line x1="{30+i*10}" y1="30" x2="{30+i*10}" y2="90" stroke="#cc6600" stroke-width="2"/>' for i in range(12)])}
      </svg>
    </div>

    <style>
    @keyframes moveMagnet {{
        0% {{ transform: translateY(0px); }}
        100% {{ transform: {direction}; }}
    }}
    </style>
    """
    st.components.v1.html(html, height=400)

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

