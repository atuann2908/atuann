import streamlit as st

st.set_page_config(page_title="ATuann", page_icon="👨‍💻", layout="wide")

hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.title("Hé Lô Mấy Ní")
st.write("🍌Vô vọc mấy cái t làm cho vui.")

# Ảnh đại diện (nếu có ảnh online)
#st.image("https://i.imgur.com/xxxxxxxx.png", width=200)

st.header("📌 Những thứ t làm")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Hệ Thống Quản Lí Giáo Dục 🎓")
    st.write("Đây là hệ thống quản lí giáo dục dành cho giáo viên, phụ huynh và học sinh..")
    if st.button("🔗 Xem dự án 1", use_container_width=True):
        st.switch_page("pages/project_1.py")

with col2:
    st.subheader(" Ghép ảnh skin Liên Quân")
    st.write("Tool ghép ảnh tùy chọn, hiển thị đẹp trên web.")
    if st.button("🔗 Xem dự án 2", use_container_width=True):
        st.switch_page("pages/project_2.py")

with col3:
    st.subheader(".....")
    st.write(".....")
    if st.button("🔗 Xem dự án 3", use_container_width=True):
        st.switch_page("pages/project_3.py")