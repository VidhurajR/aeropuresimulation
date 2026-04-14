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
temperature = st.slider("Reactor Temperature (K)", 250, 500, 350)

# -----------------------------
# ELECTRICAL SYSTEM
# -----------------------------
panel_efficiency = 0.18
panel_area = 50

power_output = panel_efficiency * panel_area * solar_irradiance
power_factor = power_output / (panel_efficiency * panel_area * 1000)

# -----------------------------
# CHEMICAL SYSTEM (KINETICS)
# -----------------------------
R = 8.314
Ea = 50000      # J/mol
A = 1e3

# Arrhenius equation
k = A * np.exp(-Ea / (R * temperature))

# Time simulation
time = np.linspace(0, 100, 100)

CO2_conc = co2_input * np.exp(-k * time * power_factor)
Methanol_conc = co2_input - CO2_conc

# Final outputs
methanol_output = Methanol_conc[-1] * 0.73
gypsum_output = so2_input * 0.9 * 1.5

# -----------------------------
# ECONOMICS
# -----------------------------
methanol_price = 25000
gypsum_price = 2000
carbon_credit = 1500

total_revenue = (
    methanol_output * methanol_price +
    gypsum_output * gypsum_price +
    co2_input * carbon_credit
)

# -----------------------------
# OUTPUT
# -----------------------------
st.subheader("Results")
st.write(f"Power Output: {power_output:.2f} W")
st.write(f"Reaction Rate Constant (k): {k:.5f}")
st.write(f"Final Methanol Produced: {methanol_output:.2f} tons/day")
st.write(f"Gypsum Produced: {gypsum_output:.2f} tons/day")
st.write(f"Total Revenue: {total_revenue:.2f} INR/day")

# -----------------------------
# GRAPH 1: KINETICS
# -----------------------------
st.subheader("Reaction Kinetics")

fig1, ax1 = plt.subplots()
ax1.plot(time, CO2_conc, label="CO2")
ax1.plot(time, Methanol_conc, label="Methanol")
ax1.set_xlabel("Time")
ax1.set_ylabel("Concentration")
ax1.set_title("CO2 to Methanol Conversion")
ax1.legend()

st.pyplot(fig1)

# -----------------------------
# GRAPH 2: TEMPERATURE EFFECT
# -----------------------------
st.subheader("Temperature Effect")

temp_range = np.linspace(250, 500, 50)
k_range = A * np.exp(-Ea / (R * temp_range))

conversion = 1 - np.exp(-k_range * 50)

fig2, ax2 = plt.subplots()
ax2.plot(temp_range, conversion)
ax2.set_xlabel("Temperature (K)")
ax2.set_ylabel("Conversion")
ax2.set_title("Temperature vs Conversion")

st.pyplot(fig2)

# -----------------------------
# GRAPH 3: POWER EFFECT
# -----------------------------
st.subheader("Solar Effect on Output")

solar_range = np.linspace(200, 1000, 20)
power_range = panel_efficiency * panel_area * solar_range
pf = power_range / (panel_efficiency * panel_area * 1000)

methanol_range = co2_input * (1 - np.exp(-k * 50 * pf)) * 0.73

fig3, ax3 = plt.subplots()
ax3.plot(solar_range, methanol_range)
ax3.set_xlabel("Solar Irradiance")
ax3.set_ylabel("Methanol Output")
ax3.set_title("Solar vs Methanol")

st.pyplot(fig3)
