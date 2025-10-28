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
if "force_arrow_fixed" not in st.session_state:
    st.session_state.force_arrow_fixed = None
if "quiz1_choice" not in st.session_state:
    st.session_state.quiz1_choice = None
if "quiz2_choice" not in st.session_state:
    st.session_state.quiz2_choice = None
if "quiz2_correct" not in st.session_state:
    st.session_state.quiz2_correct = False
# 퀴즈 3 선택 (꺽쇠) 및 정답 여부 상태 추가
if "quiz3_choice" not in st.session_state:
    st.session_state.quiz3_choice = None
if "quiz3_correct" not in st.session_state:
    st.session_state.quiz3_correct = False


scenario = scenarios[st.session_state.scenario]


def get_scene_html(motion, pole, animate=True):
    """
    자석의 움직임과 극성을 시각화하는 HTML/CSS 코드를 생성하여 반환합니다.
    """
    pole_color = "red" if pole == "N" else "blue"
    move_dir = "80px" if motion == "down" else "-80px"
    
    # --- 화살표 SVG 정의 (자석 운동 방향) --- (생략: 기존 코드와 동일)
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
    
    # --- 코일 설정 ---
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
    
    # 코일 중앙에 꺽쇠를 넣기 위한 SVG 추가
    chevron_svg = ""
    if st.session_state.step == 3 and st.session_state.quiz3_choice:
        chevron = st.session_state.quiz3_choice # '>' 또는 '<'
        chevron_color = "#3498db"
        
        # 꺽쇠를 표시할 y 좌표 (대략 코일 중앙)
        y_pos = wire_start_y + 3 * step_y # 7개 턴 중 4번째 턴 근처
        
        # 코일의 좌우 곡선 중앙을 가리키는 x 좌표 (약 130)
        x_pos_center = 125
        
        # 꺽쇠의 모양 정의 (SVG path)
        if chevron == '>':
            # 오른쪽으로 향하는 전류 (시계방향의 뒤쪽에서 앞으로)
            chevron_path = "M 12 5 L 19 12 L 12 19" 
        else:
            # 왼쪽으로 향하는 전류 (반시계방향의 뒤쪽에서 앞으로)
            chevron_path = "M 19 5 L 12 12 L 19 19"
        
        # 꺽쇠가 도선 위에 겹치도록 SVG 태그 생성
        chevron_svg = f"""
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{chevron_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; left: {x_pos_center-12}px; top: {y_pos+10}px; z-index: 10; pointer-events: none;">
            <path d="{chevron_path}"></path>
        </svg>
        """


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
    # --- 유도력 화살표 (퀴즈 1 선택 결과) --- (생략: 기존 코드와 동일)
    force_arrow_size = 50 
    force_arrow_stroke_width = 3 
    force_arrow_color = "#E94C3D"
    
    force_x_pos = 125 
    force_y_pos = 215

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
    
    html = f"""
    <div id="scene-visualization" style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px; position:relative; width: 300px; margin-left: auto; margin-right: auto;">
        
      {force_up_arrow_svg}
      {force_down_arrow_svg}
      {chevron_svg} 
        
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
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    }}
    .force-arrow-preview.fixed-arrow-visible {{
        opacity: 1 !important; 
    }}
    </style>
    """
    return html

# ---
# 콜백 함수 정의
# ---

def handle_quiz1_choice(choice):
    """퀴즈 1 선택을 처리하고 다음 단계로 이동합니다."""
    st.session_state.quiz1_choice = choice
    st.session_state.force_arrow_fixed = choice
    st.session_state.step = 2
    st.session_state.quiz2_choice = None 
    st.session_state.quiz2_correct = False
    st.session_state.quiz3_choice = None
    st.session_state.quiz3_correct = False
    st.rerun()

def handle_quiz2_choice_and_next(chosen_pole):
    """퀴즈 2 선택을 처리하고 바로 퀴즈 3으로 이동합니다."""
    st.session_state.quiz2_choice = chosen_pole
    
    if scenario["motion"] == "down":
        correct_pole = scenario["pole"]
    else:
        correct_pole = "S" if scenario["pole"] == "N" else "N"

    st.session_state.quiz2_correct = (chosen_pole == correct_pole)
    
    st.session_state.step = 3
    st.rerun()

