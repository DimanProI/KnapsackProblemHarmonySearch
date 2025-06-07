import random
import time
import matplotlib.pyplot as plt
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import numpy as np

class Knapsack:
    def __init__(self, items, max_weight):
        self.items = items
        self.max_weight = max_weight

    def evaluate(self, solution):
        total_weight = sum(self.items[i][0] for i in range(len(solution)) if solution[i] == 1)
        total_value = sum(self.items[i][1] for i in range(len(solution)) if solution[i] == 1)
        if total_weight > self.max_weight:
            return 0
        return total_value

    def is_feasible(self):
        return any(item[0] <= self.max_weight for item in self.items)

# Алгоритм поиска гармонии
class HarmonySearch:
    def __init__(self, knapsack, hms=10, hmcr=0.9, par=0.3, max_iter=100):
        self.knapsack = knapsack
        self.hms = hms
        self.hmcr = hmcr
        self.par = par
        self.max_iter = max_iter
        self.memory = []
        self.best_solution = None
        self.best_value = 0
        self.convergence = []
        self.best_iteration = 0

    def initialize_memory(self):
        self.memory = []
        n_items = len(self.knapsack.items)
        for _ in range(self.hms):
            solution = [0] * n_items
            available_indices = [i for i, item in enumerate(self.knapsack.items) if item[0] <= self.knapsack.max_weight]
            if available_indices:
                num_items = random.randint(0, min(5, len(available_indices)))
                selected = random.sample(available_indices, num_items)
                for idx in selected:
                    if sum(self.knapsack.items[i][0] for i in range(n_items) if solution[i] == 1 or i == idx) <= self.knapsack.max_weight:
                        solution[idx] = 1
            self.memory.append(solution)
        self.best_solution = max(self.memory, key=self.knapsack.evaluate, default=[0] * n_items)
        self.best_value = self.knapsack.evaluate(self.best_solution)
        self.convergence.append(self.best_value)

    def improvise(self):
        new_solution = [0] * len(self.knapsack.items)
        for i in range(len(self.knapsack.items)):
            if random.random() < self.hmcr:
                new_solution[i] = random.choice([sol[i] for sol in self.memory])
                if random.random() < self.par:
                    new_solution[i] = 1 - new_solution[i]
            else:
                new_solution[i] = random.randint(0, 1)
            if new_solution[i] == 1 and sum(self.knapsack.items[j][0] for j in range(len(new_solution)) if new_solution[j] == 1) > self.knapsack.max_weight:
                new_solution[i] = 0
        return new_solution

    def run(self):
        self.initialize_memory()
        last_improvement = 0
        for iteration in range(self.max_iter):
            new_solution = self.improvise()
            new_value = self.knapsack.evaluate(new_solution)
            worst_value = min(self.knapsack.evaluate(sol) for sol in self.memory)
            if new_value > worst_value:
                worst_idx = min(range(len(self.memory)), key=lambda i: self.knapsack.evaluate(self.memory[i]))
                self.memory[worst_idx] = new_solution
                if new_value > self.best_value:
                    self.best_solution = new_solution
                    self.best_value = new_value
                    last_improvement = iteration + 1
            self.convergence.append(self.best_value)
        self.best_iteration = last_improvement
        return self.best_solution, self.best_value, self.best_iteration

