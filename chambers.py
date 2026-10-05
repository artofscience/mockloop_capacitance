from math import pi


class OpenChamber:
    def __init__(self, radius: float = 6 / 100):
        self.mmhgtopa = 133.322
        self.mltom3 = 1e-6

        self.density = 1000 # water density in kg / m3
        self.gravity = 9.81 # gravitational acceleration N / kg or m / s2

        self.radius = radius # radius of chamber

    def area(self):
        return pi * self.radius ** 2

    def elastance(self):
        return self.density * self.gravity / self.area() / self.mmhgtopa * self.mltom3

    def capacitance(self):
        return 1 / self.elastance()

    def water_height(self, water_volume: float):
        """
        water height in m from water volume in mL
        """
        return self.mltom3 * water_volume / self.area()

    def pressure(self, water_volume):
        """Gauge pressure at bottom of chamber."""
        return (self.density * self.gravity * self.water_height(water_volume)) / self.mmhgtopa

class ClosedChamber(OpenChamber):
    def __init__(self, radius: float = 6 / 100, h0: float = 0.5, Pair0: float = 101325, n: float = 1.4, h_chamber: float = 1.0):
        super().__init__(radius)

        self.Pair0 = Pair0 # initial air pressure (default atmospheric pressure in Pa)
        self.h0 = h0 # initial water level in m
        self.n = n #
        self.h_chamber = h_chamber # total chamber height in m

    def initial_water_volume(self):
        return self.area() * self.h0 # initial water volume in m3

    def volume_chamber(self):
        """Volume of chamber in m3"""
        return self.area() * self.h_chamber # total chamber volume in m3

    def gas_constant(self):
        return self.Pair0 * (self.volume_chamber() - self.initial_water_volume()) ** self.n # gas constant taking Pair0 in Pa and Vair0 in m3

    def hydrostatic_pressure(self, water_volume):
        water_height = self.water_height(water_volume) # water height in m
        return (self.density * self.gravity * water_height) / self.mmhgtopa  # hydro pressure in mmHg

    def air_pressure(self, water_volume):
        """Gauge pressure at bottom of chamber.
        Taking water volume in mL giving pressure in mmHg"""
        vair = self.volume_chamber() - water_volume * self.mltom3 # air volume in m3
        air_pressure = (self.gas_constant() / (vair ** self.n)) / self.mmhgtopa # air pressure in mmHg
        return air_pressure - (101325 / self.mmhgtopa)
