import fetch_data
import predictor
import window_maker

def main(ticker):
    data = fetch_data.yahoo_fetcher(ticker)
    series = window_maker.data_filter(data)
    series, normalizer_cache = window_maker.scaler(series)
    Xs, ys = window_maker.windowed_dataset(series, 61, 1, 1)
    x_train, x_test, y_trian, y_test = predictor.split(Xs, ys)
    model = predictor.predictor(x_train, x_test, y_trian, y_test, normalizer_cache)
    predictor.next_day(ticker, normalizer_cache, model)

ticker = input("Enter stock ticker ")
main(ticker.upper())