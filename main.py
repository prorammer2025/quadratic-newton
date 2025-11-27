import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

# Import solver
from newton_solver import find_roots_newton


class QuadraticNewtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quadratic Root Finder — Newton-Raphson")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Set icon if available
        try:
            if sys.platform.startswith("win"):
                self.root.iconbitmap(self.resource_path("assets/icon.ico"))
        except Exception:
            pass

        self.setup_ui()

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and PyInstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def setup_ui(self):
        # === Title ===
        title_label = tk.Label(
            self.root,
            text="Quadratic Equation Solver (Newton-Raphson)",
            font=("Helvetica", 16, "bold"),
        )
        title_label.pack(pady=(20, 10))

        # === Input Frame ===
        input_frame = ttk.LabelFrame(self.root, text="Enter Coefficients: ax² + bx + c = 0")
        input_frame.pack(padx=20, pady=10, fill="x")

        # Coefficient entries
        ttk.Label(input_frame, text="a =").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_a = ttk.Entry(input_frame, width=10)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5)
        self.entry_a.insert(0, "1")

        ttk.Label(input_frame, text="b =").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_b = ttk.Entry(input_frame, width=10)
        self.entry_b.grid(row=0, column=3, padx=5, pady=5)
        self.entry_b.insert(0, "0")

        ttk.Label(input_frame, text="c =").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.entry_c = ttk.Entry(input_frame, width=10)
        self.entry_c.grid(row=0, column=5, padx=5, pady=5)
        self.entry_c.insert(0, "-4")

        # === Buttons ===
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.solve_btn = ttk.Button(btn_frame, text="Solve", command=self.solve)
        self.solve_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear)
        self.clear_btn.pack(side="left", padx=5)

        # === Output Area ===
        output_frame = ttk.LabelFrame(self.root, text="Results")
        output_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.output_text = scrolledtext.ScrolledText(
            output_frame, wrap=tk.WORD, height=12, font=("Courier", 10)
        )
        self.output_text.pack(padx=10, pady=5, fill="both", expand=True)
        self.output_text.config(state=tk.DISABLED)

        # === Footer ===
        footer = tk.Label(
            self.root,
            text="Uses Newton-Raphson method with multiple initial guesses • Real roots only",
            font=("Helvetica", 8),
            fg="gray",
        )
        footer.pack(pady=(5, 15))

        # Bind Enter to Solve
        self.root.bind("<Return>", lambda e: self.solve())

    def get_coeffs(self):
        try:
            a = float(self.entry_a.get().strip())
            b = float(self.entry_b.get().strip())
            c = float(self.entry_c.get().strip())
            return a, b, c
        except ValueError:
            raise ValueError("All coefficients must be valid numbers.")

    def solve(self):
        try:
            a, b, c = self.get_coeffs()

            if a == 0:
                messagebox.showerror("Invalid Input", "Coefficient 'a' cannot be zero for a quadratic equation.")
                return

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)

            # Discriminant (for reference, not used in NR but shown)
            disc = b * b - 4 * a * c
            self.output_text.insert(tk.END, f"Equation: {a}x² + ({b})x + ({c}) = 0\n")
            self.output_text.insert(tk.END, f"Discriminant (Δ) = {disc:.6f}\n\n")

            if disc < 0:
                self.output_text.insert(tk.END, "⚠️  No real roots (complex roots only).\n")
                self.output_text.insert(tk.END, "Newton-Raphson may still converge to complex values, but this app shows only real roots.\n")
            else:
                self.output_text.insert(tk.END, "🔍 Searching for real roots using Newton-Raphson...\n")

            # Use Newton-Raphson
            roots = find_roots_newton(a, b, c)

            if roots:
                self.output_text.insert(tk.END, f"\n✅ Found {len(roots)} real root(s):\n")
                for i, r in enumerate(roots, 1):
                    # Verify residual
                    residual = a * r * r + b * r + c
                    self.output_text.insert(tk.END, f"  Root {i}: x = {r:.8f}  (f(x) = {residual:.2e})\n")
            else:
                self.output_text.insert(tk.END, "\n❌ No real root found via Newton-Raphson (may be due to poor convergence or only complex roots).\n")
                if disc >= 0:
                    self.output_text.insert(tk.END, "💡 Hint: For quadratics, use quadratic formula for guaranteed real roots when Δ ≥ 0.\n")

            self.output_text.config(state=tk.DISABLED)

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def clear(self):
        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.entry_c.delete(0, tk.END)
        self.entry_a.insert(0, "1")
        self.entry_b.insert(0, "0")
        self.entry_c.insert(0, "-4")
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)


# === Run App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = QuadraticNewtonApp(root)
    root.mainloop()