import streamlit as st
import google.generativeai as genai
import tempfile
import base64
import cv2
import numpy as np
from PIL import Image

# Модель Gemini
model = genai.GenerativeModel("gemini-1.5-flash")

# Детектор лиц
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Состояние чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение старых сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])


def generate(uploaded_file):
    if uploaded_file is not None:

        # Конвертация изображения в OpenCV формат
        image = Image.open(uploaded_file).convert("RGB")
        cv_image = np.array(image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            # Размытие найденных лиц
            for x, y, w, h in faces:
                face_region = cv_image[y : y + h, x : x + w]
                blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
                cv_image[y : y + h, x : x + w] = blurred_face

            # Конвертация обратно в PIL и создание нового файла
            blurred_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            st.warning("⚠️ Face detected and blurred for privacy.")
            st.image(blurred_image, width=320)

            # Сохранение размытого изображения для генерации
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                blurred_image.save(tmp_file.name)
                gen_file = genai.upload_file(tmp_file.name, mime_type="image/png")
        else:
            # Нет лица — используем исходный файл
            uploaded_file.seek(0)
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                gen_file = genai.upload_file(
                    tmp_file.name, mime_type=uploaded_file.type
                )
            st.image(image, width=320)

        st.session_state.uploaded_image = "Image Uploaded"
        st.session_state.messages.append({"role": "user", "parts": "Image uploaded"})

        # Ответ от Gemini
        with st.chat_message("assistant"):
            try:
                result = model.generate_content(
                    [
                        gen_file,
                        "\n\n",
                        "Can you tell me what alphabet is it in American Sign Language? Please answer with format The detected letter is {letter}",
                    ]
                )
                st.write(result.text)
                st.session_state.messages.append(
                    {"role": "assistant", "parts": result.text}
                )
            except:
                st.write("Please submit a valid image")


def generate_for_comparison(uploaded_file):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file.flush()

            try:
                my_file = genai.upload_file(tmp_file.name, mime_type=uploaded_file.type)
                result = model.generate_content(
                    [
                        my_file,
                        "\n\n",
                        "What letter is this in American Sign Language? Just return the letter.",
                    ]
                )
                return result.text.strip()
            except Exception as e:
                return None
