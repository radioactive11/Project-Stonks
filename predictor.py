import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import fetch_data
import pandas_datareader as web
import os
import numpy as np
import pandas as pd
import window_maker
import datetime as dt


def split(Xs, ys):
    training_length = int(0.9 * len(Xs))
    print("Training Length: " + str(training_length))
    x_train = np.array(Xs[:training_length])
    y_train = np.array(ys[:training_length])
    y_train = np.reshape(y_train, y_train.shape[0])
    x_test = np.array(Xs[training_length:])
    y_test = np.array(ys[training_length:])
    y_test = np.reshape(y_test, y_test.shape[0])
    
    return x_train, x_test, y_train, y_test


def predictor (x_train, x_test, y_train, y_test, normalizer_cache):
    checkpt_dir = os.getcwd() + "\\chkpt"
    tf.keras.backend.clear_session()

    model = tf.keras.models.Sequential([
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(60, return_sequences=True,input_shape=(x_train.shape[1],1))),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(60, return_sequences=False)),
    tf.keras.layers.Dense(25),
    tf.keras.layers.Dense(1)
    ])

    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpt_dir,
                                                 save_weights_only=True,
                                                 verbose=1)
    
    model.compile(optimizer='adam',loss='mean_squared_error', metrics=["mae"])
    history = model.fit(x_train, y_train, epochs=45, callbacks=[cp_callback])
    predictions = model.predict(x_test)
    predictions = normalizer_cache.inverse_transform(predictions)
    y_test = y_test.reshape(-1,1)
    y_test = normalizer_cache.inverse_transform(y_test)
    rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
    print("Root Mean Square Error is " + str(rmse))
    return model

def next_day(stock_name, normalizer_cache, model):
    #os.chdir("..")
    os.chdir("data")
    ticker_file = stock_name + str(".NS.csv")
    quote = pd.read_csv(ticker_file)
    quote_close = quote.filter(["Close"]).values
    quote_series = quote_close[-60 : ]
    transformed = normalizer_cache.fit_transform(quote_series)
    transformed = np.reshape(transformed, (1, 60, 1))
    trial = model.predict(transformed)
    trial = normalizer_cache.inverse_transform(trial)
    print("Closing Price for next day will be: "+ str(trial[-1,0]))
    