# GUI и основная программа
class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Problem - Harmony Search")
        self.style = ttk.Style("darkly")
        self.current_theme = "darkly" 
        self.items = []
        self.params = {"max_weight": 0, "hms": 10, "hmcr": 0.9, "par": 0.3, "max_iter": 100, "vary_param": "hms", "vary_values": [5, 10, 20]}
        self.convergence_data = []
        self.execution_times = []
        self.best_iterations = []

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky=(N, S, E, W))
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=1)
        self.main_frame.columnconfigure(3, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        ttk.Button(self.main_frame, text="Load Items", command=self.load_items).grid(row=0, column=0, padx=5, pady=5, sticky=(E, W))
        ttk.Button(self.main_frame, text="Load Parameters", command=self.load_params).grid(row=0, column=1, padx=5, pady=5, sticky=(E, W))
        ttk.Button(self.main_frame, text="Run Algorithm", command=self.run_algorithm).grid(row=0, column=2, padx=5, pady=5, sticky=(E, W))
        self.theme_button = ttk.Button(self.main_frame, text="Switch to Light Theme", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=3, padx=5, pady=5, sticky=(E, W))

        self.result_text = ttk.Text(self.main_frame, height=10, width=50)
        self.result_text.grid(row=1, column=0, columnspan=4, pady=10, sticky=(N, S, E, W)) 

        ttk.Button(self.main_frame, text="Show Convergence Plot", command=self.plot_convergence).grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky=(E, W))  # Обновляем columnspan

    def toggle_theme(self):
        """Переключение между светлой и темной темой"""
        if self.current_theme == "darkly":
            self.style.theme_use("litera")  
            self.current_theme = "litera"
            self.theme_button.configure(text="Switch to Dark Theme")
            plt.style.use('default')  
        else:
            self.style.theme_use("darkly")  
            self.current_theme = "darkly"
            self.theme_button.configure(text="Switch to Light Theme")
            plt.style.use('dark_background') 

    def load_items(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    self.items = [tuple(map(float, line.strip().split())) for line in lines]
                self.result_text.delete(1.0, END)
                self.result_text.insert(END, f"Loaded items:\nItems: {self.items}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load items: {e}")

    def load_params(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    vary_param = lines[5].strip()
                    if vary_param in ["hms", "max_iter"]:
                        vary_values = [int(float(x)) for x in lines[6].strip().split()]
                    else:
                        vary_values = [float(x) for x in lines[6].strip().split()]
                    self.params = {
                        "max_weight": float(lines[0].strip()),
                        "hms": int(lines[1].strip()),
                        "hmcr": float(lines[2].strip()),
                        "par": float(lines[3].strip()),
                        "max_iter": int(lines[4].strip()),
                        "vary_param": vary_param,
                        "vary_values": vary_values
                    }
                    if self.params["vary_param"] not in ["hms", "hmcr", "par", "max_iter"]:
                        raise ValueError("Invalid vary_param. Must be one of: hms, hmcr, par, max_iter")
                    if not self.params["vary_values"]:
                        raise ValueError("vary_values must contain at least one value")
                    if self.params["vary_param"] == "hms" and any(v <= 0 for v in self.params["vary_values"]):
                        raise ValueError("hms values must be positive integers")
                    if self.params["vary_param"] == "max_iter" and any(v <= 0 for v in self.params["vary_values"]):
                        raise ValueError("max_iter values must be positive integers")
                    if self.params["vary_param"] in ["hmcr", "par"] and any(v < 0 or v > 1 for v in self.params["vary_values"]):
                        raise ValueError("hmcr and par values must be between 0 and 1")
                self.result_text.insert(END, f"Loaded parameters:\n{self.params}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load parameters: {e}")

    def run_algorithm(self):
        if not self.items or self.params["max_weight"] == 0:
            messagebox.showerror("Error", "Please load items and parameters first!")
            return

        knapsack = Knapsack(self.items, self.params["max_weight"])
        if not knapsack.is_feasible():
            messagebox.showwarning("Warning", "No feasible solution exists: all items exceed max_weight!")
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, "No feasible solution exists: all items exceed max_weight!\n")
            return

        self.convergence_data = []
        self.execution_times = []
        self.best_iterations = []
        param_to_vary = self.params["vary_param"]
        param_values = self.params["vary_values"]

        self.result_text.delete(1.0, END)
        for value in param_values:
            params = self.params.copy()
            params[param_to_vary] = value if param_to_vary != "hms" else int(value)
            params[param_to_vary] = value if param_to_vary != "max_iter" else int(value)
            hs = HarmonySearch(knapsack, params["hms"], params["hmcr"], params["par"], params["max_iter"])
            start_time = time.time()
            best_solution, best_value, best_iteration = hs.run()
            execution_time = time.time() - start_time
            self.convergence_data.append((value, hs.convergence))
            self.execution_times.append(execution_time)
            self.best_iterations.append(best_iteration)

            self.result_text.insert(END, f"\nParameter {param_to_vary} = {value}:\n")
            self.result_text.insert(END, f"Best Solution: {best_solution}\n")
            self.result_text.insert(END, f"Total Value: {best_value}\n")
            self.result_text.insert(END, f"Total Weight: {sum(self.items[i][0] for i in range(len(best_solution)) if best_solution[i] == 1)}\n")
            self.result_text.insert(END, f"Execution Time: {execution_time:.4f} seconds\n")
            self.result_text.insert(END, f"Best Value Found at Iteration: {best_iteration}\n")
            if best_value == 0:
                self.result_text.insert(END, "Warning: No feasible solution found (Total Value = 0)!\n")

    def plot_convergence(self):
        if not self.convergence_data:
            messagebox.showerror("Error", "Run the algorithm first!")
            return

        plt.style.use('default' if self.current_theme == "litera" else 'dark_background')
        fig, ax = plt.subplots()
        param_to_vary = self.params["vary_param"]
        for value, convergence in self.convergence_data:
            ax.plot(convergence, label=f"{param_to_vary}={value}")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Objective Value")
        ax.set_title(f"Convergence Plot for Varying {param_to_vary}")
        ax.legend()
        plt.show()

# Запуск программы
if __name__ == "__main__":
    root = ttk.Window()
    app = KnapsackApp(root)
    root.mainloop()
