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

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
if "scenario" not in st.session_state:
    st.session_state.scenario = random.choice(list(scenarios.keys()))

scenario = scenarios[st.session_state.scenario]


def draw_scene(motion, pole, animate=True):
    pole_color = "red" if pole == "N" else "blue"
    arrow_symbol = "↓" if motion == "down" else "↑"
    move_dir = "100px" if motion == "down" else "-100px"

    # 애니메이션 키프레임: 출발지점→이동→정지 (불연속, 원위치 복귀 X)
    anim = f"""
    @keyframes moveOnce {{
        0%   {{ transform: translateY(0); }}
        80%  {{ transform: translateY({move_dir}); }}
        100% {{ transform: translateY({move_dir}); }}
    }}
    """

    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px;">
      
      <!-- 자석 + 화살표 -->
      <div style="display:flex; align-items:center; justify-content:center;">

        <!-- 자석 -->
        <div style="width:80px; height:160px; background:#888; border:4px solid #222;
                    display:flex; align-items:end; justify-content:center;
                    animation:{'moveOnce 2s ease-out forwards' if animate else 'none'};">
            <div style="font-size:28px; font-weight:bold; color:{pole_color}; margin-bottom:6px;">{pole}</div>
        </div>

        <!-- 방향 화살표 (자석 오른쪽 측면에 표시) -->
        <div style="font-size:48px; color:#222; margin-left:25px;">{arrow_symbol}</div>
      </div>

      <!-- 코일 (입체 원통, 수평 감김) -->
      <svg width="260" height="180" viewBox="0 0 260 180" style="margin-top:20px;">
        <!-- 윗면 -->
        <ellipse cx="130" cy="70" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        <!-- 측면 -->
        <rect x="50" y="70" width="160" height="60" fill="#ffe7a8" stroke="#b97a00" stroke-width="2"/>
        <!-- 아랫면 -->
        <ellipse cx="130" cy="130" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        <!-- 전선 (수평 방향 감김) -->
        {"".join([f'<line x1="50" y1="{75+i*5}" x2="210" y2="{75+i*5}" stroke="#cc6600" stroke-width="2"/>' for i in range(10)])}
      </svg>
    </div>

    <style>
    {anim}
    </style>
    """
    st.components.v1.html(html, height=500)


# 단계별 진행 로직
if st.session_state.step == 0:
    st.subheader("🎬 상황 관찰하기")
    st.write(f"**상황:** {scenario['desc']}")

    # 자석 애니메이션 1회 재생
    draw_scene(scenario["motion"], scenario["pole"], animate=True)
    if st.button("퀴즈 시작하기 ➡️"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.subheader("퀴즈 ①: 코일이 막대자석에 가하는 자기력 방향")
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
    st.subheader("퀴즈 ③: 코일에 흐르는 전류의 방향")
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
