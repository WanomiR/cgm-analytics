from matplotlib import pyplot as plt
from matplotlib import dates as md
plt.style.use("dark_background")


def plot_glucose(df, date, range_lower, range_upper, fig_scale):

    # preprocessing
    data = df.loc[date, "glucose"]
    mask = (data > range_lower) & (data < range_upper)

    # xticks formatter
    formatter = md.DateFormatter("%H:%M")

    ylim_upper = (data.max() + 1).round()
    ylim_lower = (data.min() - 1).round()

    fig, ax = plt.subplots(figsize=(5*fig_scale, 2*fig_scale))

    in_range = data[mask].resample("5min").max()
    out_of_range = data[~mask].resample("5min").max()

    ax.plot(in_range)
    ax.plot(out_of_range)
    ax.xaxis.set_major_formatter(formatter)
    ax.set(ylim=[ylim_lower, ylim_upper])
    ax.legend(["Within target", "Outside target"])

    return fig