import numpy as np
from numpy import exp, sqrt
from scipy.constants import G, k, pi
from scipy.interpolate import interp1d
import os


class Atmosphere:
    # Computes optical depth and transmissivity for a planetary atmosphere

    def __init__(self, params: dict):
        self.p = params
        self._load_cross_section()
        

    def _load_cross_section(self):
        # Loads cross section file σ(ν) and prepares interpolation in λ
        file = os.path.join(os.path.dirname(__file__), self.p["sigma_file"]) # os used to obtain CO2.dat otherwise it had problems finding it
        nu, sigma_cm2, _ = np.loadtxt(file, unpack=True, skiprows=14)
        lam_um = 1e4 / nu           # ν [cm^-1] → λ [µm]
        sigma_m2 = sigma_cm2 * 1e-4             
        
        # linear interpolation to get a continious function for σ
        self.sigma = interp1d(lam_um, sigma_m2, bounds_error=False, fill_value=0.0)

    def scale_height(self):
        # Atmospheric scale height [m].
        m_co2 = 44.009 * 1.66054e-27        # CO₂ molecular mass [kg]
        g = G * self.p["M_pl"] / self.p["R_pl"]**2

        # the instruction shows a different formula with R_g but I think it was mixing up terminology with "molar mass" and "mass of a molecule"
        # according to literature (e.g. https://www.spaceacademy.net.au/library/notes/scaleht.htm) H = k*T/m_gas*g with m_gas being molecular mass
        # the formula with R would use molar mass for m_g since R = k*N_A
        return k * self.p["T_atm"] / (m_co2 * g)

    def number_density(self, R):
        # Barometric number density at radius R [m^-3]
        h = R - self.p["R_pl"]
        H = self.scale_height()
        return self.p["n_surf"] * exp(-h / H)

    def column_density(self, R):
        # Integrated column density using the approximation
        H = self.scale_height()
        n = self.number_density(R)
        return n * sqrt(2*pi*R*H) # I used the approximation because the Bessel function creates overflow problems

    def optical_depth(self, lam_um, R):
        # Optical depth τ(λ, R) = N_t * σ(λ)
        N_t = self.column_density(R)
        return N_t * self.sigma(lam_um)

    def transmissivity(self, lam_um, R):
        # Transmissivity T(λ, R) = exp(-τ(λ))
        tau = self.optical_depth(lam_um, R)
        return exp(-tau)
