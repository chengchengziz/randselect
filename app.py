import random
import time

import streamlit as st

from randselect.selector import random_selection

FLASH_SECONDS = 3
FLASH_INTERVAL = 0.1

st.title("Random Select")

if "names" not in st.session_state:
    st.session_state.names = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "used_names" not in st.session_state:
    st.session_state.used_names = set()
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "last_result" not in st.session_state:
    st.session_state.last_result = None

rng = random.Random()


def _add_name():
    value = st.session_state.name_input.strip()
    if value:
        st.session_state.names.append(value)
    st.session_state.name_input = ""


def _add_question():
    value = st.session_state.question_input.strip()
    if value:
        st.session_state.questions.append(value)
    st.session_state.question_input = ""


col1, col2 = st.columns(2)

with col1:
    st.subheader("Names")
    st.text_input("New name", key="name_input")
    st.button("Add name", on_click=_add_name)
    if st.session_state.names:
        st.write("\n".join(f"- {n}" for n in st.session_state.names))
    else:
        st.caption("No names added yet.")

with col2:
    st.subheader("Questions")
    st.text_input("New question", key="question_input")
    st.button("Add question", on_click=_add_question)
    if st.session_state.questions:
        st.write("\n".join(f"- {q}" for q in st.session_state.questions))
    else:
        st.caption("No questions added yet.")

st.divider()

no_repeats = st.checkbox("No repeats (within this session)", key="no_repeats")

available_names = [n for n in st.session_state.names if n not in st.session_state.used_names]
available_questions = [q for q in st.session_state.questions if q not in st.session_state.used_questions]

draw_disabled = not st.session_state.names or not st.session_state.questions
if no_repeats:
    draw_disabled = draw_disabled or not available_names or not available_questions

if st.button("Draw", disabled=draw_disabled):
    placeholder = st.empty()
    end_time = time.time() + FLASH_SECONDS
    while time.time() < end_time:
        flash_name, flash_question = random_selection(
            st.session_state.names, st.session_state.questions, rng
        )
        placeholder.markdown(f"### {flash_name} — {flash_question}")
        time.sleep(FLASH_INTERVAL)
    placeholder.empty()

    pool_names = available_names if no_repeats else st.session_state.names
    pool_questions = available_questions if no_repeats else st.session_state.questions
    chosen_name, chosen_question = random_selection(pool_names, pool_questions, rng)

    if no_repeats:
        st.session_state.used_names.add(chosen_name)
        st.session_state.used_questions.add(chosen_question)

    st.session_state.last_result = (chosen_name, chosen_question)

if no_repeats and st.session_state.names and not available_names:
    st.warning("All names are selected!")
if no_repeats and st.session_state.questions and not available_questions:
    st.warning("All questions are selected!")

if st.session_state.last_result:
    chosen_name, chosen_question = st.session_state.last_result
    st.markdown(f"## {chosen_name}, please answer: {chosen_question}")