def handle_quiz3_choice_and_check(chosen_chevron):
    """퀴즈 3 선택 (꺽쇠)을 처리하고 정답 여부를 확인한 후 다음 단계로 이동합니다."""
    st.session_state.quiz3_choice = chosen_chevron
    
    # 퀴즈 2에서 유도된 자극 (top_pole) 계산
    if scenario["motion"] == "down":
        top_pole = scenario["pole"]
    else:
        top_pole = "S" if scenario["pole"] == "N" else "N"
        
    # 오른손 법칙 적용: N극(엄지 위) -> 반시계방향, S극(엄지 아래) -> 시계방향
    # 반시계방향(N극)일 때: 코일 앞쪽 도선 전류 방향은 왼쪽 (<)
    # 시계방향(S극)일 때: 코일 앞쪽 도선 전류 방향은 오른쪽 (>)
    
    if top_pole == "N":
        correct_chevron = '<' # 반시계방향
    else: # top_pole == "S"
        correct_chevron = '>' # 시계방향

    st.session_state.quiz3_correct = (chosen_chevron == correct_chevron)
    
    # 퀴즈 4 (최종 결과) 단계로 바로 이동
    st.session_state.step = 4
    st.rerun()


# ---
# 단계별 학습 진행
# ---

if st.session_state.step == 0:
    st.subheader("🎬 상황 관찰하기")
    st.info("랜덤으로 선택된 상황을 관찰하고, 렌츠의 법칙에 따라 코일에 유도되는 현상을 예측해 보세요.")
    st.write(f"**현재 상황:** **{scenario['desc']}**")
    
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
    
    if st.button("퀴즈 시작하기 ➡️"):
        st.session_state.step = 1
        st.session_state.force_arrow_fixed = None
        st.session_state.quiz1_choice = None 
        st.session_state.quiz2_choice = None
        st.session_state.quiz2_correct = False
        st.session_state.quiz3_choice = None
        st.session_state.quiz3_correct = False
        st.rerun()

elif st.session_state.step == 1:
    
    st.subheader("퀴즈 ①: 코일이 자석에 가하는 자기력 방향")
    
    st.warning("💡 **렌츠의 법칙**: 자속 변화를 **'방해'**하는 방향으로 유도 자기장이 형성됩니다.")
    st.markdown("**코일이 자석에 가하는 힘의 방향을 선택하세요:**")
    
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)

    col1, col2 = st.columns(2)
    with col1:
        st.button("⬆️ 위쪽 힘 (방해)", 
                  on_click=handle_quiz1_choice, 
                  args=('Up',), 
                  use_container_width=True,
                  key="quiz1_up")
    with col2:
        st.button("⬇️ 아래쪽 힘 (방해)", 
                  on_click=handle_quiz1_choice, 
                  args=('Down',), 
                  use_container_width=True,
                  key="quiz1_down")

elif st.session_state.step == 2:
    
    st.subheader("퀴즈 ②: 코일의 윗면 자극은?")
    
    correct_dir = "Up" if scenario["motion"] == "down" else "Down"
    chosen_dir = st.session_state.force_arrow_fixed
    
    if chosen_dir != correct_dir:
        st.error(f"❌ 퀴즈 ① 오답! 올바른 힘의 방향은 **{'위쪽' if correct_dir == 'Up' else '아래쪽'}**입니다.")
    else:
        st.success(f"✅ 퀴즈 ① 정답! 코일은 자석의 움직임을 **{'밀어내기 위해 위쪽' if chosen_dir == 'Up' else '끌어당기기 위해 아래쪽'}**으로 힘을 가합니다.")

    st.markdown("**코일 윗면에 유도되는 자극을 선택하세요 (선택 즉시 다음 단계로 이동):**")
    
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
    
    col_n, col_s = st.columns(2)
    with col_n:
        st.button("N극", 
                  on_click=handle_quiz2_choice_and_next, 
                  args=('N',), 
                  use_container_width=True, 
                  type="primary",
                  key="quiz2_N")
    with col_s:
        st.button("S극", 
                  on_click=handle_quiz2_choice_and_next, 
                  args=('S',), 
                  use_container_width=True,
                  type="primary",
                  key="quiz2_S")

