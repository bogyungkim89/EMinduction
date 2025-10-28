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
    <form method="get" action="" id="quiz-form-{unique_key}">
        <div id="quiz1-interactive-container" style="display:flex; flex-direction:column; align-items:center;">
            
            <input type="hidden" name="choice" id="choice-input-{unique_key}" value="" />
            
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
    
    # Process the selection and transition if correct
    if chosen_dir and st.session_state.quiz1_result is None:
        if chosen_dir == correct_dir:
            st.session_state.quiz1_result = "Correct"
            st.session_state.step = 2 # Setting the next step
            st.success("✅ 정답입니다! 가까워지는 것을 막으려 밀어내고, 멀어지는 것을 막으려 끌어당기는 힘이 작용합니다. 다음 퀴즈로 넘어갑니다. (잠시 후 화면이 전환됩니다.)")
            
            # Crucial: Clear the query parameter and trigger rerun to apply state changes
            if "choice" in st.query_params:
                del st.query_params["choice"]
            st.rerun() # Immediately rerun to transition to step 2
            
        else:
            st.session_state.quiz1_result = "Incorrect"
            st.error(f"❌ 오답이에요. 자석의 움직임을 **방해**하는 방향으로 힘이 작용해야 해요. 정답은 **{correct_text}**입니다. 다시 시도해 보세요.")
            
            # Clear the query parameter so the error doesn't persist on subsequent runs
            if "choice" in st.query_params:
                del st.query_params["choice"]
            st.rerun() # Rerun to display the error and re-render the quiz without the query param

    # If the user answered incorrectly on a previous run, display the error message again
    if st.session_state.quiz1_result == "Incorrect":
        st.error(f"❌ 오답이에요. 자석의 움직임을 **방해**하는 방향으로 힘이 작용해야 해요. 정답은 **{correct_text}**입니다. 다시 시도해 보세요.")

    # --- 새로 추가된 부분: 다음 단계로 넘어가는 버튼 ---
    st.markdown("---")
    if st.button("다음으로 넘어가기 ⏭️"):
        st.session_state.step = 2
        st.rerun()
    # ----------------------------------------------------
