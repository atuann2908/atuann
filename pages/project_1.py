import streamlit as st
import pandas as pd
import os

hide_sidebar_style = """
    <style>
        /* Ẩn menu navigation mặc định (Home, pages/...) */
        section[data-testid="stSidebarNav"] {display: none !important;}
    </style>
"""

st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Cấu hình
st.set_page_config(page_title="Hệ Thống Quản Lí Giáo Dục", page_icon="🎓", layout="wide")
TEACHER_FILE = "data/teachers.csv"
STUDENT_FILE = "data/students.csv"
PHUHUYNH_FILE = "data/parents.csv"
FILE_PATH = "data/diem_hocsinh.csv"
TKB_FILE = "data/tkb.csv"

# Hàm xử lý dữ liệu
def check_teacher_login(username, password):
    if not os.path.exists(TEACHER_FILE):
        return False
    df = pd.read_csv(TEACHER_FILE)
    return ((df['username'] == username) & (df['password'] == password)).any()

def check_parent_login(username, password):
    if not os.path.exists(PHUHUYNH_FILE):
        return False
    df = pd.read_csv(PHUHUYNH_FILE)
    return ((df['username'] == username) & (df['password'] == password)).any()

def check_student_login(username, password):
    if not os.path.exists(STUDENT_FILE):
        return False
    df = pd.read_csv(STUDENT_FILE)
    return ((df['username'] == username) & (df['password'] == password)).any()

def read_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    return pd.DataFrame(columns=["Tên", "Lớp", "Môn", "Miệng", "15p", "1 tiết", "Thi", "TB"])

def save_data(df):
    df.to_csv(FILE_PATH, index=False)

def add_student(ten, lop, mon, diem_mieng, diem_15p, diem_1tiet, diem_thi):
    df = read_data()
    tb = round((diem_mieng + diem_15p + diem_1tiet*2 + diem_thi*3) / 7, 2)
    new_row = {
        "Tên": ten,
        "Lớp": lop,
        "Môn": mon,
        "Miệng": diem_mieng,
        "15p": diem_15p,
        "1 tiết": diem_1tiet,
        "Thi": diem_thi,
        "TB": tb
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)

def read_tkb():
    if os.path.exists(TKB_FILE):
        return pd.read_csv(TKB_FILE)
    # Nếu chưa có file, trả về DataFrame mẫu
    return pd.DataFrame({
        "Lớp": ["10A1", "10A2", "11B3", "12C4", "12C5"],
        "Thứ": ["Hai", "Ba", "Tư", "Năm", "Sáu"],
        "Tiết": [1, 2, 3, 4, 5],
        "Môn": ["Toán", "Văn", "Anh", "Hóa", "Tin"]
    })

def save_tkb(df):
    df.to_csv(TKB_FILE, index=False)


# Sidebar Điều Hướng
st.sidebar.title("📑 Menu")
page = st.sidebar.radio(
    "Chọn trang:",
    ["🏠 Trang Chủ", "👨‍🏫 Giáo Viên", "🧑‍💼 Phụ Huynh", "🧑‍🎓 Học Sinh", "🔑Quản Trị Viên"]
)

# Nội dung từng trang
if page =="🏠 Trang Chủ":
    st.title("Hệ Thống Quản Lí Giáo Dục 🎓")
    st.markdown("""
    **Xin chào!**   
    Đây là hệ thống quản lí giáo dục dành cho giáo viên, phụ huynh và học sinh.
    Hãy chọn một mục từ menu bên trái để bắt đầu.
    Test:
    - Tài khoản giáo viên: teacher1 - teacher_1
    - Tài khoản phụ huynh: PH1 - PH_1
    - Tài khoản học sinh: HS1 - HS_1
    """)

