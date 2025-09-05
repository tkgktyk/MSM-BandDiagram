import numpy as np

def calculate_band_structure(chi, eg, fermi_shift, wf_left, wf_right, bias, **kwargs):
    """
    Calculates the energy band structure for an MSM device.
    Doping type is determined by the sign of fermi_shift.

    Args:
        chi (float): Electron affinity in eV.
        eg (float): Band gap in eV.
        fermi_shift (float): Fermi level shift from the intrinsic level in eV.
                           Positive for n-type, negative for p-type.
        wf_left (float): Work function of the left electrode in eV.
        wf_right (float): Work function of the right electrode in eV.
        bias (float): Applied bias voltage in V.
        **kwargs: Catches unused parameters like labels.

    Returns:
        dict: A dictionary containing the calculated band structure data arrays.
    """
    # --- Constants and References ---
    E_f_left = 0  # Left electrode Fermi level is the reference
    E_f_right = E_f_left - bias # Apply bias to the right electrode

    # --- X-axis definition ---
    semiconductor_width = 20.0
    x_metal_left = np.linspace(-10, 0, 100)
    x_semiconductor = np.linspace(0, semiconductor_width, 500)
    x_metal_right = np.linspace(semiconductor_width, semiconductor_width + 10, 100)

    # --- Metal Region Calculations ---
    E_vac_left = E_f_left + wf_left
    E_vac_right = E_f_right + wf_right

    # --- Semiconductor Calculations ---
    # W_s is the semiconductor work function: E_vac - E_f
    # This can be expressed as (E_vac - E_i) - (E_f - E_i)
    # (E_vac - E_i) is (chi + eg/2). (E_f - E_i) is the fermi_shift.
    W_s = (chi + eg / 2) - fermi_shift

    E_vac_bulk_equil = E_f_left + W_s # Equilibrium bulk vacuum level

    # Bending is the deviation from the bulk vacuum level
    Ld = 2.0 # Debye length (simplified model)
    bending = (E_vac_left - E_vac_bulk_equil) * np.exp(-x_semiconductor / Ld) + \
              (E_vac_right - (E_vac_bulk_equil - bias)) * np.exp((x_semiconductor - semiconductor_width) / Ld)

    # Add linear potential drop due to bias
    potential_drop = -bias * (x_semiconductor / semiconductor_width)

    E_vac_final = E_vac_bulk_equil + bending + potential_drop

    E_c = E_vac_final - chi
    E_v = E_c - eg
    E_i = E_c - eg / 2
    
    # Quasi-Fermi levels in semiconductor (linear approximation)
    E_f_quasi = E_f_left + (E_f_right - E_f_left) * (x_semiconductor / semiconductor_width)

    return {
        "x_metal_left": x_metal_left,
        "x_semiconductor": x_semiconductor,
        "x_metal_right": x_metal_right,
        "E_f_left": E_f_left,
        "E_f_right": E_f_right,
        "E_f_quasi": E_f_quasi,
        "E_vac_left": E_vac_left,
        "E_vac_right": E_vac_right,
        "E_vac_final": E_vac_final,
        "E_c": E_c,
        "E_v": E_v,
        "E_i": E_i,
    }

def calculate_pre_junction_bands(chi, eg, fermi_shift, wf_left, wf_right, **kwargs):
    """
    Calculates the energy band structure for materials before junction.
    All levels are relative to the vacuum level (E_vac = 0).
    Doping type is determined by the sign of fermi_shift.
    """
    # --- X-axis definition for separated materials ---
    # Match widths of the 'after' view for consistency
    metal_width = 10.0
    semiconductor_width = 20.0
    gap = 2.0 # Visual separation

    # Center the semiconductor around x=0
    semi_start = -semiconductor_width / 2
    semi_end = semiconductor_width / 2
    x_semiconductor = np.linspace(semi_start, semi_end, 100)

    # Place metals on either side with a gap
    x_metal_left = np.linspace(semi_start - gap - metal_width, semi_start - gap, 100)
    x_metal_right = np.linspace(semi_end + gap, semi_end + gap + metal_width, 100)

    # --- Left Metal ---
    E_vac_left = np.full_like(x_metal_left, 0)
    E_f_left = E_vac_left - wf_left

    # --- Right Metal ---
    E_vac_right = np.full_like(x_metal_right, 0)
    E_f_right = E_vac_right - wf_right

    # --- Semiconductor (flat bands) ---
    E_vac_semi = np.full_like(x_semiconductor, 0)
    E_c = E_vac_semi - chi
    E_v = E_c - eg
    E_i = E_c - eg / 2
    # E_f relative to E_i, matching the convention (positive shift is n-type, higher energy)
    E_f_semi = E_i + fermi_shift

    return {
        "x_metal_left": x_metal_left,
        "E_vac_left": E_vac_left,
        "E_f_left": E_f_left,
        "x_semiconductor": x_semiconductor,
        "E_vac_semi": E_vac_semi,
        "E_c": E_c,
        "E_v": E_v,
        "E_i": E_i,
        "E_f_semi": E_f_semi,
        "x_metal_right": x_metal_right,
        "E_vac_right": E_vac_right,
        "E_f_right": E_f_right,
    }