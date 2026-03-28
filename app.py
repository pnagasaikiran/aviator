import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(
    page_title="Aviator Analyzer",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Aviator Simulation & Analyzer")

# --- Simulation Logic ---
def generate_crash():
    r = random.random()
    return round(max(1.0, (1 / (1 - r)) * 0.99), 2)

# --- Session Data ---
if "data" not in st.session_state:
    st.session_state.data = [generate_crash() for _ in range(100)]

data = st.session_state.data

# --- Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add Round"):
        st.session_state.data.append(generate_crash())

with col2:
    if st.button("🔄 Reset Data"):
        st.session_state.data = [generate_crash() for _ in range(100)]

# --- Stats ---
st.subheader("📊 Statistics")

st.write("Total Rounds:", len(data))
st.write("Average Multiplier:", round(np.mean(data), 2))
st.write("Max:", max(data))
st.write("Min:", min(data))

# --- Probability ---
st.subheader("📈 Probability Analysis")

st.write("≥1.5x:", round(np.mean(np.array(data)>=1.5)*100,2), "%")
st.write("≥2x:", round(np.mean(np.array(data)>=2)*100,2), "%")
st.write("≥5x:", round(np.mean(np.array(data)>=5)*100,2), "%")

# --- Chart ---
st.subheader("📉 Multiplier Trend")

fig, ax = plt.subplots()
ax.plot(data)
ax.set_xlabel("Rounds")
ax.set_ylabel("Multiplier")
st.pyplot(fig)

# --- Simulation Prediction ---
st.subheader("🤖 Simulation Insight")

recent_avg = np.mean(data[-20:])

if recent_avg < 2:
    st.success("LOW TREND (Safer: 1.3x - 2x)")
elif recent_avg < 5:
    st.warning("MEDIUM TREND (2x - 5x)")
else:
    st.error("HIGH RISK / HIGH VARIANCE")

# --- Manual Input ---
st.subheader("✍️ Manual Data Input")

user_input = st.text_area("Enter multipliers (comma separated):")

if st.button("Analyze Input"):
    try:
        user_data = [float(x.strip()) for x in user_input.split(",")]
        st.write("Average:", np.mean(user_data))
        st.write("Max:", max(user_data))
        st.write("Min:", min(user_data))
    except:
        st.error("Invalid input format")