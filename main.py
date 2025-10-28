import streamlit as st
import random
import uuid

st.set_page_config(page_title="전자기 유도 학습", layout="centered")

st.title("전자기 유도 학습 앱")
st.markdown("### 자석과 코일 사이의 거리가 바뀔 때 유도 전류를 확인해보세요!")

# 시나리오 정의
scenarios = {
    1: {"desc": "N극이 가까워지는 경우", "motion": "down", "pole": "N"},
    2: {"desc": "S극이 가까워지는 경우", "motion": "down", "pole": "S"},
    3: {"desc": "N극이 멀어지는 경우", "motion": "up", "pole": "N"},
    4: {"desc": "S극이 멀어지는 경우", "motion": "up", "pole": "S"},
}

# 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
if "scenario" not in st.session_state:
    st.session_state.scenario = random.choice(list(scenarios.keys()))
if "quiz1_result" not in st.session_state:
    st.session_state.quiz1_result = None
if "force_arrow_fixed" not in st.session_state:
    st.session_state.force_arrow_fixed = None

scenario = scenarios[st.session_state.scenario]


def get_scene_html(motion, pole, animate=True):
    pole_color = "red" if pole == "N" else "blue"
    move_dir = "80px" if motion == "down" else "-80px"

    arrow_color = "#4CAF50"
    arrow_size = 40
    arrow_offset_x = 70

    if motion == "down":
        arrow_svg = f"""
        <svg width="{arrow_size}" height="{arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{arrow_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; right:-{arrow_offset_x}px; top:calc(50% - {arrow_size/2}px);">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="5 12 12 19 19 12"></polyline>
        </svg>
        """
    else:
        arrow_svg = f"""
        <svg width="{arrow_size}" height="{arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{arrow_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; right:-{arrow_offset_x}px; top:calc(50% - {arrow_size/2}px);">
            <line x1="12" y1="19" x2="12" y2="5"></line>
            <polyline points="5 12 12 5 19 12"></polyline>
        </svg>
        """

    anim = f"""
    @keyframes floatMove {{
        0%   {{ transform: translateY(0); }}
        50%  {{ transform: translateY({move_dir}); }}
        80%  {{ transform: translateY(0); }}
        100% {{ transform: translateY(0); }}
    }}
    """

    coil_height = 180
    coil_top_y_svg = 130
    coil_bottom_y = coil_top_y_svg + coil_height
    wire_start_y = coil_top_y_svg + 10
    wire_end_y = coil_bottom_y - 10
    num_turns = 7
    step_y = (wire_end_y - wire_start_y) / (num_turns - 1) if num_turns > 1 else 0
    start_x = 210
    end_x = 50
    exit_x_end = start_x + 75

    external_wire_in = f"M {exit_x_end} {wire_start_y} L {start_x} {wire_start_y}"
    winding_front_segments = []
    winding_front_segments.append(f"M {start_x} {wire_start_y}")
    for i in range(num_turns):
        current_y = wire_start_y + i * step_y
        arc = f"A 80 22 0 0 1 {end_x} {current_y}"
        winding_front_segments.append(arc)
        if i < num_turns - 1:
            next_y = wire_start_y + (i + 1) * step_y
            winding_front_segments.append(f"M {start_x} {next_y}")

    winding_path_d = " ".join(winding_front_segments)
    exit_y_coil = wire_end_y
    external_wire_out = f"M {start_x} {exit_y_coil} L {exit_x_end} {exit_y_coil}"

    winding_svg = f"""
        <path d="{external_wire_in}" fill="none" stroke="#cc6600" stroke-width="3" />
        <path d="{winding_path_d}" fill="none" stroke="#cc6600" stroke-width="3" />
        <path d="{external_wire_out}" fill="none" stroke="#cc6600" stroke-width="3" />
    """

    force_arrow_size = 50
    force_arrow_stroke_width = 3
    force_arrow_color = "#E94C3D"
    force_x_pos = 105
    force_y_pos = 215

    up_opacity = 1 if st.session_state.step == 1 and st.session_state.force_arrow_fixed == 'Up' else 0
    down_opacity = 1 if st.session_state.step == 1 and st.session_state.force_arrow_fixed == 'Down' else 0

    force_up_arrow_svg = f"""
    <svg id="force-up" class="force-arrow-preview" width="{force_arrow_size}" height="{force_arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{force_arrow_color}" stroke-width="{force_arrow_stroke_width}" stroke-linecap="round" stroke-linejoin="round"
          style="position:absolute; left: {force_x_pos}px; top: {force_y_pos}px; z-index: 10; opacity:{up_opacity}; pointer-events: none; transition: opacity 0.1s;">
        <line x1="12" y1="19" x2="12" y2="5"></line>
        <polyline points="5 12 12 5 19 12"></polyline>
    </svg>
    """

    force_down_arrow_svg = f"""
    <svg id="force-down" class="force-arrow-preview" width="{force_arrow_size}" height="{force_arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{force_arrow_color}" stroke-width="{force_arrow_stroke_width}" stroke-linecap="round" stroke-linejoin="round"
          style="position:absolute; left: {force_x_pos}px; top: {force_y_pos}px; z-index: 10; opacity:{down_opacity}; pointer-events: none; transition: opacity 0.1s;">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <polyline points="5 12 12 19 19 12"></polyline>
    </svg>
    """

    html = f"""
    <div id="scene-visualization" style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px; position:relative;">
      {force_up_arrow_svg}
      {force_down_arrow_svg}
      <div style="display:flex; align-items:center; justify-content:center; position:relative; top:0;">
        <div style="
            width:80px; height:160px;
            background:#ccc; border:4px solid #222; border-radius:10px;
            display:flex; align-items:flex-end; justify-content:center;
            position:relative;
            transform: translateX(-75px);
            animation:{'floatMove 3s ease-in-out infinite' if animate else 'none'};">
            <div style="
                font-size:56px; font-weight:bold;
                color:{pole_color};
                margin-bottom:2px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                {pole}
            </div>
            {arrow_svg if animate else ''}
        </div>
      </div>
      <svg width="300" height="400" viewBox="0 0 300 400" style="margin-top:-20px;">
        <rect x="50" y="{coil_top_y_svg}" width="160" height="{coil_height}" fill="#ffe7a8" stroke="#b97a00" stroke-width="2"/>
        <ellipse cx="130" cy="{coil_bottom_y}" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        {winding_svg}
        <ellipse cx="130" cy="{coil_top_y_svg}" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
      </svg>
    </div>
    <style>
    {anim}
    div {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    </style>
    """
    return html


