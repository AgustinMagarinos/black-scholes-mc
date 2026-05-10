import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes price for a European call option.

    Parameters
    ----------
    S     : float : current stock price
    K     : float : strike price
    T     : float : time to expiration in years
    r     : float : risk-free interest rate (annualized)
    sigma : float : volatility (annualized)

    Returns
    -------
    float : call option price
    """

    d1 = (np.log(S/K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    return call_price

def black_scholes_put(C, S, K, T, r, sigma):
    """
    Calculate the Black-Scholes price for a European put option.

    Parameters
    ----------
    S     : float : current stock price
    K     : float : strike price
    T     : float : time to expiration in years
    r     : float : risk-free interest rate (annualized)
    sigma : float : volatility (annualized)

    Returns
    -------
    float : put option price
    """

    d1 = (np.log(S/K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    put_price = C - S + K * np.exp(-r * T)
    return put_price

if __name__ == '__main__':
    # Example:
    S = 150  # current price
    K = 155  # strike price
    T = 0.5  # 6 months
    r = 0.05 # 5% risk-free rate
    sigma = 0.2 # 20% volatility

    call_price = black_scholes_call(S, K, T, r, sigma)
    put_price = black_scholes_put(call_price, S, K, T, r, sigma)
    print(f"Call option price: ${call_price:.2f}\nPut option price: ${put_price:.2f}")