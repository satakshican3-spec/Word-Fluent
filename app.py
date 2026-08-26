import streamlit as st

st.set_page_config(
    page_title="WordFluent",
    page_icon="🎙️",
    layout="wide",
)

st.title("📖🎙️ WordFluent")
st.subheader("Play. Practise. Pronounce.")

st.write(
    "Learn languages through fun games and pronunciation practice."
)

language = st.selectbox(
    "Which language would you like to learn?",
    [
        "English",
        "French",
        "Spanish",
        "Hindi",
        "Bengali",
        "Korean",
        "Japanese",
    ],
)

if st.button("Start learning"):
    st.success(
        f"Great choice! Your {language} learning journey starts here."
    )