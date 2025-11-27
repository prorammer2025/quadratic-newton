import math

def newton_raphson_quadratic(a, b, c, x0, tol=1e-8, max_iter=100):
    """
    Applies Newton-Raphson to f(x) = ax^2 + bx + c
    Returns (root, iterations, converged: bool)
    """
    if a == 0:
        raise ValueError("Coefficient 'a' must be non-zero for quadratic.")

    def f(x):
        return a * x * x + b * x + c

    def df(x):
        return 2 * a * x + b

    x = x0
    for i in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 1e-12:
            return x, i, False  # derivative too small → fail

        x_new = x - fx / dfx

        if abs(x_new - x) < tol:
            return x_new, i, True

        x = x_new

    return x, max_iter, False


def find_roots_newton(a, b, c, tol=1e-8):
    """
    Attempts to find up to 2 real roots using multiple initial guesses.
    Returns list of unique real roots (within tolerance).
    """
    guesses = [-100, -10, -1, 0, 1, 10, 100]
    roots = []

    for guess in guesses:
        try:
            root, iters, converged = newton_raphson_quadratic(a, b, c, guess, tol)
            if converged:
                # Round to avoid near-duplicates (e.g., 2.0000001 vs 2.0)
                root_rounded = round(root, 8)
                # Check uniqueness
                if not any(abs(root_rounded - r) < 1e-6 for r in roots):
                    roots.append(root_rounded)
        except Exception:
            continue

    roots.sort()
    return roots