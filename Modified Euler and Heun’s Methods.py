import tkinter as tk
from tkinter import ttk, messagebox
import math

SAFE_ENV = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}
SAFE_ENV.update({
    "abs": abs,
    "pow": pow
})


def normalize_expression(expression):
    return expression.strip().replace("^", "**").replace("−", "-")


def make_function(expression):
    expression = normalize_expression(expression)

    def f(x, y):
        return eval(expression, {"__builtins__": {}}, {**SAFE_ENV, "x": x, "y": y})

    return f


def make_exact_function(expression):
    expression = normalize_expression(expression)

    if expression == "":
        return None

    def exact(x):
        return eval(expression, {"__builtins__": {}}, {**SAFE_ENV, "x": x})

    return exact


def modified_euler(f, x0, y0, h, x_end, exact=None):
    rows = []
    x = x0
    y = y0

    while x < x_end - 1e-12:
        current_h = min(h, x_end - x)

        k1 = f(x, y)
        mid_x = x + current_h / 2
        mid_y = y + (current_h / 2) * k1
        k2 = f(mid_x, mid_y)

        y_next = y + current_h * k2
        x_next = x + current_h

        exact_value = exact(x_next) if exact else None
        error = abs(exact_value - y_next) if exact else None

        rows.append({
            "point": x_next,
            "numerical": y_next,
            "exact": exact_value,
            "error": error
        })

        x = round(x_next, 12)
        y = y_next

    return rows


def heun_method(f, x0, y0, h, x_end, exact=None):
    rows = []
    x = x0
    y = y0

    while x < x_end - 1e-12:
        current_h = min(h, x_end - x)

        k1 = f(x, y)
        y_predict = y + current_h * k1
        k2 = f(x + current_h, y_predict)

        y_next = y + (current_h / 2) * (k1 + k2)
        x_next = x + current_h

        exact_value = exact(x_next) if exact else None
        error = abs(exact_value - y_next) if exact else None

        rows.append({
            "point": x_next,
            "numerical": y_next,
            "exact": exact_value,
            "error": error
        })

        x = round(x_next, 12)
        y = y_next

    return rows


def fmt_point(value):
    return f"{value:.10f}".rstrip("0").rstrip(".")


def fmt_number(value):
    if value is None:
        return "-"
    return f"{value:.5f}".rstrip("0").rstrip(".")


def fmt_fixed(value):
    if value is None:
        return "-"
    return f"{value:.5f}"


def clear_results():
    for widget in result_frame.winfo_children():
        widget.destroy()


def create_result_table(parent, title, rows):
    title_label = ttk.Label(parent, text=title, font=("Arial", 13, "bold"))
    title_label.pack(pady=(15, 5))

    columns = ("point", "numerical", "exact", "error")

    tree = ttk.Treeview(parent, columns=columns, show="headings", height=len(rows))

    tree.heading("point", text="Point")
    tree.heading("numerical", text="Numerical solution")
    tree.heading("exact", text="Exact solution")
    tree.heading("error", text="Magnitude of error")

    tree.column("point", width=120, anchor="center")
    tree.column("numerical", width=180, anchor="center")
    tree.column("exact", width=180, anchor="center")
    tree.column("error", width=180, anchor="center")

    for row in rows:
        tree.insert(
            "",
            "end",
            values=(
                fmt_point(row["point"]),
                fmt_number(row["numerical"]),
                fmt_fixed(row["exact"]),
                fmt_fixed(row["error"])
            )
        )

    tree.pack(padx=10, pady=5)


def run_calculation():
    try:
        clear_results()

        expression = func_entry.get()
        f = make_function(expression)

        x0 = float(x0_entry.get())
        y0 = float(y0_entry.get())
        h = float(h_entry.get())
        x_end = float(x_end_entry.get())

        if h <= 0:
            raise ValueError("Step size h must be greater than 0.")

        if x_end <= x0:
            raise ValueError("Final x value must be greater than x0.")

        exact_expression = exact_entry.get()
        exact = make_exact_function(exact_expression)

        modified_rows = modified_euler(f, x0, y0, h, x_end, exact)
        heun_rows = heun_method(f, x0, y0, h, x_end, exact)

        create_result_table(
            result_frame,
            "Errors in the Modified Euler Method",
            modified_rows
        )

        create_result_table(
            result_frame,
            "Errors in Heun's Method",
            heun_rows
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Modified Euler and Heun's Methods")
root.geometry("850x700")

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

title = ttk.Label(
    main_frame,
    text="Modified Euler and Heun's Methods",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="Enter function f(x,y):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
func_entry = ttk.Entry(input_frame, width=30)
func_entry.grid(row=0, column=1, padx=10, pady=5)
func_entry.insert(0, "y+x")

ttk.Label(input_frame, text="Enter x0:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
x0_entry = ttk.Entry(input_frame, width=30)
x0_entry.grid(row=1, column=1, padx=10, pady=5)
x0_entry.insert(0, "0")

ttk.Label(input_frame, text="Enter y0:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
y0_entry = ttk.Entry(input_frame, width=30)
y0_entry.grid(row=2, column=1, padx=10, pady=5)
y0_entry.insert(0, "1")

ttk.Label(input_frame, text="Enter step size h:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
h_entry = ttk.Entry(input_frame, width=30)
h_entry.grid(row=3, column=1, padx=10, pady=5)
h_entry.insert(0, "0.1")

ttk.Label(input_frame, text="Enter final x value:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
x_end_entry = ttk.Entry(input_frame, width=30)
x_end_entry.grid(row=4, column=1, padx=10, pady=5)
x_end_entry.insert(0, "0.3")

ttk.Label(input_frame, text="Exact solution optional:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
exact_entry = ttk.Entry(input_frame, width=30)
exact_entry.grid(row=5, column=1, padx=10, pady=5)
exact_entry.insert(0, "2*e**x-x-1")

run_button = ttk.Button(main_frame, text="Run Calculation", command=run_calculation)
run_button.pack(pady=15)

result_frame = ttk.Frame(main_frame)
result_frame.pack(fill="both", expand=True)

root.mainloop()