import streamlit as st
import random
import uuid

st.set_page_config(page_title="전자기 유도 학습", layout="centered")

st.title("🧲 전자기 유도 학습 앱")
st.markdown("### 자석이 코일 중심 위에서 반복적으로 움직이는 모습을 관찰하세요!")

# 시나리오 정의
# 1: N극이 가까워짐 (down, N)
# 2: S극이 가까워짐 (down, S)
# 3: N극이 멀어짐 (up, N)
# 4: S극이 멀어지는 경우 (up, S)
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
    # 딕셔너리의 키 중에서 랜덤으로 시나리오 선택
    st.session_state.scenario = random.choice(list(scenarios.keys()))
if "quiz1_result" not in st.session_state:
    st.session_state.quiz1_result = None

scenario = scenarios[st.session_state.scenario]


def get_scene_html(motion, pole, animate=True):
    """
    자석의 움직임과 극성을 시각화하는 HTML/CSS 코드를 생성하여 반환합니다.
    (화살표 위치 Y=215px 유지)
    """
    pole_color = "red" if pole == "N" else "blue"
    
    # 자석이 가까워지는 경우 (down)는 아래로 80px 이동, 멀어지는 경우 (up)는 위로 -80px 이동
    move_dir = "80px" if motion == "down" else "-80px"
    
    # 화살표 SVG 정의 (자석의 움직임)
    arrow_color = "#4CAF50" # 초록색 화살표
    arrow_size = 40
    arrow_offset_x = 70 # 자석 오른쪽으로 offset
    
    if motion == "down":
        # 아래를 향하는 화살표 (top에서 시작해서 아래로)
        arrow_svg = f"""
        <svg width="{arrow_size}" height="{arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{arrow_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; right:-{arrow_offset_x}px; top:calc(50% - {arrow_size/2}px);">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="5 12 12 19 19 12"></polyline>
        </svg>
        """
    else: # motion == "up"
        # 위를 향하는 화살표 (bottom에서 시작해서 위로)
        arrow_svg = f"""
        <svg width="{arrow_size}" height="{arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{arrow_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; right:-{arrow_offset_x}px; top:calc(50% - {arrow_size/2}px);">
            <line x1="12" y1="19" x2="12" y2="5"></line>
            <polyline points="5 12 12 5 19 12"></polyline>
        </svg>
        """


    # 애니메이션 정의 (3초 동안 진행하며, 50% 지점에서 최대 이동)
    anim = f"""
    @keyframes floatMove {{
        0%   {{ transform: translateY(0); }}
        50%  {{ transform: translateY({move_dir}); }}
        80%  {{ transform: translateY(0); }}
        100% {{ transform: translateY(0); }}
    }}
    """
    
    # 코일 및 전선 경로 정의 (생략 - 위치 조정과 무관)
    coil_height = 180
    coil_top_y_svg = 130 
    coil_bottom_y = coil_top_y_svg + coil_height 
    wire_start_y = coil_top_y_svg + 10  
    wire_end_y = coil_bottom_y - 10 
    num_turns = 7
    step_y = (wire_end_y - wire_start_y) / (num_turns -1) if num_turns > 1 else 0 
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
        if i < num_turns -1:
            next_y = wire_start_y + (i + 1) * step_y 
            winding_front_segments.append(f"M {start_x} {next_y}")
            
    winding_path_d = " ".join(winding_front_segments)
    exit_y_coil = wire_end_y 
    external_wire_out = f"M {start_x} {exit_y_coil} L {exit_x_end} {exit_y_coil}" 
    
    winding_svg = f"""
        <!-- 진입선 (수평 직선) --><path d="{external_wire_in}" fill="none" stroke="#cc6600" stroke-width="3" />
        <!-- 코일 감은 부분 (앞면만) --><path d="{winding_path_d}" fill="none" stroke="#cc6600" stroke-width="3" />
        <!-- 이탈선 (수평 직선) --><path d="{external_wire_out}" fill="none" stroke="#cc6600" stroke-width="3" />
    """
    # =================================================================

    # --- 유도력 화살표 위치: Y=215px ---
    force_arrow_size = 50 
    force_arrow_stroke_width = 3 
    force_arrow_color = "#E94C3D" 
    force_x_pos = 105 # X 위치: 코일 중심 (130)에 화살표 중심 (25)이 오도록 (130 - 25 = 105)
    force_y_pos = 215 # Y 위치: 215px

    # Upward force arrow
    force_up_arrow_svg = f"""
    <svg id="force-up" class="force-arrow-preview" width="{force_arrow_size}" height="{force_arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{force_arrow_color}" stroke-width="{force_arrow_stroke_width}" stroke-linecap="round" stroke-linejoin="round"
         style="position:absolute; left: {force_x_pos}px; top: {force_y_pos}px; z-index: 10; opacity:0; pointer-events: none; transition: opacity 0.1s;">
        <line x1="12" y1="19" x2="12" y2="5"></line>
        <polyline points="5 12 12 5 19 12"></polyline>
    </svg>
    """
    # Downward force arrow
    force_down_arrow_svg = f"""
    <svg id="force-down" class="force-arrow-preview" width="{force_arrow_size}" height="{force_arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{force_arrow_color}" stroke-width="{force_arrow_stroke_width}" stroke-linecap="round" stroke-linejoin="round"
         style="position:absolute; left: {force_x_pos}px; top: {force_y_pos}px; z-index: 10; opacity:0; pointer-events: none; transition: opacity 0.1s;">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <polyline points="5 12 12 19 19 12"></polyline>
    </svg>
    """
    
    # 자석의 색깔, 극성, 애니메이션을 포함한 HTML 구조
    html = f"""
    <div id="scene-visualization" style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px; position:relative;">
        
      {force_up_arrow_svg}
      {force_down_arrow_svg}
        
      <!-- 자석 컨테이너 --><div style="display:flex; align-items:center; justify-content:center; position:relative; top:0;">
        <div style="
            width:80px; height:160px;
            background:#ccc; border:4px solid #222; border-radius:10px;
            display:flex; align-items:flex-end; justify-content:center;
            position:relative;
            transform: translateX(-75px); /* 막대자석을 코일 중심축에서 왼쪽으로 추가 이동 (75px) */
            /* 애니메이션 적용: 움직임 요청 시 3초 ease-in-out 무한 반복 */
            animation:{'floatMove 3s ease-in-out infinite' if animate else 'none'};">
            
            <!-- N/S 극 표시 --><div style="
                font-size:56px; font-weight:bold; 
                color:{pole_color}; 
                margin-bottom:2px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                {pole}
            </div>
            {arrow_svg if animate else ''} <!-- 애니메이션 활성화 시에만 화살표 표시 --></div>
      </div>

      <!-- 코일 (SVG를 사용하여 입체적으로 표현) - 너비 300 유지 --><svg width="300" height="400" viewBox="0 0 300 400" style="margin-top:-20px;">
        <!-- 1. 코일 몸통 사각형 (배경) - 높이 180px (Y: 130~310) --><rect x="50" y="{coil_top_y_svg}" width="160" height="{coil_height}" fill="#ffe7a8" stroke="#b97a00" stroke-width="2"/>
        <!-- 2. 코일 아랫면 타원 (밑면) - Y=310 --><ellipse cx="130" cy="{coil_bottom_y}" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        
        <!-- 3. 코일 감은 선 (시계방향 헬릭스 및 외부 연결선) -->{winding_svg}

        <!-- 4. 코일 윗면 타원 (윗면/개구부) - Y=130 --><ellipse cx="130" cy="{coil_top_y_svg}" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
      </svg>
    </div>

    <style>
    {anim}
    /* Streamlit 기본 폰트 적용 */
    div {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    }}
    </style>
    """
    return html


