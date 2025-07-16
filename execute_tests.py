import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def get_directories(path):
    # Return only directories in the given path, excluding __pycache__ and hidden/system dirs
    return [
        name for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))
        and not name.startswith('__')
        and not name.startswith('.')
    ]

def run_tests():
    sn = sn_entry.get()
    selected_dir = dir_var.get()
    if not sn:
        messagebox.showerror("Error", "Please enter a serial number.")
        return
    if not selected_dir:
        messagebox.showerror("Error", "Please select a directory.")
        return

    # Show in-progress popup
    progress = tk.Toplevel(root)
    progress.title("Running Tests")
    tk.Label(progress, text="🕒 Running tests...\nPlease wait.", font=("Arial", 12)).pack(padx=20, pady=20)
    progress.update()

    root.update_idletasks()

    os.environ["UNIT_SN"] = sn
    try:
        result = subprocess.run(
            ["pytest", ".", f"--html=reports/report_{sn}.html", "--self-contained-html"],
            capture_output=True, text=True,
            cwd=os.path.join(test_suites_dir, selected_dir)
        )
    finally:
        progress.destroy()

    messagebox.showinfo("Done", f"Test report generated: report_{sn}.html\n\n{result.stdout}")

root = tk.Tk()
root.geometry("300x200")  # Set default size: width x height
root.title("Run MCC Tests")

tk.Label(root, text="Enter Serial Number:").pack(pady=5)
sn_entry = tk.Entry(root)
sn_entry.pack(pady=5)

# Dropdown for directories
test_suites_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_suites")
dirs = get_directories(test_suites_dir)
dir_var = tk.StringVar()
tk.Label(root, text="Select Directory:").pack(pady=5)
dir_dropdown = ttk.Combobox(root, textvariable=dir_var, values=dirs, state="readonly")
dir_dropdown.pack(pady=5)
if dirs:
    dir_dropdown.current(0)

tk.Button(root, text="Run Tests", command=run_tests).pack(pady=10)

root.mainloop()
