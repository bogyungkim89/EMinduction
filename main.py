import streamlit as st
import random

st.set_page_config(page_title="전자기 유도 학습", layout="centered")

# -------------------------------
# 시나리오 설정
# -------------------------------
scenarios = [
    {"motion": "up", "pole": "N"},
    {"motion": "up", "pole": "S"},
    {"motion": "down", "pole": "N"},
    {"motion": "down", "pole": "S"},
]

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
if "scenario" not in st.session_state:
    st.session_state.scenario = random.choice(scenarios)
if "prev_scenario" not in st.session_state:
    st.session_state.prev_scenario = None

# -------------------------------
# 시각화 HTML 구성 함수
# -------------------------------
def get_scene_html(motion, pole, animate=False):
    arrow_svg = f"""
        <svg width="80" height="80" style="position:absolute; right:-100px; top:50%; transform:translateY(-50%);">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#16a34a" />
                </marker>
            </defs>
            <line x1="10" y1="40" x2="70" y2="40" stroke="#16a34a" stroke-width="4" marker-end="url(#arrowhead)" />
        </svg>
    """

    magnet_html = f"""
        <div class="magnet {'magnet-anim' if animate else ''}" style="background:linear-gradient(to bottom, {'#ef4444' if pole=='N' else '#3b82f6'} 50%, {'#3b82f6' if pole=='N' else '#ef4444'} 50%);">
            <div class="label top-label">{pole}</div>
            <div class="label bottom-label">{'S' if pole=='N' else 'N'}</div>
            {arrow_svg}
        </div>
    """

    html = f"""
    <div class="scene">
        <svg width="160" height="260">
            <defs>
                <radialGradient id="coilGradient" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#fef3c7" />
                    <stop offset="100%" stop-color="#f59e0b" />
                </radialGradient>
            </defs>
            <ellipse cx="80" cy="130" rx="50" ry="20" fill="url(#coilGradient)" stroke="#92400e" stroke-width="3"/>
            <path d="M30,130 Q80,160 130,130" fill="none" stroke="#92400e" stroke-width="3" />
        </svg>
        {magnet_html}
    </div>

    <style>
        .scene {{
            position: relative;
            width: 160px;
            height: 260px;
            margin: auto;
        }}
        .magnet {{
            position: absolute;
            left: 40px;
            top: { '40px' if motion == 'up' else '160px' };
            width: 80px;
            height: 60px;
            border-radius: 8px;
            border: 2px solid #1f2937;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            color: white;
            font-weight: bold;
        }}
        .magnet-anim {{
            animation: floatMove 1.5s ease-in-out infinite alternate;
        }}
        @keyframes floatMove {{
            0% {{ top: { '40px' if motion == 'up' else '160px' }; }}
            100% {{ top: { '80px' if motion == 'up' else '120px' }; }}
        }}
        .label {{
            font-size: 18px;
            text-align: center;
            width: 100%;
        }}
        .top-label {{
            margin-top: 4px;
        }}
        .bottom-label {{
            margin-bottom: 4px;
        }}
    </style>
    """
    return html

# -------------------------------
# 메인 화면 구성
# -------------------------------
st.title("🧲 전자기 유도 학습 시뮬레이션")

# 현재 시나리오
scenario = st.session_state.scenario

# --------------------------------
# Step 0: 관찰 단계
# --------------------------------
if st.session_state.step == 0:
    st.markdown("### ① 자석이 코일과 어떻게 상호작용하는지 관찰해보세요.")
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=420)
    st.markdown("자석이 움직이면 코일에 어떤 변화가 생길까요?")

    if st.button("다음 단계로 ➡️"):
        st.session_state.step = 1
        st.rerun()

