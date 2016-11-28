import pandas as pd
import numpy as np
import datetime


def simple_csv(file, headers=None, remove_rows=0, year=(0, '1-4'), month=(1, 'all'), day=(2, 'all'), hour=(3, 'all'),
               minute=None, second=None):
    with open(file, 'r') as f:
        data = [line.rstrip() for line in f.readlines()]
    data = [line.split(',') for line in data]
    if headers is not None:
        ## TODO: implement header extraction
        pass
    data = data[remove_rows:]

    if year[1] != 'all':
        years = [int(x[year[0]][int(year[1].split('-')[0]) - 1:int(year[1].split('-')[1])]) for x in data]
    else:
        years = [int(x[year[0]]) for x in data]

    if month[1] != 'all':
        months = [int(x[month[0]][int(month[1].split('-')[0]) - 1:int(month[1].split('-')[1])]) for x in data]
    else:
        months = [int(x[month[0]]) for x in data]

    if day[1] != 'all':
        days = [int(x[day[0]][int(day[1].split('-')[0]) - 1:int(day[1].split('-')[1])]) for x in data]
    else:
        days = [int(x[day[0]]) for x in data]

    if hour[1] != 'all':
        hours = [int(x[hour[0]][int(hour[1].split('-')[0]) - 1:int(hour[1].split('-')[1])]) for x in data]
    else:
        hours = [int(x[hour[0]]) for x in data]

    if minute is None:
        minutes = None
    else:
        if minute[1] != 'all':
            minutes = [int(x[minute[0]][int(minute[1].split('-')[0]) - 1:int(minute[1].split('-')[1])]) for x in data]
        else:
            minutes = [int(x[minute[0]]) for x in data]

    if second is None:
        seconds = None
    else:
        if second[1] != 'all':
            seconds = [int(x[second[0]][int(second[1].split('-')[0]) - 1:int(second[1].split('-')[1])]) for x in data]
        else:
            seconds = [int(x[second[0]]) for x in data]

    if minutes is None:
        dates = [
            datetime.datetime(
                year=years[i],
                month=months[i],
                day=days[i],
                hour=hours[i])
            for i in range(len(data))
            ]
    else:
        if seconds is None:
            dates = [
                datetime.datetime(
                    year=years[i],
                    month=months[i],
                    day=days[i],
                    hour=hours[i],
                    minute=minutes[i])
                for i in range(len(data))
                ]
        else:
            dates = [
                datetime.datetime(
                    year=years[i],
                    month=months[i],
                    day=days[i],
                    hour=hours[i],
                    minute=minutes[i],
                    second=seconds[i])
                for i in range(len(data))
                ]

    frame = pd.DataFrame(data=data, index=dates)
    if minutes is None:
        del_cols = np.unique([year[0], month[0], day[0], hour[0]])
    else:
        if seconds is None:
            del_cols = np.unique([year[0], month[0], day[0], hour[0], minute[0]])
        else:
            del_cols = np.unique([year[0], month[0], day[0], hour[0], minute[0], second[0]])
    del_cols = [frame.columns[i] for i in del_cols]
    for column in del_cols:
        del frame[column]

    frame.index.names = ['Date-time [UTC]']
    frame.columns.names = ['Data classes']
    return frame

data = simple_csv(file=r'.\test_data\EVA_stress\rqh0822a.csv')
data.to_csv(r'.\test_data\EVA_stress\parsed.csv')

data2 = pd.read_csv(r'.\test_data\EVA_stress\parsed.csv', index_col=0)
data2.index = pd.to_datetime(data2.index)
