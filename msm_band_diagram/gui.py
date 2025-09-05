import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from . import plotter

class BandDiagramApp:
    def __init__(self, master):
        self.master = master
        master.title("MSM BandDiagram (GUI)")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Main Frame ---
        main_frame = ttk.Frame(master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # --- Parameters Frame ---
        params_frame = ttk.LabelFrame(main_frame, text="Parameters Input", padding="10")
        params_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # --- View Options ---
        view_frame = ttk.LabelFrame(params_frame, text="View Options", padding="5")
        view_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.view_type = tk.StringVar(value="after")
        ttk.Radiobutton(view_frame, text="Before Junction", variable=self.view_type, value="before", command=self.plot).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(view_frame, text="After Junction", variable=self.view_type, value="after", command=self.plot).grid(row=0, column=1, padx=5)

        # --- Semiconductor Parameters ---
        semi_frame = ttk.LabelFrame(params_frame, text="Semiconductor", padding="5")
        semi_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=5)
        ttk.Label(semi_frame, text="Electron Affinity (χ)").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.electron_affinity = tk.StringVar(value="4.05")
        ttk.Entry(semi_frame, textvariable=self.electron_affinity, width=10).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(semi_frame, text="eV").grid(row=0, column=2, sticky=tk.W)

        ttk.Label(semi_frame, text="Band Gap (Eg)").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.band_gap = tk.StringVar(value="1.12")
        ttk.Entry(semi_frame, textvariable=self.band_gap, width=10).grid(row=1, column=1, sticky=tk.W)
        ttk.Label(semi_frame, text="eV").grid(row=1, column=2, sticky=tk.W)

        ttk.Label(semi_frame, text="Fermi Shift (from Ei)").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.fermi_shift = tk.StringVar(value="0.2")
        ttk.Entry(semi_frame, textvariable=self.fermi_shift, width=10).grid(row=2, column=1, sticky=tk.W)
        ttk.Label(semi_frame, text="eV (+n, -p)").grid(row=2, column=2, sticky=tk.W)

        # --- Electrode Parameters ---
        electrode_frame = ttk.LabelFrame(params_frame, text="Electrodes", padding="5")
        electrode_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=5)

        ttk.Label(electrode_frame, text="Left Electrode Work Function").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.left_wf = tk.StringVar(value="4.2")
        ttk.Entry(electrode_frame, textvariable=self.left_wf, width=10).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(electrode_frame, text="eV").grid(row=0, column=2, sticky=tk.W)

        ttk.Label(electrode_frame, text="Left Electrode Label").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.left_label = tk.StringVar(value="Al")
        ttk.Entry(electrode_frame, textvariable=self.left_label, width=10).grid(row=1, column=1, sticky=tk.W)

        ttk.Label(electrode_frame, text="Right Electrode Work Function").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.right_wf = tk.StringVar(value="5.1")
        ttk.Entry(electrode_frame, textvariable=self.right_wf, width=10).grid(row=2, column=1, sticky=tk.W)
        ttk.Label(electrode_frame, text="eV").grid(row=2, column=2, sticky=tk.W)

        ttk.Label(electrode_frame, text="Right Electrode Label").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.right_label = tk.StringVar(value="Au")
        ttk.Entry(electrode_frame, textvariable=self.right_label, width=10).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(electrode_frame, text="Bias Voltage").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.bias_voltage = tk.StringVar(value="0.0")
        ttk.Entry(electrode_frame, textvariable=self.bias_voltage, width=10).grid(row=4, column=1, sticky=tk.W)
        ttk.Label(electrode_frame, text="V").grid(row=4, column=2, sticky=tk.W)

        # --- Action Buttons Frame ---
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, pady=10)
        ttk.Button(buttons_frame, text="Plot", command=self.plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Save Plot", command=self.save_plot).pack(side=tk.LEFT, padx=5)

        # --- Plot Frame ---
        plot_frame = ttk.LabelFrame(main_frame, text="Band Diagram", padding="10")
        plot_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.plot() # Initial plot

    def on_closing(self):
        self.master.quit()
        self.master.destroy()

    def plot(self):
        try:
            params = {
                'chi': float(self.electron_affinity.get()),
                'eg': float(self.band_gap.get()),
                'fermi_shift': float(self.fermi_shift.get()),
                'wf_left': float(self.left_wf.get()),
                'wf_right': float(self.right_wf.get()),
                'label_left': self.left_label.get(),
                'label_right': self.right_label.get(),
                'bias': float(self.bias_voltage.get())
            }
        except ValueError:
            messagebox.showerror("Input Error", "Invalid numerical value entered.")
            return
        
        view_type = self.view_type.get()
        if view_type == 'before':
            plotter.draw_pre_junction_diagram(self.ax, **params)
        else: # after
            plotter.draw_band_diagram(self.ax, **params)

        self.fig.tight_layout(rect=[0, 0, 0.85, 1])
        self.canvas.draw()

    def save_plot(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("SVG files", "*.svg"),
                ("All files", "*.*"),
            ])
        if not file_path:
            return
        try:
            self.fig.savefig(file_path, bbox_inches='tight')
            messagebox.showinfo("Success", f"Plot saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save plot: {e}")

def main():
    root = tk.Tk()
    app = BandDiagramApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
