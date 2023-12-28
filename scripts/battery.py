class Battery:
    def __init__(self, max_capacity, max_power, max_cycles, relative_cost, num_modules) -> None:
        self.max_capacity = max_capacity * num_modules
        self.max_power = max_power * num_modules
        self.max_cycles = max_cycles
        self.relative_cost = relative_cost
        self.charge = 0.5 * self.max_capacity
        self.cycles = 0
        self.revenue = 0
        self.is_charging = True  # needed to count when a charge/discharge cycle starts

    def plan_storage(self, expected_production_24: [float], prices_24: [float]) -> float:
        """
        this function calls one of the implemented online algorithms that
        calculates the next hour's requested battery charge delta
        (although we will only know what the actual production in that hour will be when it happens)

        Args:
            expected_production_24 ([float]): the expected production for the next 24 hours, so the algorithm has some information to go off of
            prices_24 ([float]): the day ahead prices for the next 24 hours, i.e. so we don't waste cycle life on days with high expected wind power

        Returns:
            float: the energy the algorithm would like to save in the next hour, does not have to bee one of the expected production values
        """
        return self.plan_storage_1(expected_production_24, prices_24)

    def plan_storage_1(self, expected_production_24: [float], prices_24: [float]) -> float:
        remaining_hours_this_day = expected_production_24[0] % 25

        next_hour = prices_24[0]
        minimum = min(prices_24[:remaining_hours_this_day], default=0.0)
        maximum = max(prices_24[:remaining_hours_this_day], default=0.0)
        delta = maximum - minimum
        if delta > self.relative_cost:
            if next_hour is minimum:
                return self.max_power
            elif next_hour is maximum:
                return -self.max_power
        return 0
        # if there is a delta in the next 24 hours, that is large enough:
        #   if the next hour is the low point: charge
        #   if the next hour is the high point: discharge
        #   else: do nothing

    def apply_storage(self, actual_energy: float, price: float) -> None:
        """
        runs a simulation step of one hour, dis-/charging the battery by actual_energy at price
        and updating all the internal variables

        Args:
            actual_energy (float): the energy in kWh to charge/discharge
            price (float): the price in cents per kWh to simulate this step with
        """
        new_charge = self.charge + actual_energy
        new_charge = min(new_charge, self.max_capacity)
        new_charge = max(new_charge, 0)
        delta = new_charge - self.charge
        self.charge = new_charge
        if delta >= 0: # the new charge is larger than the previous, we are charging delta kWh
            self.is_charging = True
            self.revenue -= abs(delta) * price
        else:
            if self.is_charging:
                self.cycles += 1
            self.is_charging = False
            self.revenue += abs(delta) * price
        # actual_energy = min of plan_storage output and actual_production for that hour
        # apply that charge, revenue and cycle to the battery
