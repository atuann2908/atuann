import streamlit as st

st.set_page_config(page_title="ATuann", page_icon="👨‍💻", layout="wide")

st.title("Hé Lô Mấy Ní")
st.write("🍌Vô vọc mấy cái t làm cho vui.")

# Ảnh đại diện (nếu có ảnh online)
#st.image("https://i.imgur.com/xxxxxxxx.png", width=200)

st.header("📌 Những thứ t làm")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Hệ Thống Quản Lí Giáo Dục 🎓")
    st.write("Đây là hệ thống quản lí giáo dục dành cho giáo viên, phụ huynh và học sinh..")
    st.page_link("pages/project_1.py", label="🔗 Xem dự án", icon="➡️")

with col2:
    st.subheader(" Ghép ảnh skin Liên Quân")
    st.write("Tool ghép ảnh tùy chọn, hiển thị đẹp trên web.")
    st.page_link("pages/project_2.py", label="🔗 Xem dự án", icon="➡️")

with col3:
    st.subheader(".....")
    st.write(".....")
    st.page_link("pages/project_3.py", label="🔗 Xem dự án", icon="➡️")
