import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def run_tests():
    sn = sn_entry.get()
    if not sn:
        messagebox.showerror("Error", "Please enter a serial number.")
        return
    os.environ["UNIT_SN"] = sn
    result = subprocess.run(
        ["pytest", "tests/", f"--html=reports/report_{sn}.html", "--self-contained-html"],
        capture_output=True, text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))  # Change working directory
    )
    messagebox.showinfo("Done", f"Test report generated: report_{sn}.html\n\n{result.stdout}")

root = tk.Tk()
root.title("Run MCC Tests")

tk.Label(root, text="Enter Serial Number:").pack(pady=5)
sn_entry = tk.Entry(root)
sn_entry.pack(pady=5)
tk.Button(root, text="Run Tests", command=run_tests).pack(pady=10)

root.mainloop()
