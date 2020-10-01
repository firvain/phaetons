from math import sqrt, floor
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from colorama import Fore, init
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from dotenv import load_dotenv
import os

init(autoreset=True)
load_dotenv()

TRAIN_PERC = os.getenv("TRAIN_PERC")


# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    """Transform a time series dataset into a supervised learning dataset

    Args:
        data (object): Sequence of observations as a list or 2D NumPy array.
        n_in (int, optional): Number of lag observations as input.
        Defaults to 1.
        n_out (int, optional): Number of observations as output (y).
        Defaults to 1.
        dropnan (bool, optional): Boolean whether or not to drop rows with NaN
        values. Defaults to True.

    Returns:
        [DataFrame]: Pandas DataFrame of series framed for supervised learning.
    """

    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [("var%d(t-%d)" % (j + 1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [("var%d(t)" % (j + 1)) for j in range(n_vars)]
        else:
            names += [("var%d(t+%d)" % (j + 1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


def LSTM_Prepare(fname):
    """Prepare data for LSTM model

    Args:
        fname (string): Raw data csv path

    Returns:
        [tuple]: Train data, Test Data and Data Scaler
    """
    # load dataset
    dataset = read_csv(fname, header=0, index_col=0)
    # print(dataset.head())
    numOfVars = len(dataset.columns)
    values = dataset.values
    # integer encode direction
    encoder = LabelEncoder()
    values[:, 1] = encoder.fit_transform(values[:, 1])

    # ensure all data is float
    values = values.astype("float32")
    # normalize features
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    # frame as supervised learning
    reframed = series_to_supervised(scaled, 1, 1)
    # drop columns we don't want to predict
    # print([x for x in range(numOfVars + 1, len(reframed.columns))])

    reframed.drop(
        reframed.columns[
            [x for x in range(numOfVars + 1, len(reframed.columns))]
        ],
        axis=1,
        inplace=True,
    )
    # print(reframed.head())
    # split into train and test sets
    values = reframed.values
    # n_train_hours = 365 * 24
    n_train_hours = floor(len(values) * float(TRAIN_PERC))
    # n_train_hours = 0
    # train = values[:n_train_hours, :]
    # test = values[n_train_hours:, :]
    train = values[:n_train_hours, :]
    test = values[n_train_hours:, :]
    # split into input and outputs
    train_X, train_y = train[:, :-1], train[:, -1]
    test_X, test_y = test[:, :-1], test[:, -1]
    # print(train_X.shape)
    # print(test_X.shape)
    # print(test_X[:, 1:])
    # quit()
    # reshape input to be 3D [samples, timesteps, features]
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    # print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
    return train_X, train_y, test_X, test_y, scaler


def LSTM_Exec(train_X, train_y, test_X, test_y, visualize):
    """Execute LSTM model

    Args:
        train_X (ndarray): Input Data
        train_y (ndarray): Target Data
        test_X (ndarray): Validation Data
        test_y (ndarray): Validation Data
        visualize (boolean): Wheather to plot input and output data.

    Returns:
        Sequential: Returns Sequential model
    """
    # design network
    model = Sequential()
    model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dense(1))
    model.compile(loss="mae", optimizer="adam")
    # fit network
    history = model.fit(
        train_X,
        train_y,
        epochs=3,
        batch_size=72,
        validation_data=(test_X, test_y),
        verbose=2,
        shuffle=False,
    )
    if visualize is True:
        # plot history
        pyplot.plot(history.history["loss"], label="train")
        pyplot.plot(history.history["val_loss"], label="test")
        pyplot.legend()
        pyplot.show()
    return model


def LST_Predict(train_X, train_y, test_X, test_y, model, scaler):
    """[summary]

    Args:
        train_X (ndarray): [description]
        train_y (ndarray): [description]
        test_X (ndarray): [description]
        test_y (ndarray): [description]
        model (Sequential): Keras Sequential model
        scaler ([type]): [description]

    Returns:
        [type]: [description]
    """
    # make a prediction
    yhat = model.predict(test_X)

    test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
    # invert scaling for forecast
    inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
    inv_yhat = scaler.inverse_transform(inv_yhat)
    inv_yhat = inv_yhat[:, 0]
    # invert scaling for actual
    test_y = test_y.reshape((len(test_y), 1))
    inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
    inv_y = scaler.inverse_transform(inv_y)
    inv_y = inv_y[:, 0]
    return inv_y, inv_yhat


def LSTM_Eval(inv_y, inv_yhat):
    """Evaluate LSTM model

    Args:
        inv_y (array): Actual
        inv_yhat (array): Forecast
    """
    # calculate RMSE
    rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
    print("Test RMSE: %.3f" % rmse)


def LSTM_RUN(fname, forecastHours=24, visualize=False):
    """ Run LSTM forecast model

    Args:
        fname (string): Path of CSV data
        visualize (bool, optional): Wheater to visualize data.
        Defaults to False.
    """
    print(
        Fore.MAGENTA
        + "Running WIND TURBINE NEURAL NETWORK PREDICTION (PW)"
        + Fore.WHITE
    )
    train_X, train_y, test_X, test_y, scaler = LSTM_Prepare(fname)
    model = LSTM_Exec(train_X, train_y, test_X, test_y, visualize)
    inv_y, inv_yhat = LST_Predict(
        train_X, train_y, test_X, test_y, model, scaler
    )
    LSTM_Eval(inv_y, inv_yhat)
    if visualize is True:
        pyplot.plot(inv_y[-forecastHours:], label="actual")
        pyplot.plot(inv_yhat[-forecastHours+1:], label="predicted")
        pyplot.legend()
        pyplot.show()
    return inv_yhat[-forecastHours:]
