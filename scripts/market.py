import json

ALL_HOURS = json.load(open("data/prices/2022.txt", "r"))


def get_prices(day: int, hour: int) -> [float]:
    """
    gets the next 24 hours of day ahead prices

    Args:
        day (int): day to get the prices from
        hour (int): hour of that day to get the next 24hrs from

    Returns:
        [float]: the 24 next hourly prices
    """
    idx = 24 * day + hour
    ret = []
    for price in ALL_HOURS[idx:idx + 24]:
        ret.append(float(price))
    return ret
