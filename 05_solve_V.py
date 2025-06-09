import sympy as sp
import sys

# Optional: Increase recursion limit if you're dealing with heavy symbolic expressions
sys.setrecursionlimit(3000)

def solve_R_d_y(r_value, M_value, V_value):
    # Define symbolic variables
    y, M, r, R, d, V = sp.symbols('y M r R d V')

    # Define the equations
    eq1 = sp.Eq(y + M, 20*y + 800*(1 - sp.sqrt(1 - (r*y/R)**2)))
    eq2 = sp.Eq(y, sp.sqrt(-1 + 2*d**2 - d**4 + 2*R**2 + 2*d**2*R**2 - R**4)/(2*d))
    eq3 = sp.Eq(V, (sp.pi/(12*d)) * (R - d + 1)**2 * (d**2 + 2*d + 3 + 2*d*R + 6*R - 3*R**2))

    # Try solving symbolically
    try:
        symbolic_solutions = sp.solve((eq1, eq2, eq3), (R, d, y), dict=True, simplify=False)
    except Exception as e:
        print("Error during solving:", e)
        return []

    if not symbolic_solutions:
        print("No symbolic solutions found.")
        return []

    # Plug in numeric values and evaluate safely
    substituted_solutions = []
    for sol in symbolic_solutions:
        try:
            substituted = {
                k: v.subs({r: r_value, M: M_value, V: V_value}).doit().evalf()
                for k, v in sol.items()
            }
            # Keep only if all values are real
            if all(val.is_real and not val.has(sp.I) for val in substituted.values()):
                substituted_solutions.append(substituted)
        except Exception as e:
            print("Skipping one solution due to error:", e)
            continue

    return substituted_solutions


# Example usage
if __name__ == "__main__":
    # Change these input values to test different cases
    r_input = 0.4     # radius-like variable
    M_input = 10    # mass-like or offset value
    V_input = 1  # volume-like value

    results = solve_R_d_y(r_input, M_input, V_input)

    if results:
        print("\nReal Solutions Found:")
        for i, res in enumerate(results):
            print(f"\n Solution {i+1}:")
            for var, val in res.items():
                print(f"  {var} = {val}")
    else:
        print("No valid (real) solutions found.")

