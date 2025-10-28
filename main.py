import streamlit as st
import random
import uuid

st.set_page_config(page_title="전자기 유도 학습", layout="centered")

st.title("🧲 전자기 유도 학습 앱")
st.markdown("### 자석이 코일 중심 위에서 반복적으로 움직이는 모습을 관찰하세요!")

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
    """
    자석의 움직임과 극성을 시각화하는 HTML/CSS 코드를 생성하여 반환합니다.
    중심축을 정렬하여 자석과 코일이 일직선상에 위치하도록 수정.
    """
    pole_color = "red" if pole == "N" else "blue"
    move_dir = "80px" if motion == "down" else "-80px"
    
    # 화살표 SVG 정의
    arrow_color = "#4CAF50"
    arrow_size = 40
    # 복구: 원래 위치 (오른쪽으로 70px 떨어짐)
    arrow_offset_x = 70
    
    if motion == "down":
        arrow_svg = f"""
        <svg width="{arrow_size}" height="{arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{arrow_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; right:-{arrow_offset_x}px; top:calc(50% - {arrow_size/2}px);"><br>
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="5 12 12 19 19 12"></polyline>
        </svg>
        """
    else:
        arrow_svg = f"""
        <svg width="{arrow_size}" height="{arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{arrow_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; right:-{arrow_offset_x}px; top:calc(50% - {arrow_size/2}px);"><br>
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
    
    # 코일 설정
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
        <path d="{external_wire_in}" fill="none" stroke="#cc6600" stroke-width="3" />
        <path d="{winding_path_d}" fill="none" stroke="#cc6600" stroke-width="3" />
        <path d="{external_wire_out}" fill="none" stroke="#cc6600" stroke-width="3" />
    """

    # 유도력 화살표 위치
    force_arrow_size = 50 
    force_arrow_stroke_width = 3 
    force_arrow_color = "#E94C3D"
    
    # 코일 중심(130px)에 맞춰 화살표 위치 계산
    # 전체 컨테이너 너비 300px, 중심 150px
    # 코일 중심 130px이므로, 절대 위치로 150px - (화살표 크기/2) = 125px
    force_x_pos = 125  # 중심 정렬
    force_y_pos = 215

    up_opacity = 1 if st.session_state.step == 1 and st.session_state.force_arrow_fixed == 'Up' else 0
    down_opacity = 1 if st.session_state.step == 1 and st.session_state.force_arrow_fixed == 'Down' else 0

    force_up_arrow_svg = f"""
    <svg id="force-up" class="force-arrow-preview" width="{force_arrow_size}" height="{force_arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{force_arrow_color}" stroke-width="{force_arrow_stroke_width}" stroke-linecap="round" stroke-linejoin="round"
          style="position:absolute; left: {force_x_pos}px; top: {force_y_pos}px; z-index: 10; opacity:{up_opacity}; pointer-events: none; transition: opacity 0.1s;"><br>
        <line x1="12" y1="19" x2="12" y2="5"></line>
        <polyline points="5 12 12 5 19 12"></polyline>
    </svg>
    """

    force_down_arrow_svg = f"""
    <svg id="force-down" class="force-arrow-preview" width="{force_arrow_size}" height="{force_arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{force_arrow_color}" stroke-width="{force_arrow_stroke_width}" stroke-linecap="round" stroke-linejoin="round"
          style="position:absolute; left: {force_x_pos}px; top: {force_y_pos}px; z-index: 10; opacity:{down_opacity}; pointer-events: none; transition: opacity 0.1s;"><br>
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <polyline points="5 12 12 19 19 12"></polyline>
    </svg>
    """
    
    # 자석 위치: 전체 컨테이너 중심(150px)에 자석 너비의 절반(40px)을 빼서 중앙 정렬
    # 복구: 원래 위치 (중심 정렬)
    magnet_left_position = 110  # 150 - 40 = 110px
    
    html = f"""
    <div id="scene-visualization" style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px; position:relative; width: 300px; margin-left: auto; margin-right: auto;"><br>
        <br>
      {force_up_arrow_svg}<br>
      {force_down_arrow_svg}<br>
        <br>
      <div style="position:relative; width:300px; height:160px; display:flex; justify-content:center;"><br>
        <div style="<br>
            width:80px; height:160px;<br>
            background:#ccc; border:4px solid #222; border-radius:10px;<br>
            display:flex; align-items:flex-end; justify-content:center;<br>
            position:absolute;<br>
            left: {magnet_left_position}px;<br>
            animation:{'floatMove 3s ease-in-out infinite' if animate else 'none'};"><br>
            <br>
            <div style="<br>
                font-size:56px; font-weight:bold; <br>
                color:{pole_color}; <br>
                margin-bottom:2px;<br>
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);"><br>
                {pole}<br>
            </div>
            {arrow_svg if animate else ''}<br>
        </div><br>
      </div><br>

      <svg width="300" height="400" viewBox="0 0 300 400" style="margin-top:-20px;"><br>
        <rect x="50" y="{coil_top_y_svg}" width="160" height="{coil_height}" fill="#ffe7a8" stroke="#b97a00" stroke-width="2"/><br>
        <ellipse cx="130" cy="{coil_bottom_y}" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/><br>
        <br>
        {winding_svg}<br>

        <ellipse cx="130" cy="{coil_top_y_svg}" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/><br>
      </svg><br>
    </div><br>

    <style><br>
    {anim}<br>
    div {{<br>
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";<br>
    }}<br>
    </style><br>
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
    st.subheader("퀴즈 ①: 코일이 자석에 가하는 자기력 방향")
    
    st.warning("💡 렌츠의 법칙: 자속 변화를 '방해'하는 방향으로 유도 자기장이 형성됩니다.")
    st.markdown("**코일이 자석에 가하는 힘의 방향을 선택하세요 (마우스 커서를 올려 미리보기가 가능합니다):**")
    
    unique_key = str(uuid.uuid4())
    
    quiz1_full_html = f"""
    <div id="quiz1-interactive-container" style="display:flex; flex-direction:column; align-items:center;"><br>
        <br>
        <div id="quiz1-buttons" style="display:flex; justify-content: center; width:100%; max-width: 500px; margin: 1rem 0;"><br>
            <div id="up-choice" class="quiz-choice-wrapper" style="width: 45%; margin-right: 10%;"><br>
                <button type="button" class="quiz-button" data-choice="Up"><br>
                    ⬆️ 위쪽 힘<br>
                </button><br>
            </div><br>
            <div id="down-choice" class="quiz-choice-wrapper" style="width: 45%;"><br>
                <button type="button" class="quiz-button" data-choice="Down"><br>
                    ⬇️ 아래쪽 힘<br>
                </button><br>
            </div><br>
        </div><br>
        <br>
        <div id="visualization-area"><br>
            {get_scene_html(scenario["motion"], scenario["pole"], animate=True)}<br>
        </div><br>
    </div><br>
    <br>
    <style><br>
        .quiz-button {{<br>
            background-color: #f0f2f6;<br>
            color: #262730;<br>
            border: 1px solid #ccc;<br>
            border-radius: 0.5rem;<br>
            padding: 0.5rem 1rem;<br>
            width: 100%;<br>
            cursor: pointer;<br>
            font-size: 1rem;<br>
            font-weight: 600;<br>
            transition: background-color 0.2s, box-shadow 0.2s;<br>
        }}<br>
        .quiz-button:hover {{<br>
            background-color: #e0e0e0;<br>
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);<br>
        }}<br>
        .quiz-button.is-active {{<br>
            box-shadow: 0 0 0 3px #1f77b4;<br>
            background-color: #dbeafe;<br>
        }}<br>
        #up-choice button {{<br>
            border: 2px solid #3b82f6;<br>
        }}<br>
        #down-choice button {{<br>
            border: 2px solid #ef4444;<br>
        }}<br>
    </style><br>
    <br>
    <script><br>
        const upButton = document.querySelector('#up-choice button');<br>
        const downButton = document.querySelector('#down-choice button');<br>
        const forceUp = document.getElementById('force-up');<br>
        const forceDown = document.getElementById('force-down');<br>
        <br>
        // 마우스 오버: 화살표 미리보기 (선택되지 않은 경우에만)<br>
        const handleMouseOver = (forceElement) => {{<br>
            if (!document.querySelector('.quiz-button.is-active')) {{<br>
                forceElement.style.opacity = '1';<br>
            }}<br>
        }};<br>
        <br>
        // 마우스 아웃: 화살표 숨기기 (선택되지 않은 경우에만)<br>
        const handleMouseOut = (forceElement) => {{<br>
            if (!document.querySelector('.quiz-button.is-active')) {{<br>
                forceElement.style.opacity = '0';<br>
            }}<br>
        }};<br>
        <br>
        // 클릭: 화살표 고정 및 버튼 활성화<br>
        const handleClick = (choice, forceElement, otherForceElement, buttonElement) => {{<br>
            // 화살표 표시 고정<br>
            forceElement.style.opacity = '1';<br>
            otherForceElement.style.opacity = '0';<br>
            <br>
            // 버튼 활성화 상태 표시<br>
            document.querySelectorAll('.quiz-button').forEach(btn => btn.classList.remove('is-active'));<br>
            buttonElement.classList.add('is-active');<br>
            <br>
            // Streamlit 상태에 저장<br>
            window.parent.postMessage({{<br>
                type: 'streamlit:setComponentValue',<br>
                value: choice<br>
            }}, '*');<br>
        }};<br>
        <br>
        // 이벤트 리스너 설정<br>
        if (upButton && forceUp) {{<br>
            upButton.addEventListener('mouseover', () => handleMouseOver(forceUp));<br>
            upButton.addEventListener('mouseout', () => handleMouseOut(forceUp));<br>
            upButton.addEventListener('click', () => {{ <br>
                handleClick('Up', forceUp, forceDown, upButton);<br>
            }});<br>
        }}<br>
        <br>
        if (downButton && forceDown) {{<br>
            downButton.addEventListener('mouseover', () => handleMouseOver(forceDown));<br>
            downButton.addEventListener('mouseout', () => handleMouseOut(forceDown));<br>
            downButton.addEventListener('click', () => {{ <br>
                handleClick('Down', forceDown, forceUp, downButton);<br>
            }});<br>
        }}<br>
        <br>
        // 초기 상태 복원 (이전에 선택한 것이 있으면)<br>
        const fixedState = "{st.session_state.force_arrow_fixed}";<br>
        if (fixedState === 'Up') {{<br>
            forceUp.style.opacity = '1';<br>
            forceDown.style.opacity = '0';<br>
            upButton.classList.add('is-active');<br>
        }} else if (fixedState === 'Down') {{<br>
            forceDown.style.opacity = '1';<br>
            forceUp.style.opacity = '0';<br>
            downButton.classList.add('is-active');<br>
        }}<br>
    </script><br>
    """
    
    # HTML 컴포넌트로부터 선택값 받기
    selected_choice = st.components.v1.html(quiz1_full_html, height=620)
    
    # 선택값이 있으면 세션에 저장
    if selected_choice and selected_choice != st.session_state.force_arrow_fixed:
        st.session_state.force_arrow_fixed = selected_choice
        st.rerun()
    
    # 다음 단계로 넘어가기 버튼
    st.markdown("---")
    if st.button("다음으로 넘어가기 ⏭️"):
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.subheader("퀴즈 ②: 코일의 윗면 자극은?")
    
    st.session_state.force_arrow_fixed = None
    
    if scenario["motion"] == "down":
        top_pole = scenario["pole"]
        explanation = f"자석의 {scenario['pole']}극이 가까워지므로, 코일 윗면은 **밀어내기 위해** 같은 극인 {top_pole}극이 됩니다."
    else:
        top_pole = "S" if scenario["pole"] == "N" else "N"
        explanation = f"자석의 {scenario['pole']}극이 멀어지므로, 코일 윗면은 **끌어당기기 위해** 반대 극인 {top_pole}극이 됩니다."

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
    
    if (scenario["motion"] == "down" and scenario["pole"] == "N") or (scenario["motion"] == "up" and scenario["pole"] == "S"):
        current = "반시계방향"
    else:
        current = "시계방향"
        
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
    
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
    
    if st.button("새로운 상황으로 다시 시작"):
        st.session_state.step = 0
        available_scenarios = [k for k in scenarios.keys() if k != st.session_state.scenario]
        if available_scenarios:
            st.session_state.scenario = random.choice(available_scenarios)
        else:
            st.session_state.scenario = random.choice(list(scenarios.keys()))
        st.session_state.quiz1_result = None
        st.session_state.force_arrow_fixed = None
        st.rerun()
