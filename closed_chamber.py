import numpy as np
from matplotlib import pyplot as plt
from math import pi
from chambers import ClosedChamber

dap = 80
sap = 120
map = 2 * dap / 3 + 1 * sap / 3

Patm_pa = 101325 # Pa
Patm_mmhg = 760 # mmhg

radius = 6/100 # 6 cm

n = 1.4 # polytropic constant for adiabatic/ isentropic conditions

Ctarget = 1.5 # ml/mmhg

"""
find h0 given Ctarget
C approx Vair0 / n * Pabs0, w/ n=1.4 and Pabs0 = Pgauge + Patm = 93 + 760
"""
Vair0 = Ctarget * n * (map + Patm_mmhg)
Vbuffer = 500 # mL
Vtotal = Vbuffer + Vair0

area = pi * radius **2

h0 = Vbuffer / 1e6 / area
h_chamber = Vtotal / 1e6 / area

print(h0)
print(h_chamber)

chamber = ClosedChamber(radius, h0, Patm_pa, n, h_chamber)

V = np.linspace(0, 1000, 1000)  # volume in mL

P_hydro = chamber.hydrostatic_pressure(V)
P_air = chamber.air_pressure(V)
P = P_hydro + P_air

fig, ax = plt.subplots(2,2)

# ax[0,0].plot(V, P, label="r=%1.1f cm" % r)
ax[0,0].plot(V, P_hydro, label="Hydrostatic pressure")
ax[0,0].plot(V, P_air, label="Air pressure")
ax[0,0].plot(V, P, label="Total pressure")
ax[0,0].axhline(map, label="MAP", linestyle="--", color="blue")
ax[0,0].axhline(dap, label="Diastolic aortic pressure", linestyle="--", color="black")
ax[0,0].axhline(sap, label="Peak systolic aortic pressure", linestyle="--", color="red")

h = chamber.water_height(V) * 100
# ax[0,1].plot(h, P, label="r=%1.1f cm" % r)
ax[0,1].plot(h, P_hydro, label="Hydrostatic pressure")
ax[0,1].plot(h, P_air, label="Air pressure")
ax[0,1].plot(h, P, label="Total pressure")

elastance_numerical_hydro = np.gradient(P_hydro, V)
elastance_numerical_air = np.gradient(P_air, V)
elastance_numerical = np.gradient(P, V)

# ax[1,0].plot(V, elastance_numerical, label="Num r=%1.1f cm" % r)
ax[1,0].plot(V, elastance_numerical_hydro, label="Hydrostatic elastance")
ax[1,0].plot(V, elastance_numerical_air, label="Air elastance")
ax[1,0].plot(V, elastance_numerical, label="Total elastance")

# ax[1,1].plot(V, capacitance_numerical, label="Num r=%1.1f cm" % r)
ax[1,1].plot(V, 1/elastance_numerical_hydro, label="Hydrostatic capacitance")
ax[1,1].plot(V, 1/elastance_numerical_air, label="Air capacitance")
ax[1,1].plot(V, 1/elastance_numerical, label="Total capacitance")

ax[0, 0].set_xlabel("Water volume (mL)")
ax[0, 0].set_ylabel("Pressure (mmHg)")
ax[0, 0].legend()

ax[0,1].set_xlabel("Water height (cm)")
ax[0,1].set_ylabel("Pressure (mmHg)")
ax[0,1].legend()

ax[1,0].set_xlabel("Water volume (mL)")
ax[1,0].set_ylabel("Elastance (mmHg / mL)")
ax[1,0].legend()

ax[1,1].set_xlabel("Water volume (mL)")
ax[1,1].set_ylabel("Capacitance (mL / mmHg)")
ax[1,1].legend()

plt.show()