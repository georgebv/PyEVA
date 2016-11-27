import pandas as pd
import numpy as np
import datetime


def simple_csv(file, year=0, month=1, day=2, hour=3, minute=None, second=None):
    with open(file, 'r') as f:
        data = [line for line in f.readlines()]
    data = [line.split(',') for line in data]
    for i in range(len(data)):
        data[i][-1] = data[i][-1][:-1]
    years = [int(x[year]) for x in data]
    months = [int(x[month]) for x in data]
    days = [int(x[day]) for x in data]
    hours = [int(x[hour]) for x in data]
    dates = [datetime.datetime(year=years[i], month=months[i], day=days[i], hour=hours[i]) for i in range(len(data))]
    frame = pd.DataFrame(data=data, index=dates)
    del frame[year], frame[month], frame[day], frame[hour]
    frame.index.names = ['Date-time [UTC]']
    frame.columns.names = ['Data classes']

    frame.columns = ['Water level [mm]']
    return frame

data = simple_csv(file=r'.\test_data\EVA_stress\rqh0822a.csv', year=0, month=1, day=2, hour=3)
data.to_csv(r'.\test_data\EVA_stress\parsed.csv')

data2 = pd.read_csv(r'.\test_data\EVA_stress\parsed.csv', index_col=0)
data2.index = pd.to_datetime(data2.index)
