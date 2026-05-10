import numpy as np
import matplotlib.pyplot as plt
from greeks import greeks
import os


def plot_greeks(K, T, r, sigma):
    """
    Plot Delta, Gamma and Vega as a function of stock price.
    """
    # range of stock prices around the strike price
    stock_prices = np.linspace(K * 0.5, K * 1.5, 200)

    deltas, gammas, vegas = [], [], []

    for S in stock_prices:
        g = greeks(S, K, T, r, sigma)
        deltas.append(g["delta_call"])
        gammas.append(g["gamma"])
        vegas.append(g["vega"])

    fig, axes = plt.subplots(3, 1, figsize=(10, 12))

    # delta
    axes[0].plot(stock_prices, deltas, color="steelblue", linewidth=2)
    axes[0].axvline(x=K, color="black", linestyle="--", linewidth=1, label=f"Strike (K = ${K})")
    axes[0].set_title("Delta vs Stock Price", fontsize=12)
    axes[0].set_ylabel("Delta")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # gamma
    axes[1].plot(stock_prices, gammas, color="coral", linewidth=2)
    axes[1].axvline(x=K, color="black", linestyle="--", linewidth=1, label=f"Strike (K = ${K})")
    axes[1].set_title("Gamma vs Stock Price", fontsize=12)
    axes[1].set_ylabel("Gamma")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    # vega
    axes[2].plot(stock_prices, vegas, color="seagreen", linewidth=2)
    axes[2].axvline(x=K, color="black", linestyle="--", linewidth=1, label=f"Strike (K = ${K})")
    axes[2].set_title("Vega vs Stock Price", fontsize=12)
    axes[2].set_ylabel("Vega")
    axes[2].set_xlabel("Stock Price ($)")
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    plt.suptitle("Option Greeks vs Stock Price", fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()

    os.makedirs("plots", exist_ok=True)
    plt.savefig(f"plots/greeks.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Plots saved to plots/greeks.png")

if __name__ == "__main__":
    plot_greeks(K=155, T=0.5, r=0.05, sigma=0.20)