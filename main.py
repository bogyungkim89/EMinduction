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
    pole_color = "red" if pole == "N" else "blue"
    move_dir = "80px" if motion == "down" else "-80px"
    arrow_color = "#4CAF50"
    arrow_size = 40
    arrow_offset_x = 70

    if motion == "down":
        arrow_svg = f"""
        <svg width="{arrow_size}" height="{arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{arrow_color}" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; right:-{arrow_offset_x}px; top:calc(50% - {arrow_size/2}px);">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="5 12 12 19 19 12"></polyline>
        </svg>
        """
    else:
        arrow_svg = f"""
        <svg width="{arrow_size}" height="{arrow_size}" viewBox="0 0 24 24" fill="none" stroke="{arrow_color}" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round"
             style="position:absolute; right:-{arrow_offset_x}px; top:calc(50% - {arrow_size/2}px);">
            <line x1="12" y1="19" x2="12" y2="5"></line>
            <polyline points="5 12 12 5 19 12"></polyline>
        </svg>
        """

    anim = f"""
    @keyframes floatMove {{
        0%   {{ transform: translateY(0); }}
        50%  {{ transform: translateY({move_dir}); }}
        100% {{ transform: translateY(0); }}
    }}
    """

    coil_height = 180
    coil_top_y_svg = 130
    coil_bottom_y = coil_top_y_svg + coil_height
    wire_start_y = coil_top_y_svg + 10
    wire_end_y = coil_bottom_y - 10
    num_turns = 7
    step_y = (wire_end_y - wire_start_y) / (num_turns - 1)
    start_x = 210
    end_x = 50
    exit_x_end = start_x + 75

    external_wire_in = f"M {exit_x_end} {wire_start_y} L {start_x} {wire_start_y}"
    winding_front_segments = [f"M {start_x} {wire_start_y}"]
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

    magnet_left_position = 110
    html = f"""
    <div id="scene-visualization" style="display:flex; flex-direction:column; align-items:center; position:relative; width:300px;">
      <div style="position:relative; width:300px; height:160px; display:flex; justify-content:center;">
        <div style="
            width:80px; height:160px;
            background:#ccc; border:4px solid #222; border-radius:10px;
            display:flex; align-items:flex-end; justify-content:center;
            position:absolute;
            left:{magnet_left_position}px;
            animation:{'floatMove 3s ease-in-out infinite' if animate else 'none'};">
            <div style="font-size:56px; font-weight:bold; color:{pole_color};">{pole}</div>
            {arrow_svg if animate else ''}
        </div>
      </div>
      <svg width="300" height="400" viewBox="0 0 300 400">
        <rect x="50" y="{coil_top_y_svg}" width="160" height="{coil_height}" fill="#ffe7a8" stroke="#b97a00" stroke-width="2"/>
        <ellipse cx="130" cy="{coil_bottom_y}" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        {winding_svg}
        <ellipse cx="130" cy="{coil_top_y_svg}" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
      </svg>
    </div>
    <style>{anim}</style>
    """
    return html


# ---- 단계별 ----

if st.session_state.step == 0:
    st.subheader("🎬 상황 관찰하기")
    st.info("랜덤으로 선택된 상황을 관찰하고, 렌츠의 법칙에 따라 유도 현상을 예측해 보세요.")
    st.write(f"**현재 상황:** {scenario['desc']}")
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], True), height=520)
    if st.button("퀴즈 시작하기 ➡️"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.subheader("퀴즈①: 코일이 자석에 가하는 힘의 방향")
    st.warning("💡 렌츠의 법칙: 자속 변화를 방해하는 방향으로 유도 자기장이 형성됩니다.")
    st.markdown("**힘의 방향을 선택하세요. 클릭 시 다음 퀴즈로 넘어갑니다.**")
    unique_key = str(uuid.uuid4())

    quiz1_html = f"""
    <form id="quiz1-form-{unique_key}">
        <div style="display:flex; justify-content:center; gap:2rem;">
            <button type="button" onclick="selectChoice('Up')" style="padding:1rem; font-size:1rem;">⬆️ 위쪽 힘</button>
            <button type="button" onclick="selectChoice('Down')" style="padding:1rem; font-size:1rem;">⬇️ 아래쪽 힘</button>
        </div>
        <input type="hidden" id="choice-input" name="choice" />
        <script>
            function selectChoice(choice) {{
                const params = new URLSearchParams(window.location.search);
                params.set('choice', choice);
                params.set('next_step', '2');
                window.location.search = params.toString();
            }}
        </script>
    </form>
    <div style="margin-top:1rem;">
        {get_scene_html(scenario["motion"], scenario["pole"], True)}
    </div>
    """
    st.components.v1.html(quiz1_html, height=620)

    query_params = st.query_params
    choice = query_params.get("choice")
    if choice:
        st.session_state.step = 2
        st.query_params.clear()
        st.rerun()

elif st.session_state.step == 2:
    st.subheader("퀴즈②: 코일의 윗면 자극은?")
    if scenario["motion"] == "down":
        top_pole = scenario["pole"]
        explanation = f"자석의 {scenario['pole']}극이 가까워지므로, 코일 윗면은 **밀어내기 위해** 같은 극인 {top_pole}극이 됩니다."
    else:
        top_pole = "S" if scenario["pole"] == "N" else "N"
        explanation = f"자석의 {scenario['pole']}극이 멀어지므로, 코일 윗면은 **끌어당기기 위해** 반대 극인 {top_pole}극이 됩니다."
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], True), height=520)
    options = ["윗면이 N극", "윗면이 S극"]
    answer = st.radio("코일의 윗면 자극을 선택하세요.", options)
    if st.button("정답 확인 및 다음 단계 ➡️"):
        if answer == f"윗면이 {top_pole}극":
            st.session_state.step = 3
            st.success("✅ 정답입니다!")
        else:
            st.error(f"❌ 오답입니다. 정답은 {top_pole}극입니다.")
            st.info(explanation)
        st.rerun()

elif st.session_state.step == 3:
    st.subheader("퀴즈③: 코일에 유도되는 전류 방향")
    if (scenario["motion"] == "down" and scenario["pole"] == "N") or (scenario["motion"] == "up" and scenario["pole"] == "S"):
        correct = "반시계방향"
    else:
        correct = "시계방향"
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], True), height=520)
    st.warning("💡 오른손 법칙: 유도된 자극을 엄지손가락으로, 손가락 방향이 전류 방향입니다.")
    choice = st.radio("전류 방향을 선택하세요", ["시계방향", "반시계방향"])
    if st.button("결과 보기 🎯"):
        if choice == correct:
            st.session_state.step = 4
            st.success("✅ 정답입니다! 모든 과정을 정확히 이해했어요.")
        else:
            st.error(f"❌ 오답입니다. 정답은 **{correct}**입니다.")
        st.rerun()

elif st.session_state.step == 4:
    st.subheader("✅ 학습 완료")
    st.success("축하합니다! 전자기 유도 현상을 완벽히 이해했습니다.")
    st.markdown(f"**풀이한 상황:** {scenario['desc']}")
    st.components.v1.html(get_scene_html(scenario["motion"], scenario["pole"], True), height=520)
    if st.button("새로운 상황으로 다시 시작"):
        st.session_state.step = 0
        available = [k for k in scenarios.keys() if k != st.session_state.scenario]
        st.session_state.scenario = random.choice(available or list(scenarios.keys()))
        st.rerun()
