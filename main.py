import streamlit as st
import random

st.set_page_config(page_title="전자기 유도 학습", layout="centered")

st.title("🧲 전자기 유도 학습 앱")
st.markdown("### 자석이 코일 중심 위에서 반복적으로 움직이는 모습을 관찰하세요!")

# 시나리오 정의
scenarios = {
    1: {"desc": "N극이 코일에 가까워지는 경우", "motion": "down", "pole": "N"},
    2: {"desc": "S극이 코일에 가까워지는 경우", "motion": "down", "pole": "S"},
    3: {"desc": "N극이 코일에서 멀어지는 경우", "motion": "up", "pole": "N"},
    4: {"desc": "S극이 코일에서 멀어지는 경우", "motion": "up", "pole": "S"},
}

# 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
if "scenario" not in st.session_state:
    st.session_state.scenario = random.choice(list(scenarios.keys()))

scenario = scenarios[st.session_state.scenario]


def draw_scene(motion, pole, animate=True):
    pole_color = "red" if pole == "N" else "blue"
    move_dir = "80px" if motion == "down" else "-80px"

    anim = f"""
    @keyframes floatMove {{
        0%   {{ transform: translateY(0); }}
        50%  {{ transform: translateY({move_dir}); }}
        80%  {{ transform: translateY(0); }}  /* 복귀 시간 3배로 느리게 */
        100% {{ transform: translateY(0); }}
    }}
    """

    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px;">
      
      <!-- 자석 -->
      <div style="display:flex; align-items:center; justify-content:center; position:relative; top:0;">
        <div style="
            width:80px; height:160px;
            background:#ccc; border:4px solid #222;
            display:flex; align-items:flex-end; justify-content:center;
            position:relative;
            animation:{'floatMove 3s ease-in-out infinite' if animate else 'none'};">
            <div style="font-size:56px; font-weight:bold; color:{pole_color}; margin-bottom:2px;">{pole}</div>
        </div>
      </div>

      <!-- 코일 -->
      <svg width="260" height="240" viewBox="0 0 260 240" style="margin-top:-20px;">
        <ellipse cx="130" cy="130" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        <rect x="50" y="130" width="160" height="60" fill="#ffe7a8" stroke="#b97a00" stroke-width="2"/>
        <ellipse cx="130" cy="190" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        {"".join([f'<line x1="50" y1="{135+i*5}" x2="210" y2="{135+i*5}" stroke="#cc6600" stroke-width="2"/>' for i in range(10)])}
      </svg>
    </div>

    <style>
    {anim}
    </style>
    """
    st.components.v1.html(html, height=520)


# 단계별 학습 진행
if st.session_state.step == 0:
    st.subheader("🎬 상황 관찰하기")
    st.write(f"**상황:** {scenario['desc']}")
    draw_scene(scenario["motion"], scenario["pole"], animate=True)
    if st.button("퀴즈 시작하기 ➡️"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.subheader("퀴즈 ①: 코일이 자석에 가하는 자기력 방향")
    draw_scene(scenario["motion"], scenario["pole"], animate=False)
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
    draw_scene(scenario["motion"], scenario["pole"], animate=False)
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
    st.subheader("퀴즈 ③: 코일에 유도되는 전류 방향")
    draw_scene(scenario["motion"], scenario["pole"], animate=False)
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
