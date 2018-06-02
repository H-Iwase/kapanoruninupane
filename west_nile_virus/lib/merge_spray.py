# coding: utf-8
from geopy import distance
from multiprocessing import Pool, cpu_count
import numpy as np
import pandas as pd


def select_date(df, start, end):
    """Return rows which are in the closed range between start and end."""
    return df[(start <= df.Date) & (df.Date <= end)]


def dist_in_km(a, b):
    return distance.distance((a.Latitude, a.Longitude), (b.Latitude, b.Longitude)).km


def find_min_dist(row, spray, offset_days, fill_na_by=np.nan):
    return spray.pipe(
        select_date, row.Date - offset_days, row.Date
    ).apply(
        dist_in_km, args=(row,), axis=1
    ).pipe(
        # at this point, df should not be empty, just in case
        lambda df: fill_na_by if df.empty else df.min()
    )


def select_sprayed(df, spray, offset_days):
    spray_date_index = df.Date != df.Date  # all False
    for spray_date in spray.Date.unique():
        # Select dates between unique spray date and the day offset_days after
        spray_date_index |= (spray_date <= df.Date) & (df.Date <= offset_days.apply(spray_date))

    return df[spray_date_index]


def parallel_apply(df, func, args, n=cpu_count() + 1):
    p = Pool(n)
    splitted = [{'df': spl_df, 'args': args} for spl_df in np.array_split(df, n * 20)]
    result = p.map(func, splitted)
    p.close()
    p.join()
    return pd.concat(result)


def create_min_dist_series(args_dict):
    result_series = args_dict['df'].apply(find_min_dist, args=args_dict['args'], axis=1)
    # if no results, return empty series
    if result_series.shape[0] == 0:
        return pd.Series()

    return result_series


def min_dist(df, spray, days=2):
    """Returns a Series of minimum distances to the spray location within days for each row in df

    Args:
        df (pandas.DataFrame): needs following columns ['Date', 'Latitude', 'Longitude']
        days (int):
    Returns:
        pandas.Series: Series of minimum distances to the spray location within `days` for each row in df
    """

    offset_days = pd.tseries.offsets.Day(days=days)

    return df.pipe(
        select_sprayed, spray, offset_days
    ).pipe(
        parallel_apply, create_min_dist_series, args=(spray, offset_days)
    )


# this may take several minutes
# train_with_spray = raw_train_data.assign(
#     ClosestSprayKmIn2Days=lambda df: min_dist(df, spray_data)
# )
