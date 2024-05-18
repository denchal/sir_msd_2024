import tkinter as tk
from SIR import run
from tkinter import ttk

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

start_button = ttk.Button(root, text="Start", command=start_simulation)
start_button.grid(row=len(parameters), column=0, padx=10, pady=10, sticky=tk.W)

exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=len(parameters), column=1, padx=10, pady=10, sticky=tk.E)

root.mainloop()

