from scipy.optimize import brentq
from black_scholes import black_scholes_call

def implied_volatility(market_price, S, K, T, r) -> float:
    """
    Calculate implied volatility given a market option price.

    Parameters
    ----------
    market_price : float : observed market price of the call option
    S : float : current stock price
    K : float : strike price
    T : float : time to expiration in years
    r : float : risk-free interest rate

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
        print(f"Market price ${price:.2f} -> IV: {iv*100:.2f}%")