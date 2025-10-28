    # --- 수정된 첫 번째 퀴즈 HTML ---
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

            function showArrow(dir) {{
                if (dir === 'Up') forceUp.style.opacity = '1';
                else forceDown.style.opacity = '1';
            }}
            function hideArrow() {{
                forceUp.style.opacity = '0';
                forceDown.style.opacity = '0';
            }}

            function handleClick(dir) {{
                // 판정
                if (dir === correctDir) {{
                    // Streamlit에 메시지 전달 (정답 → step 2)
                    window.parent.postMessage({{ isCorrect: true }}, '*');
                }} else {{
                    window.parent.postMessage({{ isCorrect: false }}, '*');
                }}
            }}

            upButton.addEventListener('mouseover', () => showArrow('Up'));
            upButton.addEventListener('mouseout', hideArrow);
            downButton.addEventListener('mouseover', () => showArrow('Down'));
            downButton.addEventListener('mouseout', hideArrow);

            upButton.addEventListener('click', () => handleClick('Up'));
            downButton.addEventListener('click', () => handleClick('Down'));
        </script>
    </div>
    """
    st.components.v1.html(quiz1_full_html, height=620)

    # JS 메시지 수신 → Streamlit Python 측 반응
    msg = st.experimental_get_query_params().get("msg")
