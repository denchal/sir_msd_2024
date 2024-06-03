import tkinter as tk
from SIR import run
from tkinter import ttk
from tkinter import filedialog
import threading

ADVANCED = False
POPULATIONS = []
PATIENTS_ZERO = []
SIZES =[]

def load_params():
    path = filedialog.askopenfilename(filetypes=[("SIR files", ".SIR")])
    if not path:
        return
    
    with open(path, 'r') as file:
            lines = file.readlines()

    reset()

    avg_pop.insert(0, lines[0].strip())
        
    avg_size.insert(0, lines[1].strip())

    max_patients_zero.insert(0, lines[2].strip())

    neighbourhood_size.insert(0, lines[3].strip())

    n_cities.insert(0, lines[4].strip())

    travel_rate.insert(0, lines[5].strip())

    infection_rate.insert(0, lines[6].strip())

    infection_time.insert(0, lines[7].strip())

    days.insert(0, lines[8].strip())

def reset():
    global ADVANCED, POPULATIONS, PATIENTS_ZERO, SIZES
    avg_pop.config(state='enabled')
    avg_size.config(state='enabled')
    max_patients_zero.config(state='enabled')
    
    avg_pop.delete(0, tk.END)
        
    avg_size.delete(0, tk.END)

    max_patients_zero.delete(0, tk.END)

    neighbourhood_size.delete(0, tk.END)

    n_cities.delete(0, tk.END)

    travel_rate.delete(0, tk.END)

    infection_rate.delete(0, tk.END)

    infection_time.delete(0, tk.END)

    days.delete(0, tk.END)

    ADVANCED = False
    POPULATIONS = []
    PATIENTS_ZERO = []
    SIZES = []

def start_simulation():
    global ADVANCED, POPULATIONS, PATIENTS_ZERO, SIZES
    if not ADVANCED:
         parameters = [
            int(avg_pop.get()),
            int(avg_size.get()),
            int(max_patients_zero.get()),
            int(neighbourhood_size.get()),
            int(n_cities.get()),
            float(travel_rate.get()),
            float(infection_rate.get()),
            int(infection_time.get()),
            int(days.get()),
            bool(quarantine.get())
        ]
    else:
         parameters = [
            POPULATIONS,
            SIZES,
            PATIENTS_ZERO,
            int(neighbourhood_size.get()),
            int(n_cities.get()),
            float(travel_rate.get()),
            float(infection_rate.get()),
            int(infection_time.get()),
            int(days.get()),
            bool(quarantine.get())
         ]

    def run_():
         run(parameters, ADVANCED)

    threading.Thread(target=run_).start()

def open_advanced_options():
    global ADVANCED, POPULATIONS, PATIENTS_ZERO, SIZES
    n = int(n_cities.get())
    advanced_window = tk.Toplevel(root)
    advanced_window.title("Zaawansowane opcje")

    ttk.Label(advanced_window, text="Miasto").grid(row=0, column=0)
    ttk.Label(advanced_window, text="Populacja").grid(row=0, column=1)
    ttk.Label(advanced_window, text="Pacjenci zero").grid(row=0, column=2)
    ttk.Label(advanced_window, text="Rozmiar").grid(row=0, column=3)

    entries_pop = []
    entries_patients = []
    entries_size = []
    
    for i in range(n):
        ttk.Label(advanced_window, text=f"Miasto {i+1}").grid(row=i+1, column=0)
        pop_entry = ttk.Entry(advanced_window)
        pop_entry.grid(row=i+1, column=1)
        POPULATIONS.append(pop_entry)
        entries_pop.append(pop_entry)

        patient_entry = ttk.Entry(advanced_window)
        patient_entry.grid(row=i+1, column=2)
        PATIENTS_ZERO.append(patient_entry)
        entries_patients.append(patient_entry)

        size_entry = ttk.Entry(advanced_window)
        size_entry.grid(row=i+1, column=3)
        SIZES.append(size_entry)
        entries_size.append(size_entry)

    def advanced():
        global ADVANCED, POPULATIONS, PATIENTS_ZERO, SIZES
        ADVANCED = True
        avg_pop.config(state='disabled')
        avg_size.config(state='disabled')
        max_patients_zero.config(state='disabled')
        
        POPULATIONS = [int(pop.get()) for pop in entries_pop]
        PATIENTS_ZERO = [int(patient.get()) for patient in entries_patients]
        SIZES = [int(size.get()) for size in entries_size]
        
        advanced_window.destroy()
    
    save_button = ttk.Button(advanced_window, text="Save", command=advanced)
    save_button.grid(row=n+1, column=1, columnspan=2)


root = tk.Tk()
root.title("SIR")

parameters = [
    ("Average Population", 1000),
    ("Average City Size", 300),
    ("Max Initial Patients Zero", 5),
    ("Neighbourhood Size", 3),
    ("Number of Cities", 10),
    ("Travel Rate", 0.1),
    ("Infection Rate", 1),
    ("Infection Time", 10),
    ("Simulation Days", 100)
]

entries = {}
for i, (param, default) in enumerate(parameters):
    label = ttk.Label(root, text=param)
    label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
    entry = ttk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entry.insert(0, str(default))
    entries[param] = entry

avg_pop = entries["Average Population"]
avg_size = entries["Average City Size"]
max_patients_zero = entries["Max Initial Patients Zero"]
neighbourhood_size = entries["Neighbourhood Size"]
n_cities = entries["Number of Cities"]
travel_rate = entries["Travel Rate"]
infection_rate = entries["Infection Rate"]
infection_time = entries["Infection Time"]
days = entries["Simulation Days"]

quarantine = tk.BooleanVar()
quarantine_checkbox = ttk.Checkbutton(root, text="Kwarantanna", variable=quarantine)
quarantine_checkbox.grid(row=len(parameters) + 1, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

load_button = ttk.Button(root, text="Load from file", command=load_params)
load_button.grid(row=len(parameters), column=0, padx=10, pady=10, sticky=tk.E)

start_button = ttk.Button(root, text="Start", command=start_simulation)
start_button.grid(row=len(parameters), column=1, padx=10, pady=10, sticky=tk.E)

exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=len(parameters), column=4, padx=10, pady=10, sticky=tk.E)

reset_button = ttk.Button(root, text="Reset", command=reset)
reset_button.grid(row=len(parameters), column=2, padx=10, pady=10, sticky=tk.E)

advanced_button = ttk.Button(root, text="Advanced", command=open_advanced_options)
advanced_button.grid(row=len(parameters), column=3, padx=10, pady=10, sticky=tk.E)

root.mainloop()

