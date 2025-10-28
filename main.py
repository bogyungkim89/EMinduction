import streamlit as st
import random
import uuid

st.set_page_config(page_title="전자기 유도 학습", layout="centered")

st.title("🧲 전자기 유도 학습 앱")
st.markdown("### 자석이 고리 중심 위에서 반복적으로 움직이는 모습을 관찰하세요!")

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
if "force_arrow_fixed" not in st.session_state:
    st.session_state.force_arrow_fixed = None
if "quiz1_choice" not in st.session_state:
    st.session_state.quiz1_choice = None
if "quiz2_choice" not in st.session_state:
    st.session_state.quiz2_choice = None
if "quiz2_correct" not in st.session_state:
    st.session_state.quiz2_correct = False
if "quiz3_choice" not in st.session_state:
    st.session_state.quiz3_choice = None
if "quiz3_correct" not in st.session_state:
    st.session_state.quiz3_correct = False


scenario = scenarios[st.session_state.scenario]


def get_scene_html(motion, pole, animate=True):
    """
    자석의 움직임과 극성을 시각화하는 HTML/CSS 코드를 생성하여 반환합니다.
    원통과 감긴 도선 대신 타원형 고리를 사용합니다.
    """
    pole_color = "red" if pole == "N" else "blue"
    move_dir = "80px" if motion == "down" else "-80px"
    
    # --- 화살표 SVG 정의 (자석 운동 방향) --- (기존과 동일)
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
    
    # --- 유도력 화살표 (퀴즈 1 선택 결과) --- (기존과 동일)
    force_arrow_size = 50 
    force_arrow_stroke_width = 3 
    force_arrow_color = "#E94C3D"
    
    # 자석 아래, 고리 위에 위치하도록 조정
    force_x_pos = 125 
    force_y_pos = 215 # 고리 상단 위치에 맞게 조정

    fixed_arrow = st.session_state.force_arrow_fixed if st.session_state.step >= 2 else st.session_state.quiz1_choice
    
    up_opacity_initial = 1 if fixed_arrow == 'Up' else 0
    down_opacity_initial = 1 if fixed_arrow == 'Down' else 0
    
    up_fixed_class = 'fixed-arrow-visible' if up_opacity_initial == 1 else ''
    down_fixed_class = 'fixed-arrow-visible' if down_opacity_initial == 1 else ''

    force_up_arrow_svg = f"""
    <svg id="force-up" class="force-arrow-preview {up_fixed_class}" width="{force_arrow_size}" height="{force_arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{force_arrow_color}" stroke-width="{force_arrow_stroke_width}" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; left: {force_x_pos}px; top: {force_y_pos}px; z-index: 10; opacity:{up_opacity_initial}; pointer-events: none; transition: opacity 0.1s;">
            <line x1="12" y1="19" x2="12" y2="5"></line>
            <polyline points="5 12 12 5 19 12"></polyline>
    </svg>
    """

    force_down_arrow_svg = f"""
    <svg id="force-down" class="force-arrow-preview {down_fixed_class}" width="{force_arrow_size}" height="{force_arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{force_arrow_color}" stroke-width="{force_arrow_stroke_width}" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; left: {force_x_pos}px; top: {force_y_pos}px; z-index: 10; opacity:{down_opacity_initial}; pointer-events: none; transition: opacity 0.1s;">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="5 12 12 19 19 12"></polyline>
    </svg>
    """
    
    magnet_left_position = 110 

    # --- 퀴즈 3 (Step 3) 전류 방향 꺽쇠 추가 ---
    chevron_svg = ""
    if st.session_state.step >= 3 and st.session_state.quiz3_choice: # 퀴즈 3 또는 완료 단계에서 표시
        chevron = st.session_state.quiz3_choice # '>' 또는 '<'
        chevron_color = "#3498db"
        
        # 타원형 고리 앞쪽 (아래쪽) 중앙에 위치하도록 조정
        x_pos_center = 125 # 타원 중심 x
        y_pos_bottom_segment = 295 # 타원 아래쪽 segment y (대략적인 값)
        
        # 꺽쇠의 모양 정의 (SVG path)
        if chevron == '>':
            # 오른쪽으로 향하는 전류
            chevron_path = "M 12 5 L 19 12 L 12 19" 
        else:
            # 왼쪽으로 향하는 전류
            chevron_path = "M 19 5 L 12 12 L 19 12" # 화살표 머리 모양을 위해 조정
            
        # 꺽쇠가 고리 위에 겹치도록 SVG 태그 생성
        chevron_svg = f"""
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{chevron_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; left: {x_pos_center-12}px; top: {y_pos_bottom_segment-12}px; z-index: 10; pointer-events: none;">
            <path d="{chevron_path}"></path>
        </svg>
        """
    
    # --- 타원형 고리 정의 ---
    ring_center_x = 130
    ring_center_y = 290
    ring_radius_x = 100 # 가로 반지름
    ring_radius_y = 35 # 세로 반지름 (비스듬히 보이도록)
    ring_stroke_width = 5
    ring_color = "#cc6600" # 구리색
    
    # 퀴즈 2 N/S 버튼 위치 조정 (타원형 고리 위)
    quiz2_buttons_html = ""
    if st.session_state.step == 2:
        button_style = """
            width: 50px; height: 35px; border-radius: 5px; 
            font-size: 18px; font-weight: bold; cursor: pointer;
            position: absolute; top: 190px; z-index: 50; /* 고리 위에 위치하도록 top 조정 */
            border: 2px solid; transition: all 0.1s;
        """
        n_button_style = f"{button_style} left: 100px; background-color: #ffcccc; color: red; border-color: red;"
        s_button_style = f"{button_style} left: 155px; background-color: #ccccff; color: blue; border-color: blue;"
        
        if st.session_state.quiz2_choice == 'N':
             n_button_style += " box-shadow: 0 0 0 3px #ff0000; background-color: #ffaaaa;"
        elif st.session_state.quiz2_choice == 'S':
             s_button_style += " box-shadow: 0 0 0 3px #0000ff; background-color: #aaaaff;"
             
        quiz2_buttons_html = f"""
            <div id="quiz2-choice-buttons" style="position: absolute; width: 300px; height: 160px; pointer-events: none;">
                <button type="button" 
                    onclick="window.location.href = '?choice2=N'"
                    style="{n_button_style} pointer-events: auto;">
                    N
                </button>
                <button type="button" 
                    onclick="window.location.href = '?choice2=S'"
                    style="{s_button_style} pointer-events: auto;">
                    S
                </button>
            </div>
        """

    html = f"""
    <div id="scene-visualization" style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px; position:relative; width: 300px; margin-left: auto; margin-right: auto;">
        
      {force_up_arrow_svg}
      {force_down_arrow_svg}
      {chevron_svg}
      {quiz2_buttons_html if st.session_state.step == 2 else ''} {/* 퀴즈 2에서만 N/S 버튼 표시 */}
        
      <div style="position:relative; width:300px; height:160px; display:flex; justify-content:center;">
        <div style="
            width:80px; height:160px;
            background:#ccc; border:4px solid #222; border-radius:10px;
            display:flex; align-items:flex-end; justify-content:center;
            position:absolute;
            left: {magnet_left_position}px;
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

      <svg width="300" height="400" viewBox="0 0 300 400" style="margin-top:-
