import streamlit as st

st.set_page_config(page_title="Streamlit Quiz", page_icon="📝", layout="centered")

st.title("📝 Quizlit: Test Your Streamlit Skills")

# Questions about Streamlit
questions = [
    {
        "question": "Which command do you use in the terminal to start a Streamlit app?",
        "options": ["python app.py", "streamlit run app.py", "flask run app.py", "run app.py"],
        "answer": "streamlit run app.py",
    },
    {
        "question": "Which function is used to display text in Streamlit?",
        "options": ["st.text()", "st.write()", "st.label()", "print()"],
        "answer": "st.write()",
    },
    {
        "question": "Which Streamlit widget lets a user choose a value from a list?",
        "options": ["st.selectbox()", "st.text_input()", "st.slider()", "st.radio()"],
        "answer": "st.selectbox()",
    },
    {
        "question": "What is the purpose of `st.session_state` in Streamlit?",
        "options": [
            "To store variables across reruns",
            "To configure the app layout",
            "To install Python packages",
            "To style Streamlit widgets"
        ],
        "answer": "To store variables across reruns",
    },
    {
        "question": "Which function is used to display a DataFrame in Streamlit?",
        "options": ["st.dataframe()", "st.table()", "st.show()", "st.grid()"],
        "answer": "st.dataframe()",
    },
]

# Track state
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

total_qs = len(questions)

# Show questions only if quiz not finished
if st.session_state.q_index < total_qs:
    q = questions[st.session_state.q_index]

    st.markdown(f"**Question {st.session_state.q_index + 1} of {total_qs}**")
    st.markdown(f"### {q['question']}")

    choice = st.radio(
        "Choose your answer:",
        q["options"],
        index=q["options"].index(st.session_state.answers[st.session_state.q_index]) if st.session_state.answers[st.session_state.q_index] else 0,
        key=f"q{st.session_state.q_index}"
    )

    # Navigation buttons
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Previous", disabled=st.session_state.q_index == 0):
            st.session_state.q_index -= 1
            st.rerun()

    with col2:
        if st.button("Next"):
            # Save/Update answer
            st.session_state.answers[st.session_state.q_index] = choice

            # If correct, adjust score (recalculate fresh to avoid double count)
            st.session_state.score = sum(
                1 for i, ans in enumerate(st.session_state.answers) if ans == questions[i]["answer"]
            )

            # Move forward
            if st.session_state.q_index < total_qs - 1:
                st.session_state.q_index += 1
            else:
                st.session_state.q_index = total_qs  # mark as finished
            st.rerun()

# Results screen
else:
    st.success(f"✅ Quiz Finished! You scored {st.session_state.score} out of {total_qs}")
    st.balloons()

    # Show review
    st.subheader("📋 Review Answers")
    for i, q in enumerate(questions):
        user_ans = st.session_state.answers[i]
        correct = q["answer"]
        if user_ans == correct:
            st.write(f"**Q{i+1}: {q['question']}** ✅ Your answer: {user_ans}")
        else:
            st.write(f"**Q{i+1}: {q['question']}** ❌ Your answer: {user_ans} | ✅ Correct: {correct}")

    if st.button("Restart Quiz"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.answers = [None] * total_qs
        st.rerun()
