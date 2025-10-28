import streamlit as st
import random

st.set_page_config(page_title="전자기 유도 학습", layout="centered")

st.title("🧲 전자기 유도 학습 앱")
st.markdown("### 자석이 코일 중심 위에서 반복적으로 움직이는 모습을 관찰하세요!")

# 시나리오 정의
# 1: N극이 가까워짐 (down, N)
# 2: S극이 가까워짐 (down, S)
# 3: N극이 멀어짐 (up, N)
# 4: S극이 멀어짐 (up, S)
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
    # 딕셔너리의 키 중에서 랜덤으로 시나리오 선택
    st.session_state.scenario = random.choice(list(scenarios.keys()))

scenario = scenarios[st.session_state.scenario]


def draw_scene(motion, pole, animate=True):
    """
    자석의 움직임과 극성을 시각화하는 HTML/CSS 코드를 생성하여 Streamlit에 렌더링합니다.
    자석의 움직임은 CSS 애니메이션으로 구현됩니다.
    """
    pole_color = "red" if pole == "N" else "blue"
    
    # 자석이 가까워지는 경우 (down)는 아래로 80px 이동, 멀어지는 경우 (up)는 위로 -80px 이동
    move_dir = "80px" if motion == "down" else "-80px"
    
    # 화살표 SVG 정의
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
    
    # 자석의 색깔, 극성, 애니메이션을 포함한 HTML 구조
    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px;">
        
      <!-- 자석 컨테이너 --><div style="display:flex; align-items:center; justify-content:center; position:relative; top:0;">
        <div style="
            width:80px; height:160px;
            background:#ccc; border:4px solid #222; border-radius:10px;
            display:flex; align-items:flex-end; justify-content:center;
            position:relative;
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

      <!-- 코일 (SVG를 사용하여 입체적으로 표현) --><svg width="260" height="240" viewBox="0 0 260 240" style="margin-top:-20px;">
        <!-- 코일 윗면 타원 --><ellipse cx="130" cy="130" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        <!-- 코일 몸통 사각형 --><rect x="50" y="130" width="160" height="60" fill="#ffe7a8" stroke="#b97a00" stroke-width="2"/>
        <!-- 코일 아랫면 타원 --><ellipse cx="130" cy="190" rx="80" ry="22" fill="#ffdf91" stroke="#b97a00" stroke-width="2"/>
        <!-- 코일 감은 선 (반복) -->{"".join([f'<line x1="50" y1="{135+i*5}" x2="210" y2="{135+i*5}" stroke="#cc6600" stroke-width="2"/>' for i in range(10)])}
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
    st.components.v1.html(html, height=520)


# 단계별 학습 진행
if st.session_state.step == 0:
    st.subheader("🎬 상황 관찰하기")
    st.info("랜덤으로 선택된 상황을 관찰하고, 렌츠의 법칙에 따라 코일에 유도되는 현상을 예측해 보세요.")
    st.write(f"**현재 상황:** **{scenario['desc']}**")
    draw_scene(scenario["motion"], scenario["pole"], animate=True)
    if st.button("퀴즈 시작하기 ➡️"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.subheader("퀴즈 ①: 코일이 자석에 가하는 자기력 방향")
    draw_scene(scenario["motion"], scenario["pole"], animate=False)
    
    # 렌츠의 법칙: 변화를 방해하는 방향으로 자기력 작용
    correct = "위쪽(밀어냄)" if scenario["motion"] == "down" else "아래쪽(끌어당김)"
    
    st.warning("💡 렌츠의 법칙: 자속 변화를 '방해'하는 방향으로 유도 자기장이 형성됩니다.")
    options = ["위쪽(밀어냄)", "아래쪽(끌어당김)"]
    answer1 = st.radio("코일이 자석에 가하는 힘의 방향을 선택하세요", options)
    
    if st.button("정답 확인 및 다음 단계 ➡️"):
        if answer1 == correct:
            st.session_state.step = 2
            st.success("✅ 정답입니다! 가까워지는 것을 막으려 밀어내고, 멀어지는 것을 막으려 끌어당기는 힘이 작용합니다.")
        else:
            st.error(f"❌ 오답이에요. 자석의 움직임을 **방해**하는 방향으로 힘이 작용해야 해요. 정답은 **{correct}**입니다.")
        st.rerun()

elif st.session_state.step == 2:
    st.subheader("퀴즈 ②: 코일의 윗면 자극은?")
    draw_scene(scenario["motion"], scenario["pole"], animate=False)

    # 유도되는 극성 계산 (퀴즈 1의 결과와 일치)
    if scenario["motion"] == "down": # 가까워지면 밀어내야 하므로 같은 극
        top_pole = scenario["pole"]
        explanation = f"자석의 {scenario['pole']}극이 가까워지므로, 코일 윗면은 **밀어내기 위해** 같은 극인 {top_pole}극이 됩니다."
    else: # 멀어지면 끌어당겨야 하므로 반대 극
        top_pole = "S" if scenario["pole"] == "N" else "N"
        explanation = f"자석의 {scenario['pole']}극이 멀어지므로, 코일 윗면은 **끌어당기기 위해** 반대 극인 {top_pole}극이 됩니다."

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
    draw_scene(scenario["motion"], scenario["pole"], animate=False)

    # 앙페르/오른손 법칙으로 전류 방향 계산
    # 윗면이 N극 -> 반시계방향 (N극을 엄지손가락으로 감싸면)
    # 윗면이 S극 -> 시계방향 (S극을 엄지손가락으로 감싸면)
    if (scenario["motion"] == "down" and scenario["pole"] == "N") or (scenario["motion"] == "up" and scenario["pole"] == "S"):
        current = "반시계방향" # 윗면이 N극인 경우
    else:
        current = "시계방향" # 윗면이 S극인 경우
        
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
    draw_scene(scenario["motion"], scenario["pole"], animate=False)
    
    if st.button("새로운 상황으로 다시 시작"):
        st.session_state.step = 0
        # 이전에 풀었던 시나리오가 아닌 것을 선택 (최소한 2개 이상일 때)
        available_scenarios = [k for k in scenarios.keys() if k != st.session_state.scenario]
        if available_scenarios:
            st.session_state.scenario = random.choice(available_scenarios)
        else:
            st.session_state.scenario = random.choice(list(scenarios.keys()))
        st.rerun()
