import numpy as np
from matplotlib import pyplot as plt

from chambers import OpenChamber



fig, ax = plt.subplots(2,2)
chamber = OpenChamber()
V = np.linspace(0, 1000, 100)  # volume in mL

for r in [4, 6, 8]: # radius in cm
    radius = r / 100 # radius of chamber in m
    chamber.radius = radius
    P = chamber.pressure(V)

    ax[0,0].plot(V, P, label="r=%1.1f cm" % r)
    h = chamber.water_height(V) * 100
    ax[0,1].plot(h, P, label="r=%1.1f cm" % r)

    elastance_numerical = np.gradient(P, V)
    ax[1,0].plot(V, elastance_numerical, label="Num r=%1.1f cm" % r)
    ax[1,0].axhline(chamber.elastance(), color='k', alpha=0.1, linestyle="--", label=None)

    capacitance_numerical = 1 / elastance_numerical
    ax[1,1].plot(V, capacitance_numerical, label="Num r=%1.1f cm" % r)
    ax[1,1].axhline(chamber.capacitance(), color='k', alpha=0.1, linestyle="--", label=None)


ax[0, 0].set_xlabel("Water volume (mL)")
ax[0, 0].set_ylabel("Pressure (mmHg)")
ax[0, 0].legend()

ax[0,1].set_xlabel("Water height (cm)")
ax[0,1].set_ylabel("Pressure (mmHg)")
ax[0,1].legend()

ax[1,0].set_xlabel("Water volume (mL)")
ax[1,0].set_ylabel("Elastance (mmHg / mL)")
ax[1,0].set_ylim([0, 1 / 50])
ax[1,0].legend()

ax[1,1].set_xlabel("Water volume (mL)")
ax[1,1].set_ylabel("Capacitance (mL / mmHg)")
ax[1,1].set_ylim([0, 300])
ax[1,1].legend()

plt.show()