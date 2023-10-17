import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as md
from matplotlib.ticker import AutoMinorLocator
from numpy import array, log
from streamlit_dimensions import st_dimensions


class GlucoseGraph:
    def __init__(self, df, date, range_lower, range_upper):
        self.date = date
        self.df = df.loc[self.date.strftime("%F")]
        self.range_lower = range_lower
        self.range_upper = range_upper
        self.time_formatter = md.DateFormatter("%H:%M")

    @staticmethod
    def scale_fig(scale_factor):
        return st_dimensions("main")["width"] / (300 * scale_factor)

    @property
    def bg_data(self):
        data = self.df["glucose"]
        mask = (data > self.range_lower) & (data < self.range_upper)

        within_range = data[mask].resample("5min").max()
        outside_range = data[~mask].resample("5min").max()

        return dict(
            data=data,
            max=data.max(),
            min=data.min(),
            index_max=data.index.max(),
            index_min=data.index.min(),
            within_range=within_range,
            outside_range=outside_range,
        )

    def annotate_calibrations(self, ax):
        cals = self.df.loc[self.df["cal"] == 1, "glucose"]
        for i in range(len(cals)):
            ax.annotate(
                "Sensor\ncalibration",
                xy=(cals.index[i], cals[i] + .2),
                xytext=(cals.index[i], cals[i] + 2),
                arrowprops=dict(facecolor="black", headwidth=4, width=1, headlength=4),
            )

    def annotate_carbs_intakes(self, ax):
        df = self.df.dropna(subset="carbs")
        ax.scatter(df.index, df.glucose, marker="o", s=log(df.carbs) * 30, c="green", label="Carbs intake")
        for i in range(len(df)):
            ax.annotate(
                f"{int(df.carbs[i])} g",
                xy=(df.index[i] + pd.Timedelta("20min"), df.glucose[i]),
            )

    def plot(self, scale_factor=1, figure_shape=(5, 2)):

        fig, ax = plt.subplots(figsize=(array(figure_shape) * self.scale_fig(scale_factor)))

        ax.plot(self.bg_data["within_range"], label="Within")
        ax.plot(self.bg_data["outside_range"], label="Outside")
        ax.hlines(
            [self.range_lower, self.range_upper], self.bg_data["index_min"], self.bg_data["index_max"],
            linestyles="dashed", colors="grey", alpha=.5, label="Threshold"
        )

        self.annotate_calibrations(ax)
        self.annotate_carbs_intakes(ax)

        # axes and legend settings
        ax.xaxis.set_major_formatter(self.time_formatter)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.set(
            title=f"Glucose monitor data for {self.date.strftime('%B %d, %Y')}",
            ylim=[(self.bg_data["min"] - 2).round(), (self.bg_data["max"] + 2).round()],
            ylabel="Blood glucose, $mmol/L$",
        )
        ax.legend(title="BG target range", loc="upper left")
        ax.grid(alpha=.2)

        return fig


class GlucoseInsulinGraph(GlucoseGraph):
    def __init__(self, df, date, range_lower, range_upper):
        super().__init__(df, date, range_lower, range_upper)

    def plot(self, scale_factor=1, figure_shape=(5, 3)):
        fig, axs = plt.subplots(
            2, 1, sharex=True, gridspec_kw=dict(height_ratios=[2, 1]),
            figsize=(array(figure_shape) * self.scale_fig(scale_factor))
        )

        # glucose plot
        axs[0].plot(self.bg_data["within_range"], label="Within")
        axs[0].plot(self.bg_data["outside_range"], label="Outside")
        axs[0].hlines(
            [self.range_lower, self.range_upper], self.bg_data["index_min"], self.bg_data["index_max"],
            linestyles="dashed", colors="grey", alpha=.5, label="Threshold"
        )

        self.annotate_calibrations(axs[0])
        self.annotate_carbs_intakes(axs[0])

        # axes and legend settings
        axs[0].xaxis.set_major_formatter(self.time_formatter)
        axs[0].xaxis.set_minor_locator(AutoMinorLocator())
        axs[0].set(
            title=f"Glucose monitor data for {self.date.strftime('%B %d, %Y')}",
            ylim=[(self.bg_data["min"] - 2).round(), (self.bg_data["max"] + 2).round()],
            ylabel="Blood glucose, $mmol/L$",
        )
        axs[0].legend(title="BG target range", loc="upper left")
        axs[0].grid(alpha=.2)

        bolus = self.df["bolus"].dropna()

        # insulin plot
        axs[1].plot(self.df["basal"], drawstyle="steps-post", label="Temporary basal")
        axs[1].fill_between(self.df.index, self.df["basal"], step="post", alpha=.2)
        axs[1].vlines(
            bolus.index,  0, bolus, color="purple", label="Correction bolus"
        )
        axs[1].set(
            xlabel=f"{self.date.strftime('%B %d, %Y')}",
            ylabel="Insulin dosage, $U$",
            yticks=range(int(bolus.max()))
        )

        axs[1].legend(title="Insulin treatment type", loc="upper left")
        axs[1].grid(alpha=.2)

        fig.subplots_adjust(wspace=0, hspace=0)

        return fig
