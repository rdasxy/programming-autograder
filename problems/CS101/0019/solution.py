def pay(hours, rate):
    return rate * min(hours, 40) + 1.5 * rate * max(hours-40, 0)
