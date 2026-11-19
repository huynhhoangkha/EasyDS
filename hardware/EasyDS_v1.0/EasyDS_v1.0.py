import streamlit as st

st.set_page_config(page_title="KiCad Diff Pair Generator", page_icon="⚡", layout="centered")

st.title("⚡ KiCad Differential Pair Rule Generator")
st.write("Công cụ tạo file `.kicad_dru` tự động cho tín hiệu vi sai.")

st.divider()

# --- 1. Thông tin cơ bản ---
col_info1, col_info2 = st.columns(2)
with col_info1:
    rule_name = st.text_input("Tên Rule (Rule Name)", value="Diff_Pair_USB90")
with col_info2:
    net_class = st.text_input("Tên NetClass áp dụng", value="USB_90OHM")

layer_option = st.selectbox(
    "Áp dụng cho Lớp (Layer)",
    options=["Tất cả các lớp (All)", "Lớp ngoài (Outer - F.Cu / B.Cu)", "Lớp trong (Inner)"]
)

st.divider()

# --- 2. Cấu hình Tham số Differential Pair ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📏 Differential Gap (Khoảng cách cặp)")
    gap_opt = st.number_input("Khoảng cách chuẩn (Opt) [mm]", value=0.150, step=0.010, format="%.3f")
    gap_min = st.number_input("Tối thiểu (Min) [mm]", value=0.120, step=0.010, format="%.3f")
    gap_max = st.number_input("Tối đa (Max) [mm]", value=0.180, step=0.010, format="%.3f")

with col2:
    st.subheader("✏️ Track Width (Độ rộng đường mạch)")
    width_opt = st.number_input("Độ rộng chuẩn (Opt) [mm]", value=0.200, step=0.010, format="%.3f")
    width_min = st.number_input("Tối thiểu (Min) [mm]", value=0.180, step=0.010, format="%.3f")
    width_max = st.number_input("Tối đa (Max) [mm]", value=0.220, step=0.010, format="%.3f")

st.subheader("🛡️ Clearance (Khoảng cách ly tối thiểu với nét khác)")
clearance_min = st.number_input("Cách ly tối thiểu (Min Clearance) [mm]", value=0.200, step=0.010, format="%.3f")

# --- 3. Tạo cú pháp S-Expression cho KiCad ---
layer_str = ""
if layer_option == "Lớp ngoài (Outer - F.Cu / B.Cu)":
    layer_str = "  (layer outer)\n"
elif layer_option == "Lớp trong (Inner)":
    layer_str = "  (layer inner)\n"

kicad_dru_content = f"""(version 1)

(rule "{rule_name}"
{layer_str}  (constraint diff_pair_gap (min {gap_min}mm) (opt {gap_opt}mm) (max {gap_max}mm))
  (constraint track_width (min {width_min}mm) (opt {width_opt}mm) (max {width_max}mm))
  (constraint clearance (min {clearance_min}mm))
  (condition "A.NetClass == '{net_class}'")
)
"""

st.divider()

# --- 4. Hiển thị kết quả & Download ---
st.subheader("📄 Xem trước file `.kicad_dru`:")
st.code(kicad_dru_content, language="lisp")

st.download_button(
    label="💾 Tải file .kicad_dru",
    data=kicad_dru_content,
    file_name=f"{rule_name}.kicad_dru",
    mime="text/plain"
)