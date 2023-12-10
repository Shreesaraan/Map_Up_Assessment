import pandas as pd
import numpy as np
import networkx as nx

df=pd.read_csv("dataset-3.csv")

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    G = nx.Graph()
    for index, row in df.iterrows():
        G.add_edge(row['id_start'], row['id_end'], distance=row['distance'])
    distance_matrix = dict(nx.all_pairs_dijkstra_path_length(G))
    distance_df = pd.DataFrame(distance_matrix).fillna(0)
    distance_df = (distance_df + distance_df.T) / 2
    return distance_df

    # return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    upper_triangular = df.where(~np.tril(np.ones(df.shape)).astype(bool))
    unrolled_distances = upper_triangular.stack().reset_index()
    unrolled_distances.columns = ["id_start", "id_end", "distance"]
    unrolled_distances = unrolled_distances.append(unrolled_distances.rename(columns={"id_start": "id_end", "id_end": "id_start"}))
    return unrolled_distances
    # return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_avg_distance = df[df["id_start"] == reference_id]["distance"].mean()
    threshold_range = (reference_avg_distance * 0.9, reference_avg_distance * 1.1)
    filtered_df = df[(df["id_start"] == reference_id) & (df["distance"].between(*threshold_range))]
    id_list = sorted(filtered_df["id_end"].tolist())
    return id_list
    # return df


def calculate_toll_rate(df,rate_coefficients)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    vehicle_types = ["moto", "car", "rv", "bus", "truck"]
    for vehicle_type, coefficient in rate_coefficients.items():
        df[vehicle_type] = df["distance"] * coefficient
    df = df[["id_start", "id_end", "distance"] + vehicle_types]
    return df
    # return df


def calculate_time_based_toll_rates(df,time_rate_coefficients)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here


    return df

distance_df=calculate_distance_matrix(df)
print(distance_df)

unroll=unroll_distance_matrix(distance_df)
print(unroll)

# reference_id=int(input())
ten_percent=find_ids_within_ten_percentage_threshold(unroll, 1001470)
print(ten_percent)

rate_coefficients = {
  "moto": 0.8,
  "car": 1.2,
  "rv": 1.5,
  "bus": 2.2,
  "truck": 3.6
}
toll_rate=calculate_toll_rate(unroll,rate_coefficients)
print(toll_rate)

time_rate_coefficients = {
  "00:00:00": 0.8,
  "10:00:00": 1.2,
  "18:00:00": 0.8,
  "weekend": 0.7
}
time_based=calculate_time_based_toll_rates(df, time_rate_coefficients)
cleaned_time_toll_rate = time_based.dropna(subset=['id_start'])
print(time_based)

