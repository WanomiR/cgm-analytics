from matplotlib import pyplot as plt
from matplotlib import dates as md
from matplotlib.ticker import AutoMinorLocator
from numpy import array
from streamlit_dimensions import st_dimensions


class GlucosePlot:
    def __init__(self, df, date, range_lower, range_upper):
        self.df = df
        self.date = date
        self.range_lower = range_lower
        self.range_upper = range_upper

    @staticmethod
    def scale_fig(scale_factor):
        return st_dimensions("main")["width"] / (300 * scale_factor)

    def plot(self, scale_factor=1):
        # data preprocessing
        data = self.df.loc[self.date.strftime("%F"), "glucose"]
        mask = (data > self.range_lower) & (data < self.range_upper)

        in_range = data[mask].resample("5min").max()
        out_of_range = data[~mask].resample("5min").max()

        # variables
        fig_shape = 5, 2
        formatter = md.DateFormatter("%H:%M")  # xticks formatter
        ylim_upper = (data.max() + 2).round()  # yaxis range
        ylim_lower = (data.min() - 2).round()

        # figure
        fig, ax = plt.subplots(figsize=(array(fig_shape) * self.scale_fig(scale_factor)))

        ax.plot(in_range, label="Within")
        ax.plot(out_of_range, label="Outside")
        ax.hlines(
            [self.range_lower, self.range_upper], data.index.min(), data.index.max(),
            linestyles="dashed", colors="grey", alpha=.5, label="Threshold"
        )

        # axes and legend settings
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.set(
            title="Continuous blood glucose monitor data",
            xlabel=f"{self.date.strftime('%B %d, %Y')}",
            ylim=[ylim_lower, ylim_upper],
            ylabel="Blood glucose, $mmol/L$",
        )
        ax.legend(title="BG target range")
        ax.grid(alpha=.2)

        return fig