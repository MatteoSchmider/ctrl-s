import json
import matplotlib.pyplot as plt
import numpy as np


def divide_into_chunks(list, length: int):
    """
    Generator to split a list into multiple chunks of equal length

    Args:
        list (_type_): list to split
        length (int): length of the chunks to be generated

    Yields:
        _type_: lists of size length representing chunks from list
    """
    for i in range(0, len(list), length):
        yield list[i:i + length]


def get_prices(year: int) -> [float]:
    """
    gets the prices for a year as a list of floats representing the price in ct/kWh for that hour

    Args:
        year (int): the year to get prices for

    Returns:
        _type_: list of floats representing the prices of that year
    """
    with open("data/prices/" + str(year) + ".txt", "r") as file:
        return json.load(file)


def get_daily_difference(year: int) -> [float]:
    """
    gets a list of floats, each being the maximum price difference for that day of the year

    Args:
        year (int): year to get daily differences for

    Returns:
        [float]: list of daily maximum price differences
    """    
    hours = get_prices(year)
    values = []
    for day in divide_into_chunks(hours, 24):
        diff = max(day) - min(day)
        values.append(diff)
    return values


def get_daily_average(year: int) -> [float]:
    """
    gets a list of floats, each being the average price for that day of the year

    Args:
        year (int): year to get daily average prices for

    Returns:
        [float]: list of daily average prices
    """    
    hours = get_prices(year)
    values = []
    for day in divide_into_chunks(hours, 24):
        avg = sum(day) / 24
        values.append(avg)
    return values


def print_year_stats(year: int):
    """
    prints the statistics of that year:
    year: avg price, avg daily diff, (avg daily diff) / (avg price)

    Args:
        year (int): year to print statistics for
    """    
    prices = get_prices(year)
    daily_diffs = get_daily_difference(year)
    avg_price = sum(prices) / len(prices)
    avg_diff = sum(daily_diffs) / len(daily_diffs)
    print(str(year) + ": " + str(avg_price) + ", " +
          str(avg_diff) + ", " + str(avg_diff / avg_price))


def graph_values_histogram(values, xlabel: str):
    """
    graphs values as a histogram plot with 100 bins

    Args:
        values (_type_): values to plot
        xlabel (str): label on the x axis
    """
    plt.clf()
    # density=False would make absolute counts instead of percentages
    plt.hist(np.array(values), density=True, bins=100)
    plt.xlabel(xlabel)  # "Price"
    plt.ylabel("Percentage")


def graph_values_cumulative(values, xlabel: str):
    """
    graphs values as a cumulative histogram line plot with 100 bins
    this line plot is defined by y(x) = percentage of total data whose value is larger than x
    i.e. y(x) = |{z | z >= x, z in values}| / |values|

    Args:
        values (_type_): values to plot
        xlabel (str): label on the x axis
    """
    plt.clf()
    x, base = np.histogram(np.array(values), bins=100)
    cumulative = (len(values) - np.cumsum(x)) / len(values)
    plt.plot(base[:-1], cumulative)
    plt.xlabel(xlabel)  # "Price"
    plt.ylabel("Percentage")


def graph_values_cumulative_avg(values, xlabel: str):
    """
    graphs values as a cumulative histogram line plot with 100 bins
    this line plot is defined by y(x) = avg of all z with z < x
    i.e. y(x) = avg of {z | z <= x, z in values}

    Args:
        values (_type_): values to plot
        xlabel (str): label on the x axis
    """
    plt.clf()
    x, base = np.histogram(np.array(values), bins=100)
    cumulative = np.cumsum(np.multiply(
        np.array(x), np.array(base[:-1]))) / np.cumsum(np.array(x))
    plt.plot(base[:-1], cumulative)
    plt.xlabel(xlabel)  # "Price"
    plt.ylabel("Percentage")


def graph_values_average_from_top(values, ylabel: str):
    """
    graphs values by graphing at each offset x from bin 0 to 100,
    ordered descendingly by value,
    what the average value up to and including that bin is.
    i.e. y(x) = average value of the top x out of 100 bins of values
    (bins are all of the same size)

    Args:
        values (_type_): values to plot
        ylabel (str): label on the y axis
    """
    plt.clf()
    x, base = np.histogram(np.array(values), bins=100)
    prices = []
    amounts = []
    for offset in range(0, 100):
        cumulative = np.cumsum(np.multiply(np.array(x[offset:]), np.array(
            base[offset:-1]))) / np.cumsum(np.array(x[offset:]))
        prices.append(cumulative[-1])
        amounts.append(np.cumsum(np.array(x[offset:]))[-1])
    plt.plot(amounts, prices)
    plt.xlabel("Top x days")
    plt.ylabel(ylabel)  # "Price"


def graph_prices_hist(year: int):
    """
    generates a histogram plot of all prices of that year

    Args:
        year (int): year to generate histogram for
    """
    graph_values_histogram(get_prices(year), "Price")
    plt.savefig("results/price-analysis/" + str(year) + "_prices_hist.png")


def graph_daily_diff(year: int):
    """
    generates multiple grpahs for analysis of daily max price differences for that year

    Args:
        year (int): year to generate graphs for
    """
    values = get_daily_difference(year)
    graph_values_histogram(values, "Price Difference")
    plt.savefig("results/price-analysis/" +
                str(year) + "_daily_diff_histogram.png")
    graph_values_cumulative(values, "Price Difference")
    plt.savefig("results/price-analysis/" +
                str(year) + "_daily_diff_cumulative.png")
    graph_values_cumulative_avg(values, "Price Difference")
    plt.savefig("results/price-analysis/" + str(year) +
                "_daily_diff_cumulative_avg.png")
    graph_values_average_from_top(values, "Total Price")
    plt.savefig("results/price-analysis/" + str(year) +
                "_daily_diff_average_from_top.png")


if __name__ == "__main__":
    print("averages for every year, format:")
    print("year: avg price, avg daily diff, (avg daily diff) / (avg price)")
    all_years_daily_diffs = []
    all_years_daily_avgs = []
    for year in range(2015, 2024):
        graph_daily_diff(year)
        graph_prices_hist(year)
        print_year_stats(year)
        all_years_daily_diffs += get_daily_difference(year)
        all_years_daily_avgs += get_daily_average(year)
    print("statistical correlation between daily diff and daily avg price for all years:")
    print(np.corrcoef(np.array(all_years_daily_diffs),
          np.array(all_years_daily_avgs)))
# averages for every year, format:
# year: price in ct/kWh, diff in ct/kWh, diff / price
# 2015: 3.16521872146118,   2.914175342465753,  0.9206868778788416
# 2016: 2.899361872146114,  2.365753424657535,  0.8159565894085513
# 2017: 3.418852739726039,  3.056783561643837,  0.8940962932170002
# 2018: 4.446892009132414,  3.2381753424657553, 0.7281884371861599
# 2019: 3.766660045662096,  3.023509589041095,  0.802703071789859
# 2020: 3.0426247716894954, 3.2617863013698636, 1.0720304165402141
# 2021: 9.694463926940635,  8.08699726027397,   0.8341871527109856
# 2022: 23.548153995433815, 18.80894246575342,  0.7987438195537805
# 2023: 8.079530637254912,  5.734129411764704,  0.7097107083577967
# correlation: price/diff: 0.81529518