# 단계별 학습 진행
if st.session_state.step == 0:
    st.subheader("🎬 상황 관찰하기")
    st.info("랜덤으로 선택된 상황을 관찰하고, 렌츠의 법칙에 따라 코일에 유도되는 현상을 예측해 보세요.")
    st.write(f"**현재 상황:** **{scenario['desc']}**")
    
    # 0단계는 기존 방식대로 HTML 렌더링
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
    
    if st.button("퀴즈 시작하기 ➡️"):
        st.session_state.step = 1
        st.session_state.quiz1_result = None # Reset result
        st.query_params.clear() # Clear any residual query params
        st.rerun()

elif st.session_state.step == 1:
    
    # --- 수정된 부분: 이미 정답을 맞힌 경우 바로 다음 단계로 전환 (안전 체크) ---
    if st.session_state.quiz1_result == "Correct":
        st.session_state.step = 2
        st.rerun()
    # -------------------------------------------------------------------------
        
    st.subheader("퀴즈 ①: 코일이 자석에 가하는 자기력 방향")
    
    # 렌츠의 법칙: 변화를 방해하는 방향으로 자기력 작용
    correct_dir = "Up" if scenario["motion"] == "down" else "Down"
    correct_text = "위쪽(밀어냄)" if correct_dir == "Up" else "아래쪽(끌어당김)"
    
    st.warning("💡 렌츠의 법칙: 자속 변화를 '방해'하는 방향으로 유도 자기장이 형성됩니다.")
    st.markdown("**코일이 자석에 가하는 힘의 방향을 선택하세요 (마우스 커서를 올려 미리보기가 가능합니다):**")
    
    unique_key = str(uuid.uuid4())
    
    # HTML Component for combined visualization, buttons, and hover logic
    quiz1_full_html = f"""
    <!-- HTML Form Submission for Streamlit state management -->
    <form method="get" action="" id="quiz-form-{unique_key}">
        <div id="quiz1-interactive-container" style="display:flex; flex-direction:column; align-items:center;">
            
            <input type="hidden" name="choice" id="choice-input-{unique_key}" value="" />
            
            <!-- 버튼 컨테이너 -->
            <div id="quiz1-buttons" style="display:flex; justify-content: center; width:100%; max-width: 500px; margin: 1rem 0;">
                <div id="up-choice" class="quiz-choice-wrapper" style="width: 45%; margin-right: 10%;">
                    <button 
                        type="button" 
                        class="quiz-button" 
                        data-choice="Up"
                    >
                        ⬆️ 위쪽 힘
                    </button>
                </div>
                <div id="down-choice" class="quiz-choice-wrapper" style="width: 45%;">
                    <button 
                        type="button" 
                        class="quiz-button" 
                        data-choice="Down"
                    >
                        ⬇️ 아래쪽 힘
                    </button>
                </div>
            </div>
            
            <!-- 시각화 영역: Force Arrow SVGs를 포함하고 있음 -->
            <div id="visualization-area">
                {get_scene_html(scenario["motion"], scenario["pole"], animate=True)}
            </div>
        </div>
        
        <style>
            /* 버튼 스타일 */
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
            #up-choice button {{
                border: 2px solid #3b82f6; /* Up color hint */
            }}
            #down-choice button {{
                border: 2px solid #ef4444; /* Down color hint */
            }}
            .quiz-choice-wrapper {{
                margin-bottom: 20px;
            }}
        </style>
        <script>
            // JS to handle hover events and control the force arrows opacity
            const upButton = document.querySelector('#up-choice button');
            const downButton = document.querySelector('#down-choice button');
            const forceUp = document.getElementById('force-up');
            const forceDown = document.getElementById('force-down');
            const choiceInput = document.getElementById('choice-input-{unique_key}');
            const quizForm = document.getElementById('quiz-form-{unique_key}');
            
            if (upButton && forceUp) {{
                upButton.addEventListener('mouseover', () => {{ forceUp.style.opacity = '1'; }});
                upButton.addEventListener('mouseout', () => {{ forceUp.style.opacity = '0'; }});
                upButton.addEventListener('click', () => {{ 
                    choiceInput.value = 'Up'; 
                    quizForm.submit();
                }});
            }}
            
            if (downButton && forceDown) {{
                downButton.addEventListener('mouseover', () => {{ forceDown.style.opacity = '1'; }});
                downButton.addEventListener('mouseout', () => {{ forceDown.style.opacity = '0'; }});
                downButton.addEventListener('click', () => {{ 
                    choiceInput.value = 'Down'; 
                    quizForm.submit();
                }});
            }}
        </script>
    </form>
    """
    
    st.components.v1.html(quiz1_full_html, height=520 + 100) # Give extra height for buttons/padding
    
    # Check for the submitted choice in query parameters
    query_params = st.query_params
    
    chosen_dir = query_params.get("choice")
    
    if chosen_dir and st.session_state.quiz1_result is None:
        # Process the selection
        if chosen_dir == correct_dir:
            st.session_state.quiz1_result = "Correct"
            st.session_state.step = 2 # Setting the next step
            st.success("✅ 정답입니다! 가까워지는 것을 막으려 밀어내고, 멀어지는 것을 막으려 끌어당기는 힘이 작용합니다. 다음 퀴즈로 넘어갑니다. (잠시 후 화면이 전환됩니다.)")
        else:
            st.session_state.quiz1_result = "Incorrect"
            st.error(f"❌ 오답이에요. 자석의 움직임을 **방해**하는 방향으로 힘이 작용해야 해요. 정답은 **{correct_text}**입니다. 다시 시도해 보세요.")
        
        # Crucial: Clear the query parameter and trigger rerun to apply state changes
        if "choice" in st.query_params:
            del st.query_params["choice"]
        st.rerun()

    # If the user answered incorrectly on a previous run, display the error message again
    if st.session_state.quiz1_result == "Incorrect":
        st.error(f"❌ 오답이에요. 자석의 움직임을 **방해**하는 방향으로 힘이 작용해야 해요. 정답은 **{correct_text}**입니다. 다시 시도해 보세요.")

