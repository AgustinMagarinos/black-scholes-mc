import numpy as np
from scipy.stats import norm

def greeks(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes Greeks for a European call and put.

    Parameters
    ----------
    S     : float : current stock price
    K     : float : strike price
    T     : float : time to expiration in years
    r     : float : risk-free interest rate
    sigma : float : volatility

    Returns
    -------
    dict of Greek values
    """

    d1 = (np.log(S/K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    delta_call = norm.cdf(d1)
    delta_put = -norm.cdf(-d1)

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))

    vega = S * norm.pdf(d1) * np.sqrt(T) / 100 # per 1% move in vol

    theta_call = (
        -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        - (r * K * np.exp(-r * T) * norm.cdf(d2))
    ) / 365


    theta_put = (
        -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        + (r * K * np.exp(-r * T) * norm.cdf(-d2))
    ) / 365

    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2) / 100 # per 1% move in r
    rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

    return {
        "delta_call": delta_call,
        "delta_put":  delta_put,
        "gamma":      gamma,
        "vega":       vega,
        "theta_call": theta_call,
        "theta_put":  theta_put,
        "rho_call":   rho_call,
        "rho_put":    rho_put,
    }

if __name__ == "__main__":
    S, K, T, r, sigma = 150, 155, 0.5, 0.05, 0.20

    g = greeks(S, K, T, r, sigma)

    print(f"Delta  (call): {g['delta_call']:.4f}")
    print(f"Delta  (put):  {g['delta_put']:.4f}")
    print(f"Gamma:         {g['gamma']:.4f}")
    print(f"Vega:          {g['vega']:.4f}")
    print(f"Theta  (call): {g['theta_call']:.4f}")
    print(f"Theta  (put):  {g['theta_put']:.4f}")
    print(f"Rho    (call): {g['rho_call']:.4f}")
    print(f"Rho    (put):  {g['rho_put']:.4f}")