import json


class Solar:

    def __init__(self, peak, sinus_params) -> None:
        self.peak = peak
        self.params = sinus_params
        self.data = json.load(open("data/production/production_2022.txt", "r"))

    def get_predicted_production(self, day: int, hour: int) -> [float]:
        """
        computes the predicted solar production for the next 24 hours from a given day and hour

        Args:
            day (int): day to compute from
            hour (int): hour to compute from

        Returns:
            [float]: array of 24 hourly production values in kWh
        """
        ret = [hour]
        for i in range(23):
            ret.append(0.0)
        return ret

    def get_actual_production(self, day: int, hour: int) -> float:
        """
        gets the actually produced energy for a given hour in a given day from the production data

        Args:
            day (int): day to get production for
            hour (int): hour in that day to get prodcution for

        Returns:
            float: the energy produced in that hour od that day in kWh
        """        
        return self.data[day * 24 + hour]
 