# 단계별 학습 진행
if st.session_state.step == 0:
    st.subheader("🎬 상황 관찰하기")
    st.info("랜덤으로 선택된 상황을 관찰하고, 렌츠의 법칙에 따라 코일에 유도되는 현상을 예측해 보세요.")
    st.write(f"**현재 상황:** **{scenario['desc']}**")
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
    if st.button("퀴즈 시작하기 ➡️"):
        st.session_state.step = 1
        st.session_state.quiz1_result = None
        st.session_state.force_arrow_fixed = None
        st.query_params.clear()
        st.rerun()

elif st.session_state.step == 1:
    if st.session_state.quiz1_result == "Correct":
        st.session_state.step = 2
        st.rerun()

    st.subheader("퀴즈 ①: 코일이 자석에 가하는 자기력 방향")
    correct_dir = "Up" if scenario["motion"] == "down" else "Down"
    correct_text = "위쪽(밀어냄)" if correct_dir == "Up" else "아래쪽(끌어당김)"
    st.warning("💡 렌츠의 법칙: 자속 변화를 '방해'하는 방향으로 유도 자기장이 형성됩니다.")
    st.markdown("**코일이 자석에 가하는 힘의 방향을 선택하세요 (마우스 커서를 올려 미리보기가 가능합니다):**")

    unique_key = str(uuid.uuid4())

    quiz1_full_html = f"""
    <form method="get" action="" id="quiz-form-{unique_key}">
        <div id="quiz1-interactive-container" style="display:flex; flex-direction:column; align-items:center;">
            <input type="hidden" name="choice" id="choice-input-{unique_key}" value="" />
            <input type="hidden" name="fixed_arrow" id="fixed-arrow-input-{unique_key}" value="" />
            <div id="quiz1-buttons" style="display:flex; justify-content: center; width:100%; max-width: 500px; margin: 1rem 0;">
                <div id="up-choice" class="quiz-choice-wrapper" style="width: 45%; margin-right: 10%;">
                    <button type="button" class="quiz-button" data-choice="Up">⬆️ 위쪽 힘</button>
                </div>
                <div id="down-choice" class="quiz-choice-wrapper" style="width: 45%;">
                    <button type="button" class="quiz-button" data-choice="Down">⬇️ 아래쪽 힘</button>
                </div>
            </div>
            <div id="visualization-area">
                {get_scene_html(scenario["motion"], scenario["pole"], animate=True)}
            </div>
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
            .quiz-button:hover:not(.is-active) {{
                background-color: #e0e0e0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .quiz-button.is-active {{
                box-shadow: 0 0 0 3px #1f77b4;
                background-color: #dbeafe;
            }}
            #up-choice button {{ border: 2px solid #3b82f6; }}
            #down-choice button {{ border: 2px solid #ef4444; }}
        </style>

        <script>
            const upButton = document.querySelector('#up-choice button');
            const downButton = document.querySelector('#down-choice button');
            const forceUp = document.getElementById('force-up');
            const forceDown = document.getElementById('force-down');
            const choiceInput = document.getElementById('choice-input-{unique_key}');
            const fixedArrowInput = document.getElementById('fixed-arrow-input-{unique_key}');
            const quizForm = document.getElementById('quiz-form-{unique_key}');

            // --- 마우스 오버/아웃 로직 (수정된 부분) ---
            const handleMouseOver = (forceElement) => {{
                if (!document.querySelector('.quiz-button.is-active')) {{
                    forceElement.style.opacity = '1';
                }}
            }};
            const handleMouseOut = (forceElement) => {{
                const isFixed = document.querySelector('.quiz-button.is-active');
                if (!isFixed) {{
                    forceElement.style.opacity = '0';
                }} else {{
                    forceElement.style.opacity = '1';
                }}
            }};

            const handleClick = (choice, forceElement, otherForceElement, buttonElement) => {{
                forceElement.style.opacity = '1';
                otherForceElement.style.opacity = '0';
                document.querySelectorAll('.quiz-button').forEach(btn => btn.classList.remove('is-active'));
                buttonElement.classList.add('is-active');
                choiceInput.value = choice;
                fixedArrowInput.value = choice;
                quizForm.submit();
            }};

            if (upButton && forceUp) {{
                upButton.addEventListener('mouseover', () => handleMouseOver(forceUp));
                upButton.addEventListener('mouseout', () => handleMouseOut(forceUp));
                upButton.addEventListener('click', () => {{
                    handleClick('Up', forceUp, forceDown, upButton);
                }});
            }}
            if (downButton && forceDown) {{
                downButton.addEventListener('mouseover', () => handleMouseOver(forceDown));
                downButton.addEventListener('mouseout', () => handleMouseOut(forceDown));
                downButton.addEventListener('click', () => {{
                    handleClick('Down', forceDown, forceUp, downButton);
                }});
            }}

            const fixedState = "{st.session_state.force_arrow_fixed}";
            if (fixedState === 'Up') {{
                forceUp.style.opacity = '1';
                upButton.classList.add('is-active');
            }} else if (fixedState === 'Down') {{
                forceDown.style.opacity = '1';
                downButton.classList.add('is-active');
            }}
        </script>
    </form>
    """

    st.components.v1.html(quiz1_full_html, height=620)

    query_params = st.query_params
    chosen_dir = query_params.get("choice")
    fixed_arrow = query_params.get("fixed_arrow")

    if fixed_arrow and st.session_state.force_arrow_fixed != fixed_arrow:
        st.session_state.force_arrow_fixed = fixed_arrow
        if "fixed_arrow" in st.query_params:
            del st.query_params["fixed_arrow"]
        st.rerun()

    if chosen_dir and st.session_state.quiz1_result is None:
        if chosen_dir == correct_dir:
            st.session_state.quiz1_result = "Correct"
            st.session_state.step = 2
            st.success("✅ 정답입니다! 가까워지는 것을 막으려 밀어내고, 멀어지는 것을 막으려 끌어당기는 힘이 작용합니다.")
            if "choice" in st.query_params:
                del st.query_params["choice"]
            st.rerun()
        else:
            st.session_state.quiz1_result = "Incorrect"
            st.error(f"❌ 오답이에요. 정답은 **{correct_text}**입니다. 다시 시도해 보세요.")
            if "choice" in st.query_params:
                del st.query_params["choice"]
            st.rerun()

    if st.session_state.quiz1_result == "Incorrect":
        st.error(f"❌ 오답이에요. 정답은 **{correct_text}**입니다. 다시 시도해 보세요.")

    st.markdown("---")
    if st.button("다음으로 넘어가기 ⏭️"):
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.subheader("퀴즈 ②: 코일의 윗면 자극은?")
    st.session_state.force_arrow_fixed = None
    if scenario["motion"] == "down":
        top_pole = scenario["pole"]
    else:
        top_pole = "S" if scenario["pole"] == "N" else "N"
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
    options = ["윗면이 N극", "윗면이 S극"]
    answer2 = st.radio("코일의 윗면 자극을 선택하세요", options)
    if st.button("정답 확인 및 다음 단계 ➡️"):
        if answer2 == f"윗면이 {top_pole
