import market as m
import battery as b
import solar as s


def run_simulation(battery: b.Battery, solar: s.Solar):
    for day in range(365):
        for hour in range(24):
            # can't change these
            prices = m.get_prices(day, hour)
            pred_prod = solar.get_predicted_production(day, hour)
            actual_prod = solar.get_actual_production(day, hour)
            # can change this
            planned = battery.plan_storage(pred_prod, prices)
            # can't change these either
            if planned >= 0:
                actual = min(planned, actual_prod)
            else:
                actual = planned
            # storing is positive, releasing is negative here, so releasing is always possible
            # but for storing, the max we can store is what the solar actually produces
            # we could also not output the planned prod for an hour if we reeeally want that hour's energy
            # but just output a higher number
            battery.apply_storage(actual, prices[0])


if __name__ == "__main__":
    wanted_kwh = 200.0
    num_modules = int(wanted_kwh/4.56)
    price_per_module = 1294.0 # in euros
    battery = b.Battery(4.56, 2.4, 6000, 4.7, int(wanted_kwh/4.56))
    solar = s.Solar(200.0, 0.0)
    run_simulation(battery, solar)
    print(battery.revenue / 100.0, "€ revenue", battery.cycles, "cycles")
    print(battery.revenue / 100.0 / battery.cycles, "€/cycle")
    print(price_per_module * float(num_modules)/battery.revenue*100.0, "years till ROI")
    print(6000 / battery.cycles)
    life_years = 6000 / battery.cycles
    print((life_years * battery.revenue / 100.0) - (price_per_module * num_modules))
    print(price_per_module * num_modules)
