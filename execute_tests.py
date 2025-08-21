import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import pytest


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def get_directories(path):
    if not os.path.exists(path):
        return []
    return [
        name for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))
        and not name.startswith('__')
        and not name.startswith('.')
    ]

class MCCApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x200")
        self.root.title("Run MCC Tests")

        tk.Label(root, text="Enter Serial Number:").pack(pady=5)
        self.sn_entry = tk.Entry(root)
        self.sn_entry.pack(pady=5)

        tk.Label(root, text="Select Directory:").pack(pady=5)
        self.test_suites_dir = resource_path("test_suites")
        dirs = get_directories(self.test_suites_dir)
        self.dir_var = tk.StringVar()
        self.dir_dropdown = ttk.Combobox(root, textvariable=self.dir_var, values=dirs, state="readonly")
        self.dir_dropdown.pack(pady=5)
        if dirs:
            self.dir_dropdown.current(0)

        tk.Button(root, text="Run Tests", command=self.run_tests).pack(pady=10)

    def run_tests(self):
        sn = self.sn_entry.get()
        selected_dir = self.dir_var.get()
        if not sn:
            messagebox.showerror("Error", "Please enter a serial number.")
            return
        if not selected_dir:
            messagebox.showerror("Error", "Please select a directory.")
            return

        self.progress = tk.Toplevel(self.root)
        self.progress.title("Running Tests")
        self.progress.geometry("300x120")
        tk.Label(self.progress, text="🕒 Running tests...\nPlease wait.", font=("Arial", 12)).pack(padx=20, pady=20)
        self.progress.update()
        self.root.update_idletasks()

        thread = threading.Thread(target=self._run_pytest, args=(sn, selected_dir))
        thread.start()

    def _run_pytest(self, sn, selected_dir):
        import pytest
        # Always use resource_path to find test_suites
        test_suites_dir = resource_path("test_suites")
        test_dir_path = os.path.abspath(os.path.join(test_suites_dir, selected_dir))
        reports_dir = resource_path("reports")
        os.makedirs(reports_dir, exist_ok=True)
        output_report = os.path.join(reports_dir, f"report_{sn}.html")

        # Determine the bundle root (where conftest.py is)
        if hasattr(sys, '_MEIPASS'):
            bundle_root = sys._MEIPASS
        else:
            bundle_root = os.path.dirname(os.path.abspath(__file__))

        old_cwd = os.getcwd()
        try:
            os.chdir(bundle_root)
            sys.path.insert(0, bundle_root)
            print("CWD:", os.getcwd())
            print("sys.path:", sys.path)
            print("test_dir_path:", test_dir_path)
            print("test_suites_dir:", test_suites_dir)
            print("Files in test_dir_path:", os.listdir(test_dir_path))
            tests_path = os.path.join(test_dir_path, "tests")
            print("tests_path:", tests_path)
            result = pytest.main([
                tests_path,
                f"--html={output_report}", "--self-contained-html"
            ])
            print("pytest.main() result:", result)
        except Exception as e:
            messagebox.showerror("Error", f"Test run failed:\n{e}")
        finally:
            os.chdir(old_cwd)
            self.progress.destroy()
        messagebox.showinfo("Done", f"Test report generated: \n{output_report}")
        webbrowser.open(output_report)

if __name__ == "__main__":
    root = tk.Tk()
    app = MCCApp(root)
    root.mainloop()
