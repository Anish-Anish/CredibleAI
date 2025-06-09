import streamlit as st
from fake_news_detector import detect_fake_news
from PyPDF2 import PdfReader

st.set_page_config(page_title="📰 Fake News Detector", layout="centered")
st.title("🧠 Fake News Detector")
st.markdown("Supports 📄 files and  saves history.")

# Setup chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ========== INPUT METHODS ==========
st.subheader("Input Methods")

#  File Upload
uploaded_file = st.file_uploader("📄 Upload a .txt or .pdf file", type=["txt", "pdf"])
file_text = ""
if uploaded_file:
    if uploaded_file.type == "text/plain":
        file_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        file_text = "\n".join([page.extract_text() or "" for page in reader.pages])

#  Manual Text
user_input = st.text_area("✍️ Or type news content", height=150, value=file_text)

# ========== SUBMIT ==========
if st.button("🚀 Detect Fake or Real"):
    if user_input.strip() == "":
        st.warning("Please provide some news content.")
    else:
        with st.spinner("Analyzing..."):
            result = detect_fake_news(user_input)

        verdict = result.get("verdict", "Error")
        confidence = result.get("confidence", 0)
        reason = result.get("reason", "No explanation provided.")
        emoji = "✅" if verdict.lower() == "real" else "🔥" if verdict.lower() == "fake" else "❓"

        message = f"{emoji} **{verdict.upper()}**\n\n📊 Confidence: **{confidence}%**\n\n🧠 Reason: _{reason}_"
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI", message))

# ========== HISTORY ==========
st.subheader("💬 Chat History")
for sender, msg in st.session_state.chat_history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(msg)

#   Save History
if st.download_button(
    "💾 Download Chat History",
    data="\n\n".join(f"{s}: {m}" for s, m in st.session_state.chat_history),
    file_name="chat_history.txt",
):
    st.success("Saved chat history!")
