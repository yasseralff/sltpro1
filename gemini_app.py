# app.py
import streamlit as st
import google.generativeai as genai
import function
import string
import random
import os

# Настройка API ключа
genai.configure(api_key=st.secrets["api_key"])

# Заголовки
st.header("Sigra")
st.subheader("Translate your sign language or train your gestures")

# Выбор режима
mode = st.radio("Choose mode:", ["Translate", "Train", "Train with Alphabet"])

# Состояние сессии
if "messages" not in st.session_state:
    st.session_state.messages = []

# Режим перевода
if mode == "Translate":
    uploaded_file = st.file_uploader(
        "Upload an image file",
        type=["png", "jpg", "jpeg", "webp", "heic", "heif"]
    )
    camera_image = st.camera_input("Or take a photo now")

    image_to_use = camera_image if camera_image else uploaded_file

    if image_to_use:
        function.generate(image_to_use)

# Режим тренировки по жесту
elif mode == "Train":
    if "target_letter" not in st.session_state:
        st.session_state.target_letter = random.choice(string.ascii_uppercase)
        st.session_state.score = 0
        st.session_state.attempts = 0

    st.markdown(f"### Show the letter: **{st.session_state.target_letter}**")
    train_image = st.camera_input("Take a photo with sign")

    if train_image:
        result_text = function.generate_for_comparison(train_image)

        if result_text:
            st.session_state.attempts += 1
            if st.session_state.target_letter == result_text.strip().upper():
                st.success("Correct")
                st.session_state.score += 1
            else:
                st.error(f"Incorrect. I saw: {result_text.strip()}")

            st.write(f"**Score:** {st.session_state.score} / {st.session_state.attempts}")
            if st.button("Next letter"):
                st.session_state.target_letter = random.choice(string.ascii_uppercase)

# Режим тренировки по изображениям алфавита
elif mode == "Train with Alphabet":
    alphabet = list(string.ascii_uppercase)
    if "quiz_letter" not in st.session_state:
        st.session_state.quiz_letter = random.choice(alphabet)
        st.session_state.quiz_score = 0
        st.session_state.quiz_round = 1

    st.title("Guess the Letter by Sign")

    image_path = os.path.join("images", f"{st.session_state.quiz_letter}.jpg")
    if os.path.exists(image_path):
        st.image(image_path, caption="What letter is this?", width=300)
    else:
        st.warning(f"Image not found for {st.session_state.quiz_letter}")

    user_answer = st.selectbox("Choose the letter:", alphabet)

    if st.button("Check Answer"):
        if user_answer == st.session_state.quiz_letter:
            st.success("✅ Correct!")
            st.session_state.quiz_score += 1
        else:
            st.error(f"Incorrect. It was {st.session_state.quiz_letter}")

    if st.button("Next Image"):
        st.session_state.quiz_letter = random.choice(alphabet)
        st.session_state.quiz_round += 1

    st.write(f"Round: {st.session_state.quiz_round}")
    st.write(f"Score: {st.session_state.quiz_score}")