# --------------------------------
# Step 1: 코일이 자석에 가하는 힘의 방향 퀴즈 (자동 이동 추가됨)
# --------------------------------
elif st.session_state.step == 1:
    quiz1_full_html = f"""
    <div id="quiz1-interactive-container" style="display:flex; flex-direction:column; align-items:center;">
        
        <!-- 버튼 컨테이너 -->
        <div id="quiz1-buttons" style="display:flex; justify-content: center; width:100%; max-width: 500px; margin: 1rem 0;">
            <div id="up-choice" class="quiz-choice-wrapper" style="width: 45%; margin-right: 10%;">
                <button type="button" class="quiz-button" data-choice="Up">⬆️ 위쪽 힘</button>
            </div>
            <div id="down-choice" class="quiz-choice-wrapper" style="width: 45%;">
                <button type="button" class="quiz-button" data-choice="Down">⬇️ 아래쪽 힘</button>
            </div>
        </div>

        <!-- 시각화 영역 -->
        <div id="visualization-area">
            {get_scene_html(scenario["motion"], scenario["pole"], animate=True)}
        </div>

        <style>
            .quiz-button {{
                background-color: #f0f2f6;
                color: #262730;
                border: 1px solid #ccc;
                border-radius: 0.5rem;
                padding: 0.5rem 1rem;
                width: 100%;
                cursor: pointer;
                font-size: 1rem;
                font-weight: 600;
                transition: background-color 0.2s, box-shadow 0.2s;
            }}
            .quiz-button:hover {{
                background-color: #e0e0e0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            #up-choice button {{ border: 2px solid #3b82f6; }}
            #down-choice button {{ border: 2px solid #ef4444; }}
        </style>

        <script>
            const correctDir = "{'Up' if scenario['motion'] == 'down' else 'Down'}";
            const forceUp = document.getElementById('force-up');
            const forceDown = document.getElementById('force-down');
            const upButton = document.querySelector('#up-choice button');
            const downButton = document.querySelector('#down-choice button');

            function handleClick(dir) {{
                if (dir === correctDir) {{
                    window.location.search = '?correct=true';
                }} else {{
                    window.location.search = '?correct=false';
                }}
            }}

            upButton.addEventListener('click', () => handleClick('Up'));
            downButton.addEventListener('click', () => handleClick('Down'));
        </script>
    </div>
    """
    st.components.v1.html(quiz1_full_html, height=620)

    # 정답 여부 판정
    query = st.query_params
    if "correct" in query:
        if query["correct"] == "true":
            st.session_state.step = 2
            st.success("✅ 정답입니다! 자동으로 다음 단계로 넘어갑니다.")
        else:
            st.error("❌ 오답이에요. 자석의 움직임을 방해하는 방향으로 힘이 작용해야 해요.")
        del st.query_params["correct"]
        st.rerun()

# --------------------------------
# Step 2: 코일 윗면의 자극 판별 퀴즈
# --------------------------------
elif st.session_state.step == 2:
    st.markdown("### ② 코일 윗면의 자극은 어느 쪽일까요?")
    choice = st.radio("코일 윗면의 자극을 선택하세요:", ["N극", "S극"], index=None)

    if choice:
        correct = (
            (scenario["motion"] == "up" and scenario["pole"] == "N" and choice == "N극")
            or (scenario["motion"] == "up" and scenario["pole"] == "S" and choice == "S극")
            or (scenario["motion"] == "down" and scenario["pole"] == "N" and choice == "S극")
            or (scenario["motion"] == "down" and scenario["pole"] == "S" and choice == "N극")
        )
        if correct:
            st.success("✅ 정답입니다! 자석의 움직임을 방해하려면 같은 극이 생겨야 하죠.")
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("❌ 다시 생각해보세요. 렌츠의 법칙을 떠올려보세요.")

# --------------------------------
# Step 3: 유도 전류 방향 퀴즈
# --------------------------------
elif st.session_state.step == 3:
    st.markdown("### ③ 유도 전류는 어떤 방향으로 흐를까요?")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Faraday-Law_Lenz-Law_Diagram.svg/640px-Faraday-Law_Lenz-Law_Diagram.svg.png",
             caption="참고: 렌츠의 법칙 (위키미디어)", use_container_width=True)
    st.markdown("오른손 법칙을 이용해 방향을 예측해보세요!")

    if st.button("학습 완료 🎉"):
        st.session_state.step = 4
        st.rerun()

# --------------------------------
# Step 4: 완료 화면
# --------------------------------
elif st.session_state.step == 4:
    st.success("🎉 전자기 유도 학습을 완료했습니다!")
    if st.button("다른 경우 다시 보기 🔁"):
        st.session_state.prev_scenario = st.session_state.scenario
        new_scenarios = [s for s in scenarios if s != st.session_state.prev_scenario]
        st.session_state.scenario = random.choice(new_scenarios)
        st.session_state.step = 0
        st.rerun()
