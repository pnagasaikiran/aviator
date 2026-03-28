import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(
    page_title="Aviator Advanced Analyzer",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Aviator Advanced Analyzer & Simulator")

# -------------------------------
# Simulation Logic
# -------------------------------
def generate_crash():
    r = random.random()
    return round(max(1.0, (1 / (1 - r)) * 0.99), 2)

# -------------------------------
# Session State
# -------------------------------
if "data" not in st.session_state:
    st.session_state.data = [generate_crash() for _ in range(100)]

data = st.session_state.data

# -------------------------------
# Buttons
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add Round"):
        st.session_state.data.append(generate_crash())

with col2:
    if st.button("🔄 Reset Data"):
        st.session_state.data = [generate_crash() for _ in range(100)]

# -------------------------------
# Stats
# -------------------------------
st.subheader("📊 Statistics")

st.write("Total Rounds:", len(data))
st.write("Average:", round(np.mean(data), 2))
st.write("Max:", max(data))
st.write("Min:", min(data))

# -------------------------------
# Probability Analysis
# -------------------------------
st.subheader("📈 Probability Analysis")

arr = np.array(data)

st.write("≤2x:", round(np.mean(arr <= 2) * 100, 2), "%")
st.write(">2x:", round(np.mean(arr > 2) * 100, 2), "%")
st.write(">5x:", round(np.mean(arr > 5) * 100, 2), "%")
st.write(">10x:", round(np.mean(arr > 10) * 100, 2), "%")

# -------------------------------
# Charts
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 Multiplier Trend")
    fig, ax = plt.subplots()
    ax.plot(data)
    ax.set_xlabel("Rounds")
    ax.set_ylabel("Multiplier")
    st.pyplot(fig)

with col2:
    st.subheader("📊 Distribution (Histogram)")
    fig2, ax2 = plt.subplots()
    ax2.hist(data, bins=20)
    ax2.set_xlabel("Multiplier")
    ax2.set_ylabel("Frequency")
    st.pyplot(fig2)

# -------------------------------
# Smart Insight (Prediction Logic)
# -------------------------------
st.subheader("🤖 Smart Next Round Insight")

recent = data[-10:]

low_ratio = sum(1 for x in recent if x <= 2) / len(recent)

if low_ratio > 0.7:
    st.success("Next Likely: LOW (1x – 2x)")
elif low_ratio > 0.4:
    st.warning("Next Likely: MEDIUM (2x – 5x)")
else:
    st.error("High Volatility: Possible spike (5x+)")

# -------------------------------
# Manual Input Analyzer
# -------------------------------
st.subheader("✍️ Analyze Your Own Data")

user_input = st.text_area("Enter multipliers (comma separated, with or without x)")

if st.button("Analyze Input"):
    try:
        user_data = [float(x.replace('x','').strip()) for x in user_input.split(",")]
        user_arr = np.array(user_data)

        st.write("Average:", round(np.mean(user_arr), 2))
        st.write("Max:", max(user_arr))
        st.write("Min:", min(user_arr))

        st.write("≤2x:", round(np.mean(user_arr <= 2)*100,2), "%")
        st.write(">2x:", round(np.mean(user_arr > 2)*100,2), "%")
        st.write(">5x:", round(np.mean(user_arr > 5)*100,2), "%")

        # Insight
        recent_user = user_data[-10:]
        low_ratio_user = sum(1 for x in recent_user if x <= 2) / len(recent_user)

        if low_ratio_user > 0.7:
            st.success("Trend: LOW → safer for early cashout")
        elif low_ratio_user > 0.4:
            st.warning("Trend: MEDIUM → mixed behavior")
        else:
            st.error("Trend: HIGH RISK → possible spikes")

    except:
        st.error("Invalid input format. Example: 1.2x, 2.5x, 3.0x")