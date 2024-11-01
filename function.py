import streamlit as st
import google.generativeai as genai
import tempfile
import base64

model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['parts'])

def generate(uploaded_file):
    if uploaded_file is not None:

        encoded_image = base64.b64encode(uploaded_file.read()).decode()
        st.session_state.uploaded_image = encoded_image
        msg = {
            'role': 'user',
            'parts': encoded_image
        }
        st.session_state.messages.append(msg)

        with st.chat_message('user'):
            st.image(uploaded_file, width=320)

        with st.chat_message('assistant'):
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                my_file = genai.upload_file(tmp_file.name, mime_type=uploaded_file.type)  # Specify mime_type
                try:
                    result = model.generate_content(
                        [my_file, "\n\n",
                         "Can you tell me what alphabet is it in American Sign Language? Please answer with format The detected letter is {letter}"]
                    )
                    response_content = st.write(result.text)
                except:
                    response_content = st.write("Please submit a valid image")


        # with st.chat_message('assistant'):
        #     response_content = st.write(result.text)

        st.session_state.messages.append(
            {"role": 'assistant',
             "parts": response_content}
        )