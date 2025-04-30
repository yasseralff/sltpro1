import streamlit as st
import google.generativeai as genai
import tempfile
import base64
import cv2
import numpy as np
from PIL import Image
import mediapipe as mp

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Initialize hand detector (MediaPipe)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5
)


def enhance_image(pil_image):
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0)
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    return Image.fromarray(enhanced_img)


def hand_detected(pil_image):
    pil_image = enhance_image(pil_image)
    cv_image = np.array(pil_image.convert("RGB"))
    results = hands.process(cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR))
    return results.multi_hand_landmarks is not None


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])


def generate(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")

        if not hand_detected(image):
            st.error("\U0001f6d1 No hand detected! Please retake the photo.")
            return

        cv_image = np.array(image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            for x, y, w, h in faces:
                face_region = cv_image[y : y + h, x : x + w]
                blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
                cv_image[y : y + h, x : x + w] = blurred_face

            blurred_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            st.warning("Face detected and blurred for privacy.")
            st.image(blurred_image, width=320)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                blurred_image.save(tmp_file.name)
                gen_file = genai.upload_file(tmp_file.name, mime_type="image/png")
        else:
            uploaded_file.seek(0)
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                gen_file = genai.upload_file(
                    tmp_file.name, mime_type=uploaded_file.type
                )
            st.image(image, width=320)

        st.session_state.uploaded_image = "Image Uploaded"
        st.session_state.messages.append({"role": "user", "parts": "Image uploaded"})

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
        image = Image.open(uploaded_file).convert("RGB")
        if not hand_detected(image):
            return "No hand detected."

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
            except Exception:
                return None