elif page == "🔑Quản Trị Viên":
    st.title("🔑Quản Trị Viên")
    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False

    if not st.session_state["admin_logged_in"]:
        admin_user = st.text_input("Tên đăng nhập")
        admin_pass = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập"):
            if admin_user == "atuann" and admin_pass == "Tuan@290809288266":
                st.success("Đăng Nhập Thành Công!")
                st.session_state["admin_logged_in"] = True
                st.rerun()
            else:
                st.error("Sai tài khoản quản trị viên!")
    else:
        st.header("Quản Lý Tài Khoản")
        tab = st.radio("Chọn loại tài khoản", ["Giáo Viên", "Phụ Huynh", "Học Sinh"], key="admin_tab")

        if tab == "Giáo Viên":
            st.subheader("Thêm Giáo Viên Mới")
            with st.form("form_them_giaovien", clear_on_submit=True):
                gv_username = st.text_input("Tên đăng nhập", key="gv_username")
                gv_password = st.text_input("Mật khẩu", type="password", key="gv_password")
                xac_nhan = st.text_input("Xác nhận mật khẩu", type="password", key="gv_xacnhan")
                submitted = st.form_submit_button("Thêm Giáo Viên")
                if submitted:
                    if gv_password != xac_nhan:
                        st.error("⚠️ Mật khẩu xác nhận không khớp!")
                    elif not gv_username.strip() or not gv_password.strip():
                        st.error("⚠️ Vui lòng điền đầy đủ thông tin!")
                    else:
                        if os.path.exists(TEACHER_FILE):
                            df = pd.read_csv(TEACHER_FILE)
                        else:
                            df = pd.DataFrame(columns=["username", "password"])
                        if (df['username'] == gv_username).any():
                            st.error("⚠️ Tên đăng nhập đã tồn tại!")
                        else:
                            df = pd.concat([df, pd.DataFrame([{"username": gv_username, "password": gv_password}])], ignore_index=True)
                            df.to_csv(TEACHER_FILE, index=False)
                            st.success(f"✅ Đã thêm giáo viên: {gv_username}")

        elif tab == "Phụ Huynh":
            st.subheader("Thêm Phụ Huynh Mới")
            with st.form("form_them_phuhuynh", clear_on_submit=True):
                ph_username = st.text_input("Tên đăng nhập", key="ph_username")
                ph_password = st.text_input("Mật khẩu", type="password", key="ph_password")
                xac_nhan = st.text_input("Xác nhận mật khẩu", type="password", key="ph_xacnhan")
                submitted = st.form_submit_button("Thêm Phụ Huynh")
                if submitted:
                    if ph_password != xac_nhan:
                        st.error("⚠️ Mật khẩu xác nhận không khớp!")
                    elif not ph_username.strip() or not ph_password.strip():
                        st.error("⚠️ Vui lòng điền đầy đủ thông tin!")
                    else:
                        if os.path.exists(PHUHUYNH_FILE):
                            df = pd.read_csv(PHUHUYNH_FILE)
                        else:
                            df = pd.DataFrame(columns=["username", "password"])
                        if (df['username'] == ph_username).any():
                            st.error("⚠️ Tên đăng nhập đã tồn tại!")
                        else:
                            df = pd.concat([df, pd.DataFrame([{"username": ph_username, "password": ph_password}])], ignore_index=True)
                            df.to_csv(PHUHUYNH_FILE, index=False)
                            st.success(f"✅ Đã thêm phụ huynh: {ph_username}")

        elif tab == "Học Sinh":
            st.subheader("Thêm Học Sinh Mới")
            with st.form("form_them_hocsinh", clear_on_submit=True):
                hs_username = st.text_input("Tên đăng nhập", key="hs_username")
                hs_password = st.text_input("Mật khẩu", type="password", key="hs_password")
                xac_nhan = st.text_input("Xác nhận mật khẩu", type="password", key="hs_xacnhan")
                submitted = st.form_submit_button("Thêm Học Sinh")
                if submitted:
                    if hs_password != xac_nhan:
                        st.error("⚠️ Mật khẩu xác nhận không khớp!")
                    elif not hs_username.strip() or not hs_password.strip():
                        st.error("⚠️ Vui lòng điền đầy đủ thông tin!")
                    else:
                        if os.path.exists(STUDENT_FILE):
                            df = pd.read_csv(STUDENT_FILE)
                        else:
                            df = pd.DataFrame(columns=["username", "password"])
                        if (df['username'] == hs_username).any():
                            st.error("⚠️ Tên đăng nhập đã tồn tại!")
                        else:
                            df = pd.concat([df, pd.DataFrame([{"username": hs_username, "password": hs_password}])], ignore_index=True)
                            df.to_csv(STUDENT_FILE, index=False)
                            st.success(f"✅ Đã thêm học sinh: {hs_username}")

        if st.button("Đăng xuất quản trị viên"):
            st.session_state["admin_logged_in"] = False 
            st.success("Đã đăng xuất!")
            st.rerun()


