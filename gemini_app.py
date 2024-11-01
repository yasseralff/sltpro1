import streamlit as st
import google.generativeai as genai
import function

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.header('Sigra')
st.subheader('Translate your sign language')

if "messages" not in st.session_state:
    st.session_state.messages = []

# for message in function.st.session_state.messages:
#     with st.chat_message(message['role']):
#         st.markdown(message['parts'])

uploaded_file = st.file_uploader(
    '''**Upload an image file**  
    *The photo should not show the face and only the hand*  
    *only png, jpeg, webp, heic, and heif file is accepted*'''
)

function.generate(uploaded_file)








