import numpy as np
from scipy.optimize import brentq
from black_scholes import black_scholes_call

def implied_volatility(market_price, S, K, T, r) -> float:
    """
    Calculate implied volatility given a market option price.

    Parameters
    ----------
    market_price : float : observed market price of the call option
    S            : float : current stock price
    K            : float : strike price
    T            : float : time to expiration in years
    r            : float : risk-free interest rate

    Returns
    -------
    float : implied volatility
    """
    # the function we want to find the root of
    # bs_price(sigma) - market price = 0
    def objective(sigma):
        return black_scholes_call(S, K, T, r, sigma) - market_price

    # brentq searches for a root between two bounds
    # volatility must be between 0.1% and 500%
    try:
        iv = brentq(objective, 1e-6, 5.0)
        return iv
    except ValueError:
        return None # no solution found

def plot_vol_smile(S, T, r, market_prices):
    """
    Plot the implied volatility smile.

    Parameters
    ----------
    S             : float : current stock price
    T             : float : time to expiration
    r             : float : risk-free rate
    market_prices : dict  : {strike: market_price}
    """
    import matplotlib.pyplot as plt
    import os

    strikes = sorted(market_prices.keys())
    ivs = []
    for K in strikes:
        iv = implied_volatility(market_prices[K], S, K, T, r)
        ivs.append(iv * 100 if iv else None)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(strikes, ivs, "o-", color="steelblue", linewidth=2, markersize=6)
    ax.axvline(x=S, color="black", linestyle="--", linewidth=1, label=f"Current price (S = ${S})")
    ax.set_title("Implied Volatility Smile", fontsize=13)
    ax.set_xlabel("Strike Price ($)")
    ax.set_ylabel("Implied Volatility (%)")
    ax.legend()
    ax.grid(alpha=0.3)

    os.makedirs("plots", exist_ok=True)
    plt.tight_layout()
    plt.savefig("plots/vol_smile.png", dpi=150)
    plt.show()
    print("Plot saved to plots/vol_smile.png")

if __name__ == "__main__":
    S, K, T, r = 150, 155, 0.5, 0.05

    # test: if market price equals our BS price, IV should return sigma=0.20
    test_price = 7.92
    iv = implied_volatility(test_price, S, K, T, r)
    print(f"Market price: ${test_price}")
    print(f"Implied volatility: {iv:.4f} ({iv*100:.2f}%)")

    # now test with different market prices
    print("\nHow IV changes with market price:")
    for price in [5.00, 7.92, 10.00, 13.00, 16.00]:
        iv = implied_volatility(price, S, K, T, r)
        print(f"  Market price ${price:.2f} -> IV: {iv*100:.2f}%")

    # simulated market prices across strikes showing a volatility smile
    market_prices = {
        120: 31.50,
        125: 27.20,
        130: 23.10,
        135: 19.40,
        140: 15.30,
        145: 11.80,
        150: 9.20,
        155: 7.92,
        160: 6.10,
        165: 5.20,
        170: 4.80,
        175: 4.60,
        180: 4.50,
    }

    plot_vol_smile(S, T, r, market_prices)