import pandas as pd
import numpy as np
import json
from os.path import basename, exists
from streamlit_dimensions import st_dimensions


def fig_scale(n): return np.log10(st_dimensions(key="main")["width"] // 200) * n


def read_json(path):
    lines = []
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            try:
                lines.append(json.loads(line))
            except json.decoder.JSONDecodeError:
                print(line)
            line = f.readline()

    return pd.DataFrame(lines)


def show_data_range(series):
    ts_start = series.min()
    ts_end = series.max()

    if series.is_unique:
        print('All entries are unique!')

    print('Start timestamp:\t', ts_start)
    print('End timestamp:  \t', ts_end)
    print('The total range:\t', ts_end - ts_start)


def parse_datetime(series, ts_format=None):
    if ts_format is None:
        return pd.to_datetime(series).dt.tz_localize(None).round('min')
    else:
        return pd.to_datetime(series, ts_format).dt.tz_localize(None).round('min')


def convert_to_mmol(series): return series * .0555


def build_basal_series(data):
    ts_series = data.index
    basal = data['basal']
    times = data['duration'].astype(int)

    zipped = zip(ts_series, basal, times)
    delta = pd.Timedelta('1min')

    ts_series, values = [], []
    for ts, basal, times in zipped:
        for t in range(times):
            ts_series.append(ts + delta * t)
            values.append(basal)
    df = pd.DataFrame({'basal': values}, index=ts_series)
    df.index.name = 'timestamp'
    return df


def process_entries(path):
    # read the data
    df = read_json(path)
    # set timestamp df as index
    df = df.set_index(parse_datetime(df['dateString'])).sort_index()
    df.index.name = 'timestamp'
    # convert mg/dL to mmol/L
    df['glucose'] = convert_to_mmol(df['sgv'])
    # filter out calibration records and resample the resulting series
    df = df.loc[df['type'] == 'sgv', ['glucose']].resample('5min').max()
    return df


def process_treatments(path):
    # variables
    cols_mapping = {'insulin': 'bolus', 'amount': 'basal', 'eventType': 'event_type'}
    cols_to_use = ['basal', 'duration', 'bolus', 'rate', 'glucose', 'carbs', 'cal']
    events_to_keep = ['Temp Basal', 'Correction Bolus', 'Meal Bolus', 'BG Check']

    # read the data
    df = read_json(path)
    # set timestamp as index
    df = df.set_index(parse_datetime(df["created_at"])).sort_index()
    df.index.name = 'timestamp'
    # rename data fields and take a subset
    df.rename(cols_mapping, axis=1, inplace=True)
    # df['cal'] = 1 if df['event_type'] == 'BG Check' else 0
    df['cal'] = np.where(df['event_type'] == 'BG Check', 1, 0)
    df['basal'] *= df['rate']
    # convert duration to continuous data series
    tmp_basal = df.loc[df['event_type'] == 'Temp Basal', ['basal', 'duration']].copy()
    tmp_basal = build_basal_series(tmp_basal)
    df = df.loc[df['event_type'].isin(events_to_keep), cols_to_use]
    df = tmp_basal.combine_first(df).resample('5min').max()
    return df


# download modsim.py
def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve
        local, _ = urlretrieve(url, filename)
        print('Downloaded ' + local)


