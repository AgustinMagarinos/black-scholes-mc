import numpy as np
from black_scholes import black_scholes_call


# n = num of simulations
def monte_carlo_call(S, K, T, r, sigma, n=100000):
    """
    Price a European call option using Monte Carlo simulation.

    Parameters
    ----------
    S : float : current stock price
    K : float : strike price
    T : float : time to expiration in years
    r : float : risk-free interest rate (annualized)
    sigma : float : volatility (annualized)
    n : int : number of simulated price paths

    Returns
    -------
    float : estimated call option price
    """
    # Step 1: simulate n random draws from a standard normal
    Z = np.random.standard_normal(n)

    # Step 2: simulate final stock price for each path using geometric brownian motion
    S_T = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)

    # Step 3: calculate payoff for each path
    payoff = np.maximum(S_T - K, 0)

    # Step 4: discount average payoff back to today
    price = np.exp(-r * T) * np.mean(payoff)

    return price

if __name__ == "__main__":
    S = 150
    K = 155
    T = 0.5
    r = 0.05
    sigma = 0.20

    mc_price = monte_carlo_call(S, K, T, r, sigma)
    bs_price = black_scholes_call(S, K, T, r, sigma)

    print(f"Monte Carlo price: ${mc_price:.2f}")
    print(f"Black-Scholes price: ${bs_price:.2f}")
    print(f"Difference: ${abs(mc_price - bs_price):.4f}")