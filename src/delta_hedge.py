import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes_call
from greeks import greeks
import os

def delta_hedge_simulation(S0, K, T, r, sigma, n_steps=52, n_sims=5):
    """
        Simulate a delta hedging strategy over the life of an option.

        We sold a call option and hedge by holding delta shares of stock,
        rebalancing at each time step.

        Parameters
        ----------
        S0     : float : initial stock price
        K      : float : strike price
        T      : float : time to expiration in years
        r      : float : risk-free rate
        sigma  : float : volatility
        n_steps: int   : number of rebalancing steps (52 = weekly)
        n_sims : int   : number of paths to simulate

        Returns
        -------
        dict with simulation results
        """
    dt = T / n_steps
    time = np.linspace(0, T, n_steps + 1)

    all_paths = []
    all_pnls = []

    for sim in range(n_sims):
        # simulate stock price path
        Z = np.random.standard_normal(n_steps)
        S = np.zeros(n_steps + 1)
        S[0] = S0

        for t in range(1, n_steps + 1):
            S[t] = S[t-1] * np.exp(
                (r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z[t-1]
            )

        # delta hedge
        cash = np.zeros(n_steps + 1) # cash account
        delta_pos = np.zeros(n_steps + 1) # shares held
        pnl = np.zeros(n_steps + 1) # hedging pnl

        # at t=0 sell the position, collect premium, buy delta shares
        option_price = black_scholes_call(S[0], K, T, r, sigma)
        d = greeks(S[0], K, T, r, sigma)["delta_call"]

        delta_pos[0] = d
        cash[0] = option_price - d * S[0] # premium recieved - cost of shares

        for t in range(1, n_steps + 1):
            time_remaining = T - t * dt

            # rebalance: calculate new delta
            if time_remaining > 1e-6:
                new_delta = greeks(S[t], K, time_remaining, r, sigma)["delta_call"]
            else:
                new_delta = 1.0 if S[t] > K else 0.0

            # update cash: grow at risk free rate, adjust for rebalancing
            cash[t] = cash[t-1] * np.exp(r * dt) - (new_delta - delta_pos[t-1]) * S[t]
            delta_pos[t] = new_delta

        # pnl at expiration: cash + shares - option payoff
        final_payoff = max(S[-1] - K, 0)
        final_pnl = cash[-1] + delta_pos[-1] * S[-1] - final_payoff

        all_paths.append(S)
        all_pnls.append(final_pnl)

    return {
        "time": time,
        "paths": all_paths,
        "pnls": all_pnls,
    }

def plot_delta_hedge(S0, K, T, r, sigma, n_steps=52, n_sims=200):
    results = delta_hedge_simulation(S0, K, T, r, sigma, n_steps=n_steps, n_sims=n_sims)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # left: sample stock paths
    for path in results["paths"][:20]:
        axes[0].plot(results["time"], path, alpha=0.4, linewidth=0.8)
    axes[0].axhline(y=K, color="black", linestyle="--", linewidth=1.5, label=f"Strike (K = ${K})")
    axes[0].set_title("Sample Stock Price Paths", fontsize=12)
    axes[0].set_xlabel("Time (years)")
    axes[0].set_ylabel("Stock Price ($)")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # right: pnl distribution
    axes[1].hist(results["pnls"], bins=40, color="steelblue", edgecolor="white", linewidth=0.5)
    axes[1].axvline(x=0, color="black", linestyle="--", linewidth=1.5, label="Zero PnL")
    axes[1].axvline(x=np.mean(results["pnls"]), color="coral", linestyle="-",
                    linewidth=2, label=f"Mean PnL: ${np.mean(results['pnls']):.2f}")
    axes[1].set_title("Delta Hedging PnL Distribution", fontsize=12)
    axes[1].set_xlabel("PnL at Expiration ($)")
    axes[1].set_ylabel("Frequency")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.suptitle(f"Delta Hedging Simulation  |  {n_steps} rebalancing steps  |  {n_sims} paths",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()

    os.makedirs("plots", exist_ok=True)
    plt.savefig("plots/delta_hedge.png", dpi=150, bbox_inches="tight")
    plt.show()
    print(f"\nPnL summary across {n_sims} simulations:")
    print(f"  Mean PnL:   ${np.mean(results['pnls']):.4f}")
    print(f"  Std PnL:    ${np.std(results['pnls']):.4f}")
    print(f"  Min PnL:    ${np.min(results['pnls']):.4f}")
    print(f"  Max PnL:    ${np.max(results['pnls']):.4f}")


if __name__ == "__main__":
    plot_delta_hedge(S0=150, K=155, T=0.5, r=0.05, sigma=0.20, n_steps=52, n_sims=200)