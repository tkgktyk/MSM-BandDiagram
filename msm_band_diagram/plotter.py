import matplotlib.pyplot as plt
import numpy as np
from . import core # Use relative import within the package

def draw_band_diagram(ax, **params):
    """
    Calculates and draws a band diagram for the junction.
    This function acts as a controller that calls the calculation engine
    and then uses the results to draw the plot.
    """
    ax.clear()

    # 1. Calculate the band structure
    data = core.calculate_band_structure(**params)

    # --- Unpack data for convenience ---
    x_metal_left = data["x_metal_left"]
    x_semiconductor = data["x_semiconductor"]
    x_metal_right = data["x_metal_right"]
    E_f_left = data["E_f_left"]
    E_f_right = data["E_f_right"]
    E_f_quasi = data["E_f_quasi"]
    E_vac_left = data["E_vac_left"]
    E_vac_right = data["E_vac_right"]
    E_vac_final = data["E_vac_final"]
    E_c = data["E_c"]
    E_v = data["E_v"]
    E_i = data["E_i"]

    # --- Unpack optional labels and bias from original params ---
    label_left = params.get('label_left', 'Metal 1')
    label_right = params.get('label_right', 'Metal 2')
    bias = params.get('bias', 0.0)
    wf_left = params.get('wf_left', 0.0)
    wf_right = params.get('wf_right', 0.0)


    # 2. Draw the plot using the calculated data
    # --- Draw Fermi Levels ---
    ax.plot(x_metal_left, np.full_like(x_metal_left, E_f_left), 'k--')
    ax.plot(x_metal_right, np.full_like(x_metal_right, E_f_right), 'k--')
    ax.plot(x_semiconductor, E_f_quasi, 'k--', label='Quasi-Fermi Level')

    # --- Draw Metal Regions ---
    ax.plot(x_metal_left, np.full_like(x_metal_left, E_vac_left), 'grey')
    ax.fill_between(x_metal_left, E_vac_left, E_f_left - 5, color='lightgrey')
    ax.text(x_metal_left[0], E_f_left - 0.1, f"{label_left}\nW={wf_left:.1f}eV", va='top', ha='left')

    ax.plot(x_metal_right, np.full_like(x_metal_right, E_vac_right), 'grey')
    ax.fill_between(x_metal_right, E_vac_right, E_f_right - 5, color='lightgrey')
    ax.text(x_metal_right[-1], E_f_right - 0.1, f"{label_right}\nW={wf_right:.1f}eV\nBias={bias:.1f}V", va='top', ha='right')

    # --- Draw Semiconductor Bands ---
    ax.plot(x_semiconductor, E_vac_final, 'grey', label='Vacuum Level (E_vac)')
    ax.plot(x_semiconductor, E_c, 'b-', label='Conduction Band (Ec)')
    ax.plot(x_semiconductor, E_v, 'r-', label='Valence Band (Ev)')
    ax.plot(x_semiconductor, E_i, 'g:', label='Intrinsic Level (Ei)')

    # --- Final Touches ---
    ax.set_xlabel("")
    ax.set_xticks([])
    ax.set_ylabel("Energy (eV)")
    ax.set_title("Energy Band Diagram (After Junction)")
    ax.grid(True, linestyle='--', alpha=0.6)

    # Create a legend with unique entries
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1.02, 1.0))

    # Adjust Y limits to show all content
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(min(ymin, E_f_left - 2, E_f_right - 2), max(ymax, E_vac_left + 1, E_vac_right + 1))

def draw_pre_junction_diagram(ax, **params):
    """
    Calculates and draws a band diagram for materials before junction.
    """
    ax.clear()

    # 1. Calculate the pre-junction band structures
    data = core.calculate_pre_junction_bands(**params)

    # --- Unpack data ---
    x_metal_left, E_vac_left, E_f_left = data["x_metal_left"], data["E_vac_left"], data["E_f_left"]
    x_semi, E_vac_semi, E_c, E_v, E_i, E_f_semi = data["x_semiconductor"], data["E_vac_semi"], data["E_c"], data["E_v"], data["E_i"], data["E_f_semi"]
    x_metal_right, E_vac_right, E_f_right = data["x_metal_right"], data["E_vac_right"], data["E_f_right"]

    # --- Unpack labels from original params ---
    label_left = params.get('label_left', 'Metal 1')
    label_right = params.get('label_right', 'Metal 2')
    wf_left = params.get('wf_left', 0.0)
    wf_right = params.get('wf_right', 0.0)
    chi = params.get('chi', 0.0)
    eg = params.get('eg', 0.0)

    # 2. Draw the plot
    # --- Left Metal ---
    ax.plot(x_metal_left, E_vac_left, 'grey')
    ax.fill_between(x_metal_left, E_vac_left, E_f_left - 5, color='lightgrey')
    ax.plot(x_metal_left, E_f_left, 'k--')
    ax.text(x_metal_left.mean(), 0.5, f"{label_left}\nW={wf_left:.1f}eV", va='top', ha='center')

    # --- Semiconductor ---
    ax.plot(x_semi, E_vac_semi, 'grey', label='Vacuum Level (E_vac)')
    ax.plot(x_semi, E_c, 'b-', label='Conduction Band (Ec)')
    ax.plot(x_semi, E_v, 'r-', label='Valence Band (Ev)')
    ax.plot(x_semi, E_i, 'g:', label='Intrinsic Level (Ei)')
    ax.plot(x_semi, E_f_semi, 'k--', label='Fermi Level (Ef)')
    ax.text(x_semi.mean(), 0.5, f"Semiconductor\nχ={chi:.1f}eV, Eg={eg:.1f}eV", va='top', ha='center')


    # --- Right Metal ---
    ax.plot(x_metal_right, E_vac_right, 'grey')
    ax.fill_between(x_metal_right, E_vac_right, E_f_right - 5, color='lightgrey')
    ax.plot(x_metal_right, E_f_right, 'k--')
    ax.text(x_metal_right.mean(), 0.5, f"{label_right}\nW={wf_right:.1f}eV", va='top', ha='center')


    # --- Final Touches ---
    ax.set_xlabel("Position (arbitrary units)")
    ax.set_xticks([])
    ax.set_ylabel("Energy (eV)")
    ax.set_title("Energy Band Diagram (Before Junction)")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1.02, 1.0))

    ymin, ymax = ax.get_ylim()
    ax.set_ylim(min(E_f_left.min(), E_f_right.min(), E_v.min()) - 1, ymax + 1)
