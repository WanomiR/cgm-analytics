from matplotlib import pyplot as plt
from matplotlib import dates as md
from matplotlib.ticker import AutoMinorLocator
from numpy import array


# plt.style.use("dark_background")


def plot_glucose(df, date, range_lower, range_upper, fig_scale):
    """
    Plots glucose line graph for selected day.
    :param df: pandas dataframe
    :param date: selected date, datetime object
    :param range_lower: low glucose threshold
    :param range_upper: high glucose threshold
    :param fig_scale: figure scaling factor
    :return: matplotlib figure
    """

    # data preprocessing
    data = df.loc[date.strftime("%F"), "glucose"]
    mask = (data > range_lower) & (data < range_upper)

    in_range = data[mask].resample("5min").max()
    out_of_range = data[~mask].resample("5min").max()

    # variables
    fig_shape = 5, 2
    formatter = md.DateFormatter("%H:%M")  # xticks formatter
    ylim_upper = (data.max() + 2).round()  # yaxis range
    ylim_lower = (data.min() - 2).round()

    # figure
    fig, ax = plt.subplots(figsize=(array(fig_shape) * fig_scale))

    ax.plot(in_range, label="Within")
    ax.plot(out_of_range, label="Outside")
    ax.hlines(
        [range_lower, range_upper], data.index.min(), data.index.max(),
        linestyles="dashed", colors="grey", alpha=.5, label="Threshold"
    )

    # axes and legend settings
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.set(
        title="Continuous blood glucose monitor data",
        xlabel=f"{date.strftime('%B %d, %Y')}",
        ylim=[ylim_lower, ylim_upper],
        ylabel="Blood glucose, $mmol/L$",
    )
    ax.legend(title="BG target range")
    ax.grid(alpha=.2)

    return fig
