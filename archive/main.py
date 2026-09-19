import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from rate_mfp_rempi import calculate_rate


# ============================================================
# CONSTANTS
# ============================================================

k_B = 1.380649e-23       # Boltzmann constant [J K^-1]
h = 6.62607015e-34       # Planck constant [J s]
c = 299792458.0          # Speed of light [m s^-1]

# ============================================================
# VALUE GENERATION
# ============================================================

def make_values(start, stop, number, scale="linear"):
    """
    Generate either a single value or a range of values.

    scale:
        'linear'       -> np.linspace
        'logarithmic'  -> np.logspace
    """

    start = float(start)
    stop = float(stop)
    number = int(number)

    if number < 1:
        raise ValueError("Number of values must be at least 1.")

    if scale == "logarithmic":
        if start <= 0 or stop <= 0:
            raise ValueError(
                "Logarithmic ranges require positive start and stop values."
            )

        return np.logspace(
            np.log10(start),
            np.log10(stop),
            number
        )

    return np.linspace(start, stop, number)

# ============================================================
# GUI
# ============================================================

class PhotoionizationGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Multiphoton Photoionization Rate Calculator"
        )

        self.root.geometry(
            "760x850"
        )

        # ----------------------------------------------------
        # Range-selection variables
        # ----------------------------------------------------

        self.range_variable = tk.StringVar(
            value="none"
        )

        self.entries = {}

        self.build_gui()

    # ========================================================
    # GENERIC ENTRY
    # ========================================================

    def add_entry(
        self,
        parent,
        key,
        label,
        default,
        row
    ):

        ttk.Label(
            parent,
            text=label
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        entry = ttk.Entry(
            parent,
            width=18
        )

        entry.insert(
            0,
            str(default)
        )

        entry.grid(
            row=row,
            column=1,
            sticky="w",
            padx=5,
            pady=4
        )

        self.entries[key] = entry

    # ========================================================
    # RANGE WIDGET
    # ========================================================

    def add_variable(
        self,
        parent,
        key,
        label,
        default,
        row
    ):

        # ----------------------------------------------------
        # Checkbox
        # ----------------------------------------------------

        checkbox = ttk.Checkbutton(
            parent,
            text="Range",
            variable=self.range_variable,
            onvalue=key,
            offvalue="none",
            command=self.update_range_controls
        )

        checkbox.grid(
            row=row,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        # ----------------------------------------------------
        # Single value
        # ----------------------------------------------------

        ttk.Label(
            parent,
            text=label
        ).grid(
            row=row,
            column=1,
            sticky="w",
            padx=5,
            pady=4
        )

        single_entry = ttk.Entry(
            parent,
            width=14
        )

        single_entry.insert(
            0,
            str(default)
        )

        single_entry.grid(
            row=row,
            column=2,
            padx=5,
            pady=4
        )

        self.entries[key + "_single"] = single_entry

        # ----------------------------------------------------
        # Range frame
        # ----------------------------------------------------

        range_frame = ttk.Frame(parent)

        range_frame.grid(
            row=row,
            column=3,
            columnspan=3,
            padx=5,
            pady=4
        )

        ttk.Label(
            range_frame,
            text="Start"
        ).grid(
            row=0,
            column=0
        )

        start_entry = ttk.Entry(
            range_frame,
            width=11
        )

        start_entry.insert(
            0,
            str(default)
        )

        start_entry.grid(
            row=0,
            column=1,
            padx=3
        )

        ttk.Label(
            range_frame,
            text="Stop"
        ).grid(
            row=0,
            column=2
        )

        stop_entry = ttk.Entry(
            range_frame,
            width=11
        )

        stop_entry.insert(
            0,
            str(default)
        )

        stop_entry.grid(
            row=0,
            column=3,
            padx=3
        )

        ttk.Label(
            range_frame,
            text="N"
        ).grid(
            row=0,
            column=4
        )

        number_entry = ttk.Entry(
            range_frame,
            width=6
        )

        number_entry.insert(
            0,
            "3"
        )

        number_entry.grid(
            row=0,
            column=5,
            padx=3
        )

        self.entries[key + "_start"] = start_entry
        self.entries[key + "_stop"] = stop_entry
        self.entries[key + "_number"] = number_entry

        # Initially disabled
        self.range_widgets = getattr(
            self,
            "range_widgets",
            {}
        )

        self.range_widgets[key] = [
            start_entry,
            stop_entry,
            number_entry
        ]

    # ========================================================
    # ENABLE/DISABLE RANGE FIELDS
    # ========================================================

    def update_range_controls(self):

        selected = self.range_variable.get()

        for key, widgets in self.range_widgets.items():

            if key == selected:

                state = "normal"

            else:

                state = "disabled"

            for widget in widgets:

                widget.config(
                    state=state
                )

        # ----------------------------------------------------
        # Single values remain enabled only when that variable
        # is NOT selected as the range variable.
        # ----------------------------------------------------

        for key in ["intensity", "sigma", "temperature"]:

            if key == selected:

                self.entries[
                    key + "_single"
                ].config(
                    state="disabled"
                )

            else:

                self.entries[
                    key + "_single"
                ].config(
                    state="normal"
                )

    # ========================================================
    # BUILD GUI
    # ========================================================

    def build_gui(self):

        main = ttk.Frame(
            self.root,
            padding=12
        )

        main.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # PRESSURE
        # ====================================================

        pressure_frame = ttk.LabelFrame(
            main,
            text="Pressure range",
            padding=10
        )

        pressure_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            pressure_frame,
            text="Start [mbar]"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=4
        )

        pressure_start = ttk.Entry(
            pressure_frame,
            width=14
        )

        pressure_start.insert(
            0,
            "1e-7"
        )

        pressure_start.grid(
            row=0,
            column=1,
            padx=5,
            pady=4
        )

        ttk.Label(
            pressure_frame,
            text="Stop [mbar]"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=4
        )

        pressure_stop = ttk.Entry(
            pressure_frame,
            width=14
        )

        pressure_stop.insert(
            0,
            "1e-3"
        )

        pressure_stop.grid(
            row=0,
            column=3,
            padx=5,
            pady=4
        )

        ttk.Label(
            pressure_frame,
            text="Number"
        ).grid(
            row=0,
            column=4,
            padx=5,
            pady=4
        )

        pressure_number = ttk.Entry(
            pressure_frame,
            width=8
        )

        pressure_number.insert(
            0,
            "100"
        )

        pressure_number.grid(
            row=0,
            column=5,
            padx=5,
            pady=4
        )

        self.entries["pressure_start"] = pressure_start
        self.entries["pressure_stop"] = pressure_stop
        self.entries["pressure_number"] = pressure_number

        # ====================================================
        # CONSTANT / SINGLE PARAMETERS
        # ====================================================

        physical_frame = ttk.LabelFrame(
            main,
            text="Other parameters",
            padding=10
        )

        physical_frame.pack(
            fill="x",
            pady=5
        )

        self.add_entry(
            physical_frame,
            "radius",
            "Radius [mm]",
            0.5,
            0
        )

        self.add_entry(
            physical_frame,
            "order",
            "Multiphoton order",
            2,
            1
        )

        self.add_entry(
            physical_frame,
            "wavelength",
            "Wavelength [nm]",
            249.6,
            2
        )

        # ====================================================
        # VARIABLE PARAMETERS
        # ====================================================

        variable_frame = ttk.LabelFrame(
            main,
            text="Variable parameters",
            padding=10
        )

        variable_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            variable_frame,
            text="Select at most ONE parameter to use as a range."
        ).grid(
            row=0,
            column=0,
            columnspan=6,
            sticky="w",
            padx=5,
            pady=(0, 8)
        )

        # ----------------------------------------------------
        # Intensity
        # ----------------------------------------------------

        self.add_variable(
            variable_frame,
            "intensity",
            "Intensity [MW cm⁻²]",
            30,
            1
        )

        # ----------------------------------------------------
        # Sigma
        # ----------------------------------------------------

        self.add_variable(
            variable_frame,
            "sigma",
            "Sigma [cm^(2N) s^(N-1)]",
            4e-45,
            2
        )

        # ----------------------------------------------------
        # Temperature
        # ----------------------------------------------------

        self.add_variable(
            variable_frame,
            "temperature",
            "Temperature [°C]",
            150,
            3
        )

        # ====================================================
        # BUTTONS
        # ====================================================

        button_frame = ttk.Frame(main)

        # Prevent this frame from being compressed when the
        # plot frame expands.
        button_frame.pack(
            fill="x",
            side="bottom",
            pady=10
        )

        ttk.Button(
            button_frame,
            text="Generate Plot",
            command=self.generate_plot
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Generate & Save Plot",
            command=lambda: self.generate_plot(save=True)
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.destroy
        ).pack(
            side="right",
            padx=5
        )

        # ====================================================
        # PLOT DISPLAY
        # ====================================================

        self.plot_frame = ttk.LabelFrame(
            main,
            text="Plot",
            padding=5
        )

        self.plot_frame.pack(
            fill="both",
            expand=True,
            side="top",
            pady=5
        )

        # ====================================================
        # INITIAL GUI STATE
        # ====================================================

        self.update_range_controls()

    # ========================================================
    # READ VARIABLE
    # ========================================================

    def read_variable(
        self,
        key,
        scale
    ):

        selected = self.range_variable.get()

        # ----------------------------------------------------
        # Range mode
        # ----------------------------------------------------

        if selected == key:

            start = float(
                self.entries[
                    key + "_start"
                ].get()
            )

            stop = float(
                self.entries[
                    key + "_stop"
                ].get()
            )

            number = int(
                self.entries[
                    key + "_number"
                ].get()
            )

            return make_values(
                start,
                stop,
                number,
                scale
            )

        # ----------------------------------------------------
        # Single-value mode
        # ----------------------------------------------------

        value = float(
            self.entries[
                key + "_single"
            ].get()
        )

        return np.array(
            [value]
        )

    # ========================================================
    # READ ALL INPUTS
    # ========================================================

    def read_inputs(self):

        # ----------------------------------------------------
        # Pressure range
        # ----------------------------------------------------

        pressure_start = float(
            self.entries[
                "pressure_start"
            ].get()
        )

        pressure_stop = float(
            self.entries[
                "pressure_stop"
            ].get()
        )

        pressure_number = int(
            self.entries[
                "pressure_number"
            ].get()
        )

        if pressure_start <= 0 or pressure_stop <= 0:
            raise ValueError(
                "Pressure start and stop must be greater than zero."
            )

        if pressure_stop <= pressure_start:
            raise ValueError(
                "Pressure stop must be greater than pressure start."
            )

        if pressure_number < 2:
            raise ValueError(
                "Pressure number must be at least 2."
            )

        pressure = make_values(
            pressure_start,
            pressure_stop,
            pressure_number,
            "logarithmic"
        )

        # ----------------------------------------------------
        # Physical parameters
        # ----------------------------------------------------

        radius = float(
            self.entries[
                "radius"
            ].get()
        )

        order = int(
            self.entries[
                "order"
            ].get()
        )

        wavelength = float(
            self.entries[
                "wavelength"
            ].get()
        )

        if radius <= 0:
            raise ValueError(
                "Radius must be greater than zero."
            )

        if order < 1:
            raise ValueError(
                "Multiphoton order must be at least 1."
            )

        if wavelength <= 0:
            raise ValueError(
                "Wavelength must be greater than zero."
            )

        # ----------------------------------------------------
        # Variable parameters
        # ----------------------------------------------------

        intensity = self.read_variable(
            "intensity",
            "logarithmic"
        )

        sigma = self.read_variable(
            "sigma",
            "logarithmic"
        )

        temperature = self.read_variable(
            "temperature",
            "linear"
        )

        # ----------------------------------------------------
        # Validate variable values
        # ----------------------------------------------------

        if np.any(intensity <= 0):
            raise ValueError(
                "Intensity must be greater than zero."
            )

        if np.any(sigma <= 0):
            raise ValueError(
                "Sigma must be greater than zero."
            )

        if np.any(
            temperature + 273.15 <= 0
        ):
            raise ValueError(
                "Temperature must be above absolute zero."
            )

        return (
            pressure,
            radius,
            order,
            wavelength,
            intensity,
            sigma,
            temperature
        )

    # ========================================================
    # GENERATE PLOT
    # ========================================================

    def generate_plot(
        self,
        save=False
    ):

        try:

            (
                pressure,
                radius,
                order,
                wavelength,
                intensities,
                sigmas,
                temperatures
            ) = self.read_inputs()

            # ------------------------------------------------
            # Pressure axis
            # ------------------------------------------------

            pressures = pressure

            # ------------------------------------------------
            # Create figure
            # ------------------------------------------------

            fig, ax = plt.subplots(
                figsize=(9, 6)
            )

            selected = self.range_variable.get()

            # =================================================
            # INTENSITY RANGE
            # =================================================

            if selected == "intensity":

                for intensity in intensities:

                    rates = calculate_rate(
                        pressures,
                        radius,
                        temperatures[0],
                        order,
                        sigmas[0],
                        intensity,
                        wavelength
                    )

                    ax.loglog(
                        pressures,
                        rates,
                        label=(
                            f"I = {intensity:.3g} MW/cm²"
                        )
                    )

            # =================================================
            # SIGMA RANGE
            # =================================================

            elif selected == "sigma":

                for sigma in sigmas:

                    rates = calculate_rate(
                        pressures,
                        radius,
                        temperatures[0],
                        order,
                        sigma,
                        intensities[0],
                        wavelength
                    )

                    ax.loglog(
                        pressures,
                        rates,
                        label=(
                            f"σ = {sigma:.3g}"
                        )
                    )

            # =================================================
            # TEMPERATURE RANGE
            # =================================================

            elif selected == "temperature":

                for temperature in temperatures:

                    rates = calculate_rate(
                        pressures,
                        radius,
                        temperature,
                        order,
                        sigmas[0],
                        intensities[0],
                        wavelength
                    )

                    ax.loglog(
                        pressures,
                        rates,
                        label=(
                            f"T = {temperature:.3g} °C"
                        )
                    )

            # =================================================
            # SINGLE VALUES
            # =================================================

            else:

                rates = calculate_rate(
                    pressures,
                    radius,
                    temperatures[0],
                    order,
                    sigmas[0],
                    intensities[0],
                    wavelength
                )

                ax.loglog(
                    pressures,
                    rates,
                    linewidth=2,
                    label="Single parameter set"
                )

            # =================================================
            # FORMATTING
            # =================================================

            ax.set_xlabel(
                "Pressure [mbar]"
            )

            ax.set_ylabel(
                "Photoionization rate [s⁻¹]"
            )

            ax.set_title(
                f"{order}-Photon Ionization "
                f"(λ = {wavelength:g} nm)"
            )

            ax.grid(
                True,
                which="both",
                linestyle="--",
                alpha=0.4
            )

            ax.legend(
                fontsize=9
            )

            fig.tight_layout()

            # =================================================
            # SAVE
            # =================================================

            if save:

                filename = (
                    filedialog.asksaveasfilename(
                        title="Save plot",
                        defaultextension=".png",
                        filetypes=[
                            ("PNG", "*.png"),
                            ("PDF", "*.pdf"),
                            ("SVG", "*.svg"),
                            ("All files", "*.*")
                        ]
                    )
                )

                if filename:

                    fig.savefig(
                        filename,
                        dpi=300,
                        bbox_inches="tight"
                    )

                    messagebox.showinfo(
                        "Plot saved",
                        f"Plot saved to:\n{filename}"
                    )

            # ============================================================
            # DISPLAY PLOT IN TKINTER WINDOW
            # ============================================================

            # Remove any previously displayed plot
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            # Create Matplotlib canvas
            canvas = FigureCanvasTkAgg(
                fig,
                master=self.plot_frame
            )

            canvas.draw()

            # Add canvas to Tkinter frame
            canvas.get_tk_widget().pack(
                fill="both",
                expand=True
            )

            # Store reference so the canvas is not garbage-collected
            self.canvas = canvas


        except Exception as error:

            messagebox.showerror(
                "Input error",
                str(error)
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = PhotoionizationGUI(
        root
    )

    root.mainloop()