elif st.session_state.step == 2:
    st.subheader("퀴즈 ②: 코일의 윗면 자극은?")
    
    # 유도되는 극성 계산 (퀴즈 1의 결과와 일치)
    if scenario["motion"] == "down": # 가까워지면 밀어내야 하므로 같은 극
        top_pole = scenario["pole"]
        explanation = f"자석의 {scenario['pole']}극이 가까워지므로, 코일 윗면은 **밀어내기 위해** 같은 극인 {top_pole}극이 됩니다."
    else: # 멀어지면 끌어당겨야 하므로 반대 극
        top_pole = "S" if scenario["pole"] == "N" else "N"
        explanation = f"자석의 {scenario['pole']}극이 멀어지므로, 코일 윗면은 **끌어당기기 위해** 반대 극인 {top_pole}극이 됩니다."

    # 시각화 HTML 렌더링
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)

    options = ["윗면이 N극", "윗면이 S극"]
    answer2 = st.radio("코일의 윗면 자극을 선택하세요", options)
    
    if st.button("정답 확인 및 다음 단계 ➡️"):
        if answer2 == f"윗면이 {top_pole}극":
            st.session_state.step = 3
            st.success("✅ 정답입니다! 이 유도 자극이 바로 퀴즈 ①의 자기력을 만들어냅니다.")
        else:
            st.error(f"❌ 오답이에요. 렌츠의 법칙에 따라 유도된 자극은 **{top_pole}극**이 되어야 합니다.")
            st.info(explanation)
        st.rerun()

