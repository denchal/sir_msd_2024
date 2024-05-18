import tkinter as tk
from SIR import run
from tkinter import ttk
from tkinter import filedialog

def load_params():
    path = filedialog.askopenfilename(filetypes=[("SIR files", "*.SIR")])
    if not path:
        return
    
    with open(path, 'r') as file:
            lines = file.readlines()

    if len(lines) < 9:
         reset()

    avg_pop.delete(0, tk.END)
    avg_pop.insert(0, lines[0].strip())
        
    avg_size.delete(0, tk.END)
    avg_size.insert(0, lines[1].strip())

    max_patients_zero.delete(0, tk.END)
    max_patients_zero.insert(0, lines[2].strip())

    neighbourhood_size.delete(0, tk.END)
    neighbourhood_size.insert(0, lines[3].strip())

    n_cities.delete(0, tk.END)
    n_cities.insert(0, lines[4].strip())

    travel_rate.delete(0, tk.END)
    travel_rate.insert(0, lines[5].strip())

    infection_rate.delete(0, tk.END)
    infection_rate.insert(0, lines[6].strip())

    infection_time.delete(0, tk.END)
    infection_time.insert(0, lines[7].strip())

    days.delete(0, tk.END)
    days.insert(0, lines[8].strip())

def reset():
    avg_pop.delete(0, tk.END)
        
    avg_size.delete(0, tk.END)

    max_patients_zero.delete(0, tk.END)

    neighbourhood_size.delete(0, tk.END)

    n_cities.delete(0, tk.END)

    travel_rate.delete(0, tk.END)

    infection_rate.delete(0, tk.END)

    infection_time.delete(0, tk.END)

    days.delete(0, tk.END)

def start_simulation():
    AVG_POP = int(avg_pop.get())
    AVG_SIZE = int(avg_size.get())
    MAX_PATIENTS_ZERO = int(max_patients_zero.get())
    NEIGHBOURHOOD_SIZE = int(neighbourhood_size.get())
    N_CITIES = int(n_cities.get())
    TRAVEL_RATE = float(travel_rate.get())
    INFECTION_RATE = float(infection_rate.get())
    INFECTION_TIME = int(infection_time.get())
    DAYS = int(days.get())

    root.destroy()

    run(AVG_POP, AVG_SIZE, MAX_PATIENTS_ZERO, NEIGHBOURHOOD_SIZE,
                       N_CITIES, TRAVEL_RATE, INFECTION_RATE, INFECTION_TIME, DAYS)

root = tk.Tk()
root.title("SIR")

parameters = [
    ("Average Population", 1000),
    ("Average City Size", 300),
    ("Max Initial Patients Zero", 5),
    ("Neighbourhood Size", 2),
    ("Number of Cities", 10),
    ("Travel Rate", 0.1),
    ("Infection Rate", 0.5),
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

load_button = ttk.Button(root, text="Load from file", command=load_params)
load_button.grid(row=len(parameters), column=0, padx=10, pady=10, sticky=tk.W)

start_button = ttk.Button(root, text="Start", command=start_simulation)
start_button.grid(row=len(parameters), column=1, padx=10, pady=10, sticky=tk.W)

exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=len(parameters), column=3, padx=10, pady=10, sticky=tk.E)

reset_button = ttk.Button(root, text="Reset", command=reset)
reset_button.grid(row=len(parameters), column=2, padx=10, pady=10, sticky=tk.E)

root.mainloop()

