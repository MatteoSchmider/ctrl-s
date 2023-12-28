import matplotlib.pyplot as plt
import json
from scipy import optimize
import numpy as np
from evaluate_prices import divide_into_chunks


def get_production():
    with open("data/production/production_2022.txt", "r") as file:
        hours = json.load(file)
    values = []
    for day in divide_into_chunks(hours, 24):
        values.append(sum(day))
    return values


def solar_func(x, amplitude, frequency, phase, offset):
    return amplitude * np.sin(frequency * x + phase) + offset


def fit_sinus(data: [float]):
    xs = np.array([float(i) for i in range(0, len(data)*3)])
    params, _ = optimize.curve_fit(
        solar_func, xs, data + data + data, p0=[100, 6/len(data), 10, 300])
    for i in range(1000):
        params, _ = optimize.curve_fit(
            solar_func, xs, data + data + data, p0=params)
    return params


def plot_prod():
    plt.clf()
    data = get_production()
    params = fit_sinus(data)
    xs = np.array([float(i) for i in range(0, len(data))])
    plt.plot(data)
    plt.plot(xs, solar_func(xs, params[0], params[1], params[2], params[3]))
    plt.savefig("results/production_2022.png")


if __name__ == "__main__":
    plot_prod()
    fit_sinus(get_production())