elif page == "👨‍🏫 Giáo Viên":
    if st.session_state.get('role') != 'teacher':
        st.title("👨‍🏫 Giáo Viên")
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập"):
            if check_teacher_login(username, password):
                st.success("Đăng nhập thành công!")
                st.session_state['role'] = 'teacher'
                st.rerun()
            else:
                st.error("Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        st.header("Chọn chức năng:")
        chuc_nang = st.radio("Chọn chức năng", ["Nhập điểm", "Xem điểm", "Thời khóa biểu"])
        if st.button("Đăng xuất giáo viên"):
            st.session_state['role'] = None
            st.success("Đã đăng xuất!")
            st.rerun()

        elif chuc_nang == "Nhập điểm":
            st.title("📝 Nhập Điểm Học Sinh")
            with st.form("form_nhap_diem", clear_on_submit=True):
                ten = st.text_input("Họ và tên")
                lop = st.selectbox("Chọn lớp", ["10A1", "10A2", "10A3", "10A4", "10A5", "10A6", "10A7", "10A8", "10A9", "10A10", "11B1", "11B2", "11B3", "11B4", "11B5", "11B6", "11B7", "11B8", "11B9", "11B10", "12C1", "12C2", "12C3", "12C4", "12C5", "12C6", "12C7", "12C8", "12C9", "12C10"])
                mon = st.selectbox("Chọn môn", ["Toán", "Văn", "Anh", "Lý", "Hóa", "Sinh", "Sử", "Địa", "Tin", "KTPL", "Thể dục", "AN-QP"])
                diem_mieng = st.number_input("Điểm miệng", 0.0, 10.0, step=0.1)
                diem_15p = st.number_input("Điểm 15 phút", 0.0, 10.0, step=0.1)
                diem_1tiet = st.number_input("Điểm 1 tiết", 0.0, 10.0, step=0.1)
                diem_thi = st.number_input("Điểm thi", 0.0, 10.0, step=0.1)

                submitted = st.form_submit_button("💾 Lưu điểm")
                if submitted:
                    if ten.strip():
                        add_student(ten, lop, mon, diem_mieng, diem_15p, diem_1tiet, diem_thi)
                        st.success(f"✅ Đã lưu điểm cho {ten} ({lop} - {mon})")
                    else:
                        st.error("⚠️ Vui lòng nhập họ tên học sinh!")
        elif chuc_nang == "Xem điểm":
            st.title("📋 Danh Sách Điểm Học Sinh")
            df = read_data()
            if not df.empty:
                lop = st.multiselect("Chọn lớp", options=df["Lớp"].unique())
                mon = st.multiselect("Chọn môn", options=df["Môn"].unique())

                df_filtered = df.copy()
                if lop:
                    df_filtered = df_filtered[df_filtered["Lớp"].isin(lop)]
                if mon:
                    df_filtered = df_filtered[df_filtered["Môn"].isin(mon)]

                st.dataframe(df_filtered, use_container_width=True)
                st.download_button("⬇️ Tải CSV", df_filtered.to_csv(index=False), "danh_sach_diem.csv")
            else:
                st.warning("⚠️ Chưa có dữ liệu. Hãy thêm điểm ở mục Nhập điểm.")
        elif chuc_nang == "Thời khóa biểu":
            st.title("📅Thời Khóa Biểu")
            tkb = read_tkb()

            all_classes = tkb["Lớp"].dropna().astype(str).unique().tolist() + ["10A1", "10A2", "10A3", "10A4", "10A5", "10A6", "10A7", "10A8", "10A9", "10A10", "11B1", "11B2", "11B3", "11B4", "11B5", "11B6", "11B7", "11B8", "11B9", "11B10", "12C1", "12C2", "12C3", "12C4", "12C5", "12C6", "12C7", "12C8", "12C9", "12C10"]
            all_classes = sorted(list(set(all_classes)))  # Loại bỏ trùng lặp và sắp xếp lại
            selected_class = st.selectbox("Chọn lớp", all_classes)

            tkb_lop = tkb[tkb["Lớp"] == selected_class]

            if not tkb_lop.empty:
                tkb_pivot = tkb_lop.pivot(index="Tiết", columns="Thứ", values="Môn")
                tkb_pivot = tkb_pivot.reindex(columns=["Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy"], fill_value="")
                tkb_pivot.index.name = "Tiết"
                st.dataframe(tkb_pivot, use_container_width=True)
            else:
                st.info("Chưa có thời khóa biểu cho lớp này.")
            st.divider()

            st.subheader("➕ Thêm môn học")
            with st.form("add_subject"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    thu = st.selectbox("Chọn thứ", ["Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy"])
                with col2:
                    tiet = st.number_input("Tiết", min_value=1, max_value=10, step=1)
                with col3:
                    mon = st.text_input("Tên môn học")

                submit = st.form_submit_button("Thêm")

            if submit and mon.strip():
                new_row = pd.DataFrame({"Lớp": [selected_class], "Thứ": [thu], "Tiết": [tiet], "Môn": [mon.strip()]})
                tkb = pd.concat([tkb, new_row], ignore_index=True)
                save_tkb(tkb)
                st.success("✅ Đã thêm môn học!")
                st.rerun()

            st.divider()

            # --- Chọn môn học để chỉnh sửa ---
            st.subheader("✏ Chỉnh sửa môn học")
            tkb_lop = tkb[tkb["Lớp"] == selected_class]
            if len(tkb_lop) > 0:
                selected_idx = st.selectbox(
                    "Chọn dòng để chỉnh sửa",
                    tkb_lop.index,
                    format_func=lambda x: f"{tkb_lop.loc[x, 'Thứ']} - Tiết {tkb_lop.loc[x, 'Tiết']} - {tkb_lop.loc[x, 'Môn']}"
                )

                with st.form("edit_subject"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        new_thu = st.selectbox("Thứ", ["Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy"], index=["Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy"].index(tkb_lop.loc[selected_idx, "Thứ"]))
                    with col2:
                        new_tiet = st.number_input("Tiết", min_value=1, max_value=10, step=1, value=int(tkb_lop.loc[selected_idx, "Tiết"]))
                    with col3:
                        new_mon = st.text_input("Môn học", value=tkb_lop.loc[selected_idx, "Môn"])

                    save_edit = st.form_submit_button("💾 Lưu chỉnh sửa")

                if save_edit:
                    tkb.loc[selected_idx, "Thứ"] = new_thu
                    tkb.loc[selected_idx, "Tiết"] = new_tiet
                    tkb.loc[selected_idx, "Môn"] = new_mon
                    save_tkb(tkb)
                    st.success("✅ Đã cập nhật môn học!")
                    st.rerun()
            else:
                st.info("Không có môn học để chỉnh sửa.")

            st.divider()

            # --- Xóa môn học ---
            st.subheader("🗑 Xóa môn học")
            tkb_lop = tkb[tkb["Lớp"] == selected_class]
            if len(tkb_lop) > 0:
                selected_delete = st.selectbox(
                    "Chọn dòng để xóa",
                    tkb_lop.index,
                    format_func=lambda x: f"{tkb_lop.loc[x, 'Thứ']} - Tiết {tkb_lop.loc[x, 'Tiết']} - {tkb_lop.loc[x, 'Môn']}"
                )
                if st.button("Xóa"):
                    tkb = tkb.drop(index=selected_delete).reset_index(drop=True)
                    save_tkb(tkb)
                    st.success(" Đã xóa môn học!")
                    st.rerun()
            else:
                st.info("Không có môn học để xóa.")
elif page == "🧑‍💼 Phụ Huynh":
    if st.session_state.get('role') != 'parent':
        st.title("🧑‍💼 Phụ Huynh")
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập"):
            if check_parent_login(username, password):
                st.success("Đăng nhập thành công!")
                st.session_state['role'] = 'parent'
                st.rerun()
            else:
                st.error("Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        st.header("COMMING SOON...")
        if st.button("Đăng xuất phụ huynh"):
            st.session_state['role'] = None
            st.success("Đã đăng xuất!")
            st.rerun()
elif page == "🧑‍🎓 Học Sinh":
    if st.session_state.get('role') != 'student':
        st.title("🧑‍🎓 Học Sinh")
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập"):
            if check_student_login(username, password):
                st.success("Đăng nhập thành công!")
                st.session_state['role'] = 'student'
                st.rerun()
            else:
                st.error("Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        st.header("COMMING SOON...")
        if st.button("Đăng xuất học sinh"):
            st.session_state['role'] = None
            st.success("Đã đăng xuất!")
            st.rerun()