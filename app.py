import streamlit as st
import random
import re

# 문제 로딩 함수
@st.cache_data
def load_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    question_blocks = content.strip().split('\n\n')
    questions = []

    for block in question_blocks:
        lines = block.strip().split('\n')
        if len(lines) < 6:
            continue
        q_text = lines[0].split('. ', 1)[1]
        options = [line[3:].strip() for line in lines[1:5]]
        answer_line = lines[5]
        answer_char = re.search(r'Answer:\s*([A-D])', answer_line).group(1)
        answer_index = 'ABCD'.index(answer_char)
        questions.append({
            'question': q_text,
            'options': options,
            'answer': answer_index
        })
    random.shuffle(questions)
    return questions

# 퀴즈 앱
def quiz_app():
    st.title("🧠 머신러닝 퀴즈")
    st.markdown("문제를 풀고 얼마나 기억하고 있는지 확인해보세요!")

    if 'questions' not in st.session_state:
        st.session_state.questions = load_questions("문제,답.txt")
        st.session_state.index = 0
        st.session_state.score = 0

    questions = st.session_state.questions
    index = st.session_state.index

    if index < len(questions):
        q = questions[index]
        st.subheader(f"문제 {index+1}/{len(questions)}")
        st.write(q['question'])

        choice = st.radio("보기", q['options'], index=None, key=index)

        if st.button("다음 ▶"):
            if choice is None:
                st.warning("보기를 선택해주세요!")
            else:
                correct = q['options'][q['answer']]
                if choice == correct:
                    st.session_state.score += 1
                    st.success("정답입니다! 🎉")
                else:
                    st.error(f"틀렸습니다. 정답: {correct}")
                st.session_state.index += 1
                st.experimental_rerun()
    else:
        st.success("퀴즈 완료! 🎉")
        st.metric(label="총 점수", value=f"{st.session_state.score} / {len(questions)}")
        st.metric(label="정답률", value=f"{(st.session_state.score/len(questions))*100:.2f}%")
        if st.button("다시 풀기 🔄"):
            del st.session_state.questions
            st.experimental_rerun()

if __name__ == "__main__":
    quiz_app()
