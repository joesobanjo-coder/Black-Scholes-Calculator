import math

from scipy.stats import norm

S = 100  # Spot price
K = 100  # Strike price
T = 1  # Time to maturity in years
r = 0.05  # Risk-free interest rate
sigma = 0.2  # Annualized volatility


def find_d1_d2(S, K, T, r, sigma):
    if S <= 0 or K <= 0:
        raise ValueError(
            "Spot price (S) and Strike price (K) must be strictly positive."
        )
    if T <= 0:
        raise ValueError("Time to maturity (T) must be greater than zero.")
    if sigma <= 0:
        raise ValueError("Volatility (sigma) must be strictly positive.")
    numerator_d1 = math.log(S / K) + (r + ((sigma**2) / 2)) * T
    denominator_d1 = sigma * math.sqrt(T)
    d1 = numerator_d1 / denominator_d1
    d2 = d1 - sigma * math.sqrt(T)
    return (d1, d2)


def call_option_price(S, K, T, r, sigma):
    d1, d2 = find_d1_d2(S, K, T, r, sigma)
    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return call_price


def put_option_price(S, K, T, r, sigma):
    d1, d2 = find_d1_d2(S, K, T, r, sigma)
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price


def verify_put_call_parity(S, K, T, r, sigma):
    c = call_option_price(S, K, T, r, sigma)
    p = put_option_price(S, K, T, r, sigma)

    lhs = c - p
    rhs = S - (K * math.exp(-r * T))

    # Assert that both sides match to 6 decimal places
    assert math.isclose(lhs, rhs, rel_tol=1e-5), (
        f"Parity violation: LHS={lhs}, RHS={rhs}"
    )
    print(f"Put-Call Parity holds: C - P = {lhs:.4f}, S - Ke^(-rT) = {rhs:.4f}")


print(f"Call Option Price: {call_option_price(S, K, T, r, sigma)}")
print(f"Put Option Price: {put_option_price(S, K, T, r, sigma)}")
