import pandas as pd
import streamlit as st

# --- 1. Tiêu đề ứng dụng ---
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# --- 2. Dữ liệu mẫu (10 sinh viên) ---
# Quy tắc tính điểm tổng kết thông thường: Chuyên cần * 0.1 + Giữa kỳ * 0.3 + Cuối kỳ * 0.6
data = {
    "Họ tên": [
        "Nguyễn Văn An",
        "Trần Thị Bình",
        "Lê Hoàng Cường",
        "Phạm Thị Dung",
        "Hoàng Văn Em",
        "Vũ Thị Phượng",
        "Đỗ Minh Giang",
        "Bùi Thị Hoa",
        "Ngô Văn Hùng",
        "Lý Thị Khanh",
    ],
    "Chuyên cần": [8.0, 9.0, 7.5, 6.0, 10.0, 8.5, 9.5, 4.0, 7.0, 8.0],
    "Giữa kỳ": [7.0, 8.5, 6.5, 5.5, 9.0, 7.5, 8.0, 3.5, 6.0, 7.5],
    "Cuối kỳ": [7.5, 8.0, 7.0, 5.0, 9.5, 8.0, 8.5, 3.0, 6.5, 7.0],
}

df = pd.DataFrame(data)

# Tính điểm Tổng kết
df["Tổng kết"] = (
    df["Chuyên cần"] * 0.1 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.6
).round(2)


# Xếp loại dựa trên điểm tổng kết
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"


df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# --- 3. Hiển thị bảng điểm ---
st.subheader("📋 Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df, use_container_width=True)

# --- 4. Các thông kê tổng quan ---
st.markdown("---")
st.subheader("📊 Thống kê chung của lớp")

col1, col2, col3 = st.columns(3)

# Điểm trung bình của lớp
dtb_lop = df["Tổng kết"].mean().round(2)
col1.metric("Điểm TB của lớp", dtb_lop)

# Số sinh viên đạt (Tổng kết >= 5.0)
so_sv_dat = len(df[df["Tổng kết"] >= 5.0])
col2.metric("Số sinh viên đạt", f"{so_sv_dat}/10")

# Sinh viên cao nhất và thấp nhất
sv_max = df.loc[df["Tổng kết"].idxmax()]
sv_min = df.loc[df["Tổng kết"].idxmin()]

col3.metric(
    "SV Tổng kết cao nhất",
    f"{sv_max['Họ tên']} ({sv_max['Tổng kết']})",
)

st.info(
    f"🔻 **Sinh viên có điểm tổng kết thấp nhất:** {sv_min['Họ tên']} ({sv_min['Tổng kết']})"
)

# --- 5. Tra cứu điểm từng sinh viên (Selectbox) ---
st.markdown("---")
st.subheader("🔍 Tra cứu thông tin sinh viên")

selected_student = st.selectbox(
    "Chọn tên sinh viên để xem chi tiết:", df["Họ tên"].tolist()
)

# Lọc dữ liệu sinh viên được chọn
student_info = df[df["Họ tên"] == selected_student].iloc[0]

# Hiển thị thông tin
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", student_info["Chuyên cần"])
c2.metric("Giữa kỳ", student_info["Giữa kỳ"])
c3.metric("Cuối kỳ", student_info["Cuối kỳ"])
c4.metric("Tổng kết", student_info["Tổng kết"])
c5.metric("Xếp loại", student_info["Xếp loại"])
# --- 6. Biểu đồ cột điểm tổng kết ---
st.markdown("---")
st.subheader("📈 Biểu đồ cột điểm tổng kết của sinh viên")

# Chuẩn bị dữ liệu vẽ biểu đồ
chart_data = df.set_index("Họ tên")[["Tổng kết"]]
st.bar_chart(chart_data)

# --- 7. Thông tin người tạo ứng dụng ở cuối trang ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 12px;'>"
    "Được tạo bởi: [Họ và tên của bạn] - MSSV: [Mã số sinh viên của bạn]"
    "</div>",
    unsafe_allow_html=True,
)