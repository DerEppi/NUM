from params import params
from atmosphere import Atmosphere


atm = Atmosphere(params)

R = params["R"]
lamb = params["lambda_um"]
n_surf = params["n_surf"]
Temp = params["T_atm"]
M_pl = params["M_pl"]
R_pl = params["R_pl"]

# check
print("Parameters:")
print(f"Planet radius: {R_pl:.1e} m, Planet mass: {M_pl:.1e} kg")
print(f"Surface temperature: {Temp:.1f} K, Surface density: {n_surf:.2e} m^-3")
print(f"Wavelength and radius of interest: λ = {lamb:.1f} µm, R = {R:.1e} m")
print(f"Distance from planet surface: {(R-R_pl):.0f} m\n")



tau = atm.optical_depth(params["lambda_um"], params["R"])
T = atm.transmissivity(params["lambda_um"], params["R"])

print("Results:")
print(f"Optical depth: {tau:.4f}")
print(f"Transmissivity: {T:.4e}")