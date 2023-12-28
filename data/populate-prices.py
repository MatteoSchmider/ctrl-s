import requests
import json

START = 1546297200000  # = 01.01.2019 , 00:00
# day = 24 hours * 60 minutes * 60 seconds * 1000 milliseconds milliseconds
DAY = 24 * 60 * 60 * 1000
# current day in 2023 in milliseconds since start
YEAR_2023 = (8 * 30 + 30) * DAY
YEAR = 365 * DAY  # how long a year is in milliseconds


def get_prices(year: int) -> [float]:
    """
    function to get a list of hourly prices from the awattar api for a full year

    Args:
        year (int): the year to get the price list for

    Returns:
        [float]: a python list of floats, each entry being the price for that hour
    """
    start = START + ((year - 2019) *
                     YEAR)  # calculate start time relative to 2019
    if year != 2023:
        end = start + YEAR  # calulate end as one year later
    else:
        # as 2023 is not done yet, calculate end to some day until which data is available
        end = start + YEAR_2023
    response = requests.get(
        "https://api.awattar.de/v1/marketdata?start=" + str(start) + "&end=" + str(end))
    hours = response.json()["data"]
    values = []
    for i in range(len(hours)):
        # market price is in € / MWh => this converts to ct/kWh
        values.append(float(hours[i]["marketprice"]) / 10.0)
    return values


if __name__ == "__main__":
    for year in range(2015, 2024):
        with open("data/prices/" + str(year) + ".txt", "w") as file:
            json.dump(get_prices(year), file)
