import streamlit as st
import google.generativeai as genai
from keywords import KEYWORDS  

genai.configure(api_key="AIzaSyBcLBvfn49kChzPIeF9L4RJ7b9yut8y7N0") #API_KEY_FREE_DONT_WORRY =)))))aaaaaaaaaaaaaaaaaaaaaaa

def init_session_state():
    if "chat" not in st.session_state:
        st.session_state.chat = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

def initialize_model():
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-002",
            generation_config={
                "temperature": 0.9,
                "top_p": 0.9,
                "max_output_tokens": 780,  
            },
        )
        return model
    except Exception as e:
        st.error(f"Lỗi khi khởi tạo mô hình: {str(e)}")
        return None

def ask_question(prompt):
    try:
        if any(keyword in prompt.lower() for keyword in KEYWORDS):
            if st.session_state.chat is None:
                st.session_state.chat = initialize_model().start_chat(history=[])
            response = st.session_state.chat.send_message(prompt)
            return response.text.strip()
        else:
            return "❌ Tôi không thuộc chuyên môn này. Vui lòng hỏi về gym hoặc chế độ dinh dưỡng."
    except Exception as e:
        st.error(f"Lỗi khi gửi câu hỏi: {str(e)}")
        return "❌ Có lỗi xảy ra khi xử lý câu hỏi của bạn."
#---------
def main():
    st.set_page_config(page_title="🏋️‍♂️ PT Chatbot", page_icon="🤖", layout="wide")

    st.markdown(
    """
    <style>
    .css-1v0mbdj {
        background-color: #FDCF76 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    init_session_state()

    st.title("🏋️‍♂️ Chatbot hướng dẫn về thể hình chuyên nghiệp")
    st.sidebar.markdown("BOT CHAT PT v1.4")
    selected_mode = st.sidebar.radio(
        "Các Chức Năng Chính",
        options=["Gợi ý bài tập", "Tư vấn dinh dưỡng", "Trò chuyện với PT"],
        key="selected_mode",
    )

    # ***Gợi ý bài tập
    if selected_mode == "Gợi ý bài tập":
        st.header("📋 Gợi ý bài tập")
        muscle_group = st.selectbox("Chọn nhóm cơ", ["Tay", "Vai", "Ngực", "Bụng", "Chân"," Mông ", "Giảm mỡ bụng", "Cardio"], key="muscle_group")
        if st.button("Xác nhận nhóm cơ"):
            response = ask_question(f"Gợi ý bài tập cho nhóm cơ {muscle_group}.")
            st.session_state.messages.append({"role": "assistant", "content": response})

    # ***Tư vấn dinh dưỡng
    elif selected_mode == "Tư vấn dinh dưỡng":
        st.header("🍎 Tư vấn chế độ dinh dưỡng")
        weight = st.number_input("Nhập cân nặng (kg):", min_value=60, max_value=200, step=1, key="weight")
        height = st.number_input("Nhập chiều cao (cm):", min_value=170, max_value=250, step=1, key="height")
        age = st.number_input("Nhập độ tuổi:", min_value=10, max_value=100, step=1, key="age")
        goal = st.selectbox("Mục tiêu của bạn:", ["Giảm cân", "Tăng cân", "Duy trì cân nặng"], key="goal")

        if st.button("Tư vấn chế độ dinh dưỡng"):
            response = ask_question(
                f"Tôi nặng {weight}kg, cao {height}cm, {age} tuổi, và muốn {goal.lower()}. Hãy tư vấn chế độ dinh dưỡng cho tôi 1 cách ngắn gọn và đưa ra thực đơn 3 bữa tôi nên ăn trong ngày."
            )
            st.session_state.messages.append({"role": "assistant", "content": response})

    # ***Trò chuyện với PT
    elif selected_mode == "Trò chuyện với PT":
        st.header("💬 Trò chuyện với PT")
        user_message = st.text_input("Nhập câu hỏi của bạn:", key="user_input")
        if st.button("Gửi câu hỏi"):
            response = ask_question(user_message)
            st.session_state.messages.append({"role": "user", "content": user_message})
            st.session_state.messages.append({"role": "assistant", "content": response})
#------------------
    st.markdown("---")
    st.header("📜 Lịch sử trò chuyện")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if st.button("🗑️ Xóa lịch sử trò chuyện"):
        st.session_state.messages = []
        st.success("Lịch sử trò chuyện đã được xóa.")
###------ @@
    st.sidebar.markdown(
        """
        <br><br>
        <p style="font-size: 10px; color: gray; text-align: center;">
            &copy; 2024 PT Chatbot made by plgztn.
        </p>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
#v1.4.5 update 11/19/2024-