elif st.session_state.step == 3:
    st.subheader("퀴즈 ③: 코일에 유도되는 전류 방향")
    
    # 앙페르/오른손 법칙으로 전류 방향 계산
    if (scenario["motion"] == "down" and scenario["pole"] == "N") or (scenario["motion"] == "up" and scenario["pole"] == "S"):
        current = "반시계방향" # 윗면이 N극인 경우
    else:
        current = "시계방향" # 윗면이 S극인 경우
        
    # 시각화 HTML 렌더링
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
        
    st.warning("💡 오른손 법칙: 유도된 자극(퀴즈 ② 결과)을 오른손 엄지손가락으로 가리키고 코일을 감싸쥐면, 네 손가락 방향이 전류의 방향입니다.")
    options = ["시계방향", "반시계방향"]
    answer3 = st.radio("전류의 방향을 선택하세요", options)
    
    if st.button("결과 보기 🎯"):
        if answer3 == current:
            st.session_state.step = 4
            st.success("✅ 최종 정답입니다! 모든 단계를 정확히 이해했어요. 전자기 유도 현상을 완벽히 이해했네요 🎉")
        else:
            st.error(f"❌ 오답이에요. 퀴즈 ②의 결과에 오른손 법칙을 적용해 보세요. 정답은 **{current}**입니다.")
        st.rerun()
        
elif st.session_state.step == 4:
    st.subheader("✅ 학습 완료")
    st.success("축하합니다! 전자기 유도 현상(렌츠의 법칙)의 세 단계를 모두 정확히 이해하고 적용했습니다.")
    st.markdown(f"**풀이한 상황:** {scenario['desc']}")
    
    # 시각화 HTML 렌더링
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
    
    if st.button("새로운 상황으로 다시 시작"):
        st.session_state.step = 0
        # 이전에 풀었던 시나리오가 아닌 것을 선택 (최소한 2개 이상일 때)
        available_scenarios = [k for k in scenarios.keys() if k != st.session_state.scenario]
        if available_scenarios:
            st.session_state.scenario = random.choice(available_scenarios)
        else:
            st.session_state.scenario = random.choice(list(scenarios.keys()))
        st.rerun()
