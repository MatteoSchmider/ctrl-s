import csv
import json


if __name__ == "__main__":
    # site has capacity of 200kWp
    # csv contains list of all quarterly hour average power values in kW

    # first 15min of 2022 are not in the csv, but it is night, so init the production list with 0.0 as first value
    quarterly = [0.0]
    # 1.) read the quarter-hourly average power
    with open("data/production/BEG Buchtzig.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for i, row in enumerate(reader):
            if i > 0:
                # first csv row are the row titles
                # switch from DE decimal , to international decimal ".", convert the string to float value, append to list
                quarterly.append(float(row[3].replace(",", ".")))
    # last element is the first 15min of 2023 => pop it from list
    quarterly.pop()
    assert (len(quarterly) == 365 * 24 * 4)
    # 2.) compute the hourly generated energy in kWh
    hourly = []
    for i in range(len(quarterly)):
        # every fourth element => every 0-15min of a full hour
        if i % 4 == 0:
            # compute the energy produced in that hour in kWh, append it to the list
            hourly.append(quarterly[i] * 0.25 + quarterly[i+1] *
                          0.25 + quarterly[i+2] * 0.25 + quarterly[i+3] * 0.25)

    assert (len(hourly) == 365 * 24)
    # save hourly values into txt
    with open("data/production/production_2022.txt", "w") as file:
        json.dump(hourly, file)
