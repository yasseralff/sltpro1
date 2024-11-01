import streamlit as st
import google.generativeai as genai
import tempfile


genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")


st.header('ASL Translation App')

# initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# messages
# {'role': "user" or "assistant" or "system", "content": prompt or response}

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['parts'])

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    tmp_file.write(uploaded_file.read())
    my_file = genai.upload_file(tmp_file.name, mime_type=uploaded_file.type)  # Specify mime_type
    result = model.generate_content(
        [my_file, "\n\n", "Can you tell me what alphabet is it in American Sign Language? Please answer with format Alphabet: the answer"]
    )

    response_content = st.write(result.text)
    st.session_state.messages.append(
        {"role": 'assistant',
         "parts": response_content}
    )

if prompt:=st.chat_input("Message"):
    msg = {
        'role': 'user',
        'parts': prompt
    }
    st.session_state.messages.append(msg)

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):

        response = model.generate_content(st.session_state.messages)
        response_content = st.write(response.text)

    st.session_state.messages.append(
        {"role": 'assistant',
         "parts": response_content}
    )







