import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import fetch_data
import numpy as np

def data_filter(data):
    df = data.filter(["Close"])
    dataset = df.values
    return dataset

def scaler(series):
    data_normalizer = MinMaxScaler(feature_range=(0, 1))
    normalized_data = data_normalizer.fit_transform(series)
    return normalized_data, data_normalizer
    

def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    xs = []
    ys = []
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(window_size, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(window_size))
    dataset = dataset.map(lambda window: (window[:-1], window[-1:]))
    #dataset = dataset.shuffle(buffer_size=10)
    for x, y in dataset:
        xs.append(x.numpy())
        ys.append(y.numpy())
    return xs, ys
