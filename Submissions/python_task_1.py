import pandas as pd
import numpy as np

df1=pd.read_csv("dataset-1.csv")
df2=pd.read_csv("dataset-2.csv")

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car_matrix = pd.pivot_table(df, values='car', index='id_1', columns='id_2', fill_value=0)
    np.fill_diagonal(car_matrix.values, 0)
    return car_matrix

    # return df





def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    car_type_counts = {"low": 0, "medium": 0, "high": 0}
    for car in df["car"]:
        if car <= 15:
            car_type_counts["low"] += 1
        elif car <= 25:
            car_type_counts["medium"] += 1
        else:
            car_type_counts["high"] += 1

    return car_type_counts
    # return dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean= df["bus"].mean()
    filtered_df = df[df["bus"] > 2 * bus_mean]
    return sorted(filtered_df.index.to_list())
    # return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    avg_trucks_by_route = df.groupby('route')['truck'].mean()
    filtered_routes = avg_trucks_by_route[avg_trucks_by_route > 7].index.to_list()
    return sorted(filtered_routes)

    # return list()

def modify_value(value):
  try:
    # Convert value to float before comparison
    value = float(value)
    if value > 20:
      return value * 0.75
    else:
      return value * 1.25
  except ValueError:
    # Return the original value if conversion fails
    return value

def multiply_matrix(df)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    return df.applymap(modify_value).round(1)
    # return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    # days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # df['startDay'] = pd.Categorical(df['startDay'], categories=days_order, ordered=True)
    # df['endDay'] = pd.Categorical(df['endDay'], categories=days_order, ordered=True)
    # df['startTime'] = pd.to_timedelta(df['startTime'])
    # df['endTime'] = pd.to_timedelta(df['endTime'])
    # def safe_create_timestamp(day, time):
    #     try:
    #         return pd.to_datetime(day) + pd.to_timedelta(time)
    #     except pd.errors.OutOfBoundsDatetime:
    #         return pd.NaT
    # df['startTimestamp'] = df.apply(lambda x: safe_create_timestamp(x['startDay'], x['startTime']), axis=1)
    # df['endTimestamp'] = df.apply(lambda x: safe_create_timestamp(x['endDay'], x['endTime']), axis=1)
    # df['duration'] = df['endTimestamp'] - df['startTimestamp']
    # completeness_series = (
    #     df.groupby(['id', 'id_2'])['duration']
    #     .apply(lambda x: (x.max() - x.min()) >= pd.Timedelta(days=7, hours=23, minutes=59, seconds=59))
    # )
    # return completeness_series
    # return pd.Series()

car_matrix = generate_car_matrix(df1)
print(car_matrix)

type_count=get_type_count(df1)
print(type_count)

sorted_bus=get_bus_indexes(df1)
print(sorted_bus)

filtered_bus=filter_routes(df1)
print(filtered_bus)

modified_df = multiply_matrix(car_matrix)
print(modified_df)

