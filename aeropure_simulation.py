import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("AeroPure Integrated Simulation")

# -----------------------------
# USER INPUT
# -----------------------------
co2_input = st.slider("CO2 Input (tons/day)", 10, 200, 50)
so2_input = st.slider("SO2 Input (tons/day)", 5, 100, 20)
solar_irradiance = st.slider("Solar Irradiance (W/m^2)", 200, 1000, 800)

# -----------------------------
# ELECTRICAL SYSTEM
# -----------------------------
panel_efficiency = 0.18
panel_area = 50

power_output = panel_efficiency * panel_area * solar_irradiance
power_factor = power_output / (panel_efficiency * panel_area * 1000)

# -----------------------------
# CHEMICAL SYSTEM
# -----------------------------
co2_efficiency = 0.35
so2_efficiency = 0.9
methanol_yield = 0.73

actual_efficiency = co2_efficiency * power_factor

methanol_output = co2_input * actual_efficiency * methanol_yield
gypsum_output = so2_input * so2_efficiency * 1.5

# -----------------------------
# ECONOMICS
# -----------------------------
methanol_price = 25000
gypsum_price = 2000
carbon_credit = 1500

methanol_revenue = methanol_output * methanol_price
gypsum_revenue = gypsum_output * gypsum_price
carbon_revenue = co2_input * carbon_credit

total_revenue = methanol_revenue + gypsum_revenue + carbon_revenue

# -----------------------------
# OUTPUT
# -----------------------------
st.subheader("Results")
st.write(f"Power Output: {power_output:.2f} W")
st.write(f"Methanol Produced: {methanol_output:.2f} tons/day")
st.write(f"Gypsum Produced: {gypsum_output:.2f} tons/day")
st.write(f"Total Revenue: {total_revenue:.2f} INR/day")

# -----------------------------
# SIMULATION RANGE
# -----------------------------
solar_range = np.linspace(200, 1000, 20)

power_range = panel_efficiency * panel_area * solar_range
power_factor_range = power_range / (panel_efficiency * panel_area * 1000)

methanol_range = co2_input * (co2_efficiency * power_factor_range) * methanol_yield

revenue_range = (
    methanol_range * methanol_price +
    gypsum_output * gypsum_price +
    co2_input * carbon_credit
)

# -----------------------------
# GRAPH 1: POWER
# -----------------------------
st.subheader("Power Analysis")

fig1, ax1 = plt.subplots()
ax1.plot(solar_range, power_range)
ax1.set_xlabel("Solar Irradiance (W/m^2)")
ax1.set_ylabel("Power Output (W)")
ax1.set_title("Solar vs Power Output")

st.pyplot(fig1)

# -----------------------------
# GRAPH 2: METHANOL
# -----------------------------
st.subheader("Methanol Production")

fig2, ax2 = plt.subplots()
ax2.plot(solar_range, methanol_range)
ax2.set_xlabel("Solar Irradiance (W/m^2)")
ax2.set_ylabel("Methanol Output (tons/day)")
ax2.set_title("Solar vs Methanol Production")

st.pyplot(fig2)

# -----------------------------
# GRAPH 3: REVENUE
# -----------------------------
st.subheader("Revenue Analysis")

fig3, ax3 = plt.subplots()
ax3.plot(solar_range, revenue_range)
ax3.set_xlabel("Solar Irradiance (W/m^2)")
ax3.set_ylabel("Revenue (INR/day)")
ax3.set_title("Solar vs Revenue")

st.pyplot(fig3)