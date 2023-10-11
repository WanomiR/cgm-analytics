import numpy as np


class Dataset:

    def __init__(self, dataframe, date,
                 marker_size_carbs=12,
                 marker_size_bolus=10, ):

        self.df = dataframe.loc[date]
        self.marker_size_carbs = marker_size_carbs
        self.marker_size_bolus = marker_size_bolus

    @property
    def glucose(self):
        """ Continuous glucose monitoring data """
        glucose_series = self.df.loc[:, "glucose"]
        timestamps = glucose_series.index
        glucose_values = glucose_series.to_numpy()
        glucose_max = max([np.nanmax(glucose_values) + 2.5, 20])
        return dict(ts=timestamps, values=glucose_values, max=glucose_max)

    @property
    def food(self):
        """ Carbohydrates intake data """
        food_df = self.df.dropna(subset="carbs")
        timestamps = food_df.index
        carbs_intake = food_df["carbs"].to_numpy().astype(np.int8)
        glucose_values = food_df["glucose"].to_numpy()
        marker_size = np.log(carbs_intake) * self.marker_size_carbs
        return dict(
            n=len(food_df),
            ts=timestamps,
            carbs=carbs_intake,
            glucose=glucose_values,
            marker=marker_size
        )

    @property
    def cals(self):
        """ Sensor calibration points """
        cal_df = self.df.loc[self.df["cal"] == 1, "glucose"]
        timestamps = cal_df.index
        glucose_values = cal_df.to_numpy()
        return dict(n=len(cal_df), ts=timestamps, glucose=glucose_values)

    @property
    def basal(self):
        """ Temp basal insulin treatments data """
        basal_df = self.df.dropna(subset="basal").loc[:, "basal"]
        timestamps = basal_df.index
        basal_values = basal_df.to_numpy()
        basal_max = max([np.max(basal_values), 1.5])
        return dict(ts=timestamps, values=basal_values, max=basal_max)

    @property
    def bolus(self):
        """ Bolus insulin treatments data """
        bolus_df = self.df.loc[:, "bolus"].dropna()
        timestamps = bolus_df.index
        bolus_values = bolus_df.to_numpy()
        marker_size = np.clip(
            np.log2(bolus_values * self.marker_size_bolus) * 5, 0, 40
        )
        return dict(ts=timestamps, values=bolus_values, marker=marker_size)