elif st.session_state.step == 3:
    st.subheader("퀴즈 ③: 코일에 유도되는 전류 방향")
    
    # 퀴즈 2 피드백 제공
    if scenario["motion"] == "down":
        top_pole = scenario["pole"]
    else:
        top_pole = "S" if scenario["pole"] == "N" else "N"
        
    if st.session_state.quiz2_correct:
        st.success(f"✅ 퀴즈 ② 정답! 코일 윗면은 **{top_pole}극**이 유도되었습니다.")
    else:
        st.error(f"❌ 퀴즈 ② 오답. 렌츠의 법칙에 따라 코일 윗면은 **{top_pole}극**이 유도되어야 합니다.")
        
    st.warning("💡 **오른손 법칙**: 유도된 자극(퀴즈 ② 결과)을 오른손 엄지손가락으로 가리키고 코일을 감싸쥐세요. 네 손가락 방향이 전류의 방향입니다.")
    st.markdown("**코일 앞쪽 도선(가장 가까운 세로 선)의 전류 방향을 선택하세요 (선택 즉시 결과 보기):**")

    # 시각화 (선택 전에는 꺽쇠 없음)
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
        
    col_left, col_right = st.columns(2)
    with col_left:
        # 왼쪽 꺽쇠: 반시계방향 (코일 앞쪽 도선이 왼쪽으로 흐름)
        st.button("왼쪽 (<)", 
                  on_click=handle_quiz3_choice_and_check, 
                  args=('<',), 
                  use_container_width=True,
                  type="secondary",
                  key="quiz3_left")
    with col_right:
        # 오른쪽 꺽쇠: 시계방향 (코일 앞쪽 도선이 오른쪽으로 흐름)
        st.button("오른쪽 (>)", 
                  on_click=handle_quiz3_choice_and_check, 
                  args=('>',), 
                  use_container_width=True,
                  type="secondary",
                  key="quiz3_right")
        
elif st.session_state.step == 4:
    st.subheader("✅ 학습 완료")
    
    # 최종 결과 요약
    if scenario["motion"] == "down":
        top_pole = scenario["pole"]
    else:
        top_pole = "S" if scenario["pole"] == "N" else "N"
        
    if top_pole == "N":
        correct_chevron = '<' # 반시계
        correct_current_text = "반시계방향 (앞쪽 도선: 왼쪽 <)"
    else: # top_pole == "S"
        correct_chevron = '>' # 시계
        correct_current_text = "시계방향 (앞쪽 도선: 오른쪽 >)"
    
    # 퀴즈 3 피드백
    if st.session_state.quiz3_correct:
        st.success(f"✅ 퀴즈 ③ 최종 정답! 코일의 전류 방향은 **{correct_current_text}**입니다.")
    else:
        st.error(f"❌ 퀴즈 ③ 오답. 올바른 전류 방향은 **{correct_current_text}**입니다.")
        
    st.markdown(f"**풀이한 상황:** {scenario['desc']}")
    
    # 최종 시각화 (선택된 꺽쇠 표시)
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], animate=True), height=520)
    
    if st.button("새로운 상황으로 다시 시작"):
        st.session_state.step = 0
        available_scenarios = [k for k in scenarios.keys() if k != st.session_state.scenario]
        if available_scenarios:
            st.session_state.scenario = random.choice(available_scenarios)
        else:
            st.session_state.scenario = random.choice(list(scenarios.keys()))
        st.session_state.force_arrow_fixed = None
        st.session_state.quiz1_choice = None
        st.session_state.quiz2_choice = None
        st.session_state.quiz2_correct = False
        st.session_state.quiz3_choice = None
        st.session_state.quiz3_correct = False
        st.rerun()
