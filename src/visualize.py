import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes_call

def simulate_paths(S, T, r, sigma, n_paths=200, n_steps=252):
    """
    Simulate GBM price paths.

    Parameters
    ----------
    S : float : current stock price
    T : float : time to expiration in years
    r : float : risk-free interest rate
    sigma : float : volatility
    n_paths : int   : number of paths to simulate
    n_steps : int   : number of time steps (252 = trading days in a year)

    Returns
    -------
    paths : np.ndarray of shape (n_steps + 1, n_paths)
    time : np.ndarray of time points
    """
    dt = T / n_steps
    time = np.linspace(0, T, n_steps + 1)

    # matrix of random shocks, each column is one path
    Z = np.random.standard_normal((n_steps, n_paths))

    # build paths step by step
    paths = np.zeros((n_steps + 1, n_paths))
    paths[0] = S

    for t in range(1, n_steps + 1):
        paths[t] = paths[t-1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z[t-1])

    return paths, time

def plot_paths(S, K, T, r, sigma, n_paths=200):
    paths, time = simulate_paths(S, T, r, sigma, n_paths)

    fig, ax = plt.subplots(figsize=(12, 6))

    # color paths by whether they finish in the money or not
    for i in range(n_paths):
        final_price = paths[-1, i]
        color = "steelblue" if final_price > K else "salmon"
        ax.plot(time, paths[:, i], color=color, alpha=0.3, linewidth=0.8)

    # strike price line
    ax.axhline(y=K, color="black", linestyle="--", linewidth=1.5, label=f"Strike (K= ${K})")

    # starting price dot
    ax.plot(0, S, "ko", markersize=6, label=f"Current price (S = ${S})")

    # labels
    bs_price = black_scholes_call(S, T, r, sigma, n_paths)
    ax.set_title(f"Simulated GBM Price Paths\nBS Call Price: ${bs_price:.2f}  |  Blue = in the money at expiry, Red = out of the money", fontsize=13)
    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Stock price ($)")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("plots/pricing_paths.png", dpi=150)
    plt.show()
    print("Plot saved to plots/pricing_paths.png")

if __name__ == "__main__":
    import os
    os.makedirs("plots", exist_ok=True)

    S = 150
    K = 155
    T = 0.5
    r = 0.05
    sigma = 0.20

    plot_paths(S, K, T, r, sigma)
