import streamlit as st
from smartos_main import run_model   # ⬅️ import your model function here

# Streamlit App
st.set_page_config(page_title="SmartOS Dashboard", layout="wide")

st.title("🚀 SmartOS Dashboard")

# Sidebar
st.sidebar.header("Configuration")
st.sidebar.write("Running in **Web Mode**")
st.sidebar.write("Port: 8080")

# Input Section
st.subheader("🔹 Run Model")
user_input = st.text_input("Enter your input:")

if st.button("Run SmartOS"):
    if user_input.strip():
        result = run_model(user_input)   # <-- Call your SmartOS function
        st.success("### ✅ Result:")
        st.write(result)
    else:
        st.warning("Please enter a valid input.")

# Logs Section
st.subheader("📜 Logs")
if st.button("View Logs"):
    with open("smartos.log", "r") as f:   # adjust to your actual log file path
        logs = f.read()
    st.text_area("Logs", logs, height=200)

# Config Section
st.subheader("⚙️ Configuration")
st.json({
    "mode": "web",
    "port": 8080,
    "status": "running"
})
