#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
from io import BytesIO
from os import path
from zipfile import ZipFile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_predict, cross_validate, \
    train_test_split


# function to download and extract zip file

def loadData(URL):
    URL = urllib.request.urlopen(URL)
    with ZipFile(BytesIO(URL.read())) as my_zip_file:
        names = my_zip_file.namelist()
        names = [names for names in names if names.endswith('.csv')
                 and '/' not in names]
        if not path.exists(names[0]):
            my_zip_file.extractall()
        else:
            print ('exists')
        return names[0]


# function to produce plots

def makeSomePlots(
    X_test,
    Y_test,
    predict,
    plotNum,
    yAxName,
    divideLenOfDataBy,
    ):
    howMAnyPointOnPlot = int(len(predict) / divideLenOfDataBy)
    (fig, axes) = plt.subplots(nrows=plotNum, figsize=(2 * plotNum, 6
                               * plotNum))
    for i in range(plotNum):
        plotHelper = howMAnyPointOnPlot * (i + 1)
        if plotHelper >= len(predict):
            break
        axes[i].scatter(X_test[plotHelper
                        - howMAnyPointOnPlot:plotHelper],
                        Y_test[plotHelper
                        - howMAnyPointOnPlot:plotHelper], color='black'
                        , marker='.', label='Test values')
        axes[i].plot(X_test[plotHelper
                     - howMAnyPointOnPlot:plotHelper],
                     predict[plotHelper
                     - howMAnyPointOnPlot:plotHelper], color='blue',
                     linewidth=3, label='Predict line')
        axes[i].legend(loc='upper right')
        axes[i].set_ylabel(yAxName, size=15)
        axes[i].set_xlabel('Wind Speed [m/s]', size=15)
    yAxName = yAxName + '.png'
    plt.savefig(yAxName)
    plt.show()


# function to produce predictions

def producePredictionFromSplitDataByLR(
    X_train,
    X_test,
    Y_train,
    Y_test,
    ):
    regr = linear_model.LinearRegression()
    regr.fit(X_train, Y_train)
    predict = regr.predict(X_test)
    mean_sq_err = mean_squared_error(Y_test, predict)
    coef = r2_score(Y_test, predict)
    return (predict, mean_sq_err, coef)


def main():
    URL = \
        'https://s3.eu-central-1.amazonaws.com/windally-test/dataset.csv.zip'
    FILENAME = loadData(URL)
    df = pd.read_csv(FILENAME, infer_datetime_format=True,
                     encoding='ISO-8859-1', engine='python')
    
    df = df[df['WINDSPEED'] >= 0]
    df = df[df['ACTIVE POWER'] >= 0]
    active_wind_matrix = np.array(df[['ACTIVE POWER', 'WINDSPEED'
                                  ]].as_matrix())
    reactive_wind_matrix = np.array(df[['REACTIVE POWER', 'WINDSPEED'
                                    ]].as_matrix())
    size = len(active_wind_matrix[:, 0])

    wind = np.array(active_wind_matrix[:, 1]).reshape(size, 1)
    activepower = np.array(active_wind_matrix[:, 0]).reshape(size, 1)
    reactivepower = np.array(reactive_wind_matrix[:, 0]).reshape(size,
            1)

    # simple linear regresion for activepower - test size 20%, number of generate plots 5, plot are generated for pieces of test data
    # to be more clear

    (X_train, X_test, Y_train, Y_test) = train_test_split(wind,
            activepower, test_size=0.2, random_state=0)
    (predict, error1, coef1) = \
        producePredictionFromSplitDataByLR(X_train, X_test, Y_train,
            Y_test)
    makeSomePlots(
        X_test,
        Y_test,
        predict,
        5,
        'Active Power[MW] (Simple LR)',
        20,
        )
    print ('Active power Mean squared error: %.2f' % error1)
    print ('Active power Coefficient of determination: %.2f' % coef1)

    # simple lr for reactive power similary like up

    (X_train, X_test, Y_train, Y_test) = train_test_split(wind,
            reactivepower, test_size=0.2, random_state=0)
    (predict, error2, coef2) = \
        producePredictionFromSplitDataByLR(X_train, X_test, Y_train,
            Y_test)
    makeSomePlots(
        X_test,
        Y_test,
        predict,
        5,
        'Reactive Power [MVAR] (Simple LR)',
        20,
        )
    print ('Reactive power Mean squared error: %.2f' % error2)
    print ('Reactive power Coefficient of determination: %.2f' % coef2)

    # prediction for active power using cross validation

    lr = linear_model.LinearRegression()
    cv_results = cross_validate(lr, wind, activepower, cv=10)
    predict2 = cross_val_predict(lr, wind, activepower, cv=10)
    error11 = mean_squared_error(activepower, predict2)
    coef11 = r2_score(activepower, predict2)
    makeSomePlots(
        wind,
        activepower,
        predict2,
        4,
        'Active Power[MW] (Cross Val)',
        20,
        )
    print ('Active power Mean squared error: %.2f' % error11)
    print ('Active power Coefficient of determination: %.2f' % coef11)

    # prediction for reactive power using cross validation

    cv_results2 = cross_validate(lr, wind, reactivepower, cv=10)
    predict2 = cross_val_predict(lr, wind, reactivepower, cv=10)
    error21 = mean_squared_error(activepower, predict2)
    coef21 = r2_score(reactivepower, predict2)
    makeSomePlots(
        wind,
        reactivepower,
        predict2,
        4,
        'Reactive Power [MVAR] (Cross Val)',
        20,
        )
    print ('Reactive power Mean squared error: %.2f' % error21)
    print ('Reactive power Coefficient of determination: %.2f' % coef21)

    # comparison of results

    print ('Active power Difference between errors in simple method and CV method: %.2f' \
        % abs(error1 - error11))
    print ('Rective power Difference between errors in simple method and CV method: %.2f' \
        % abs(error2 - error21))
    print ('Active power Difference between coefs in simple method and CV method: %.2f' \
        % abs(coef1 - coef11))
    print ('Rective power Difference between coefs in simple method and CV method: %.2f' \
        % abs(coef2 - coef21))

    # # check results for active power only for wind between 7 and 15 m/s

    df = df[df['WINDSPEED'] >= 7]
    df = df[df['WINDSPEED'] <= 15]
    active_wind_matrix = np.array(df[['ACTIVE POWER', 'WINDSPEED'
                                  ]].as_matrix())
    size = len(active_wind_matrix[:, 0])
    wind = np.array(active_wind_matrix[:, 1]).reshape(size, 1)
    activepower = np.array(active_wind_matrix[:, 0]).reshape(size, 1)

    (X_train, X_test, Y_train, Y_test) = train_test_split(wind,
            activepower, test_size=0.2, random_state=0)
    (predict3, error3, coef3) = \
        producePredictionFromSplitDataByLR(X_train, X_test, Y_train,
            Y_test)
    makeSomePlots(
        X_test,
        Y_test,
        predict3,
        5,
        'Active Power[MW] speed 7-15 ms',
        5,
        )
    print ('Active power Mean squared error: %.2f' % error3)
    print ('Active power Coefficient of determination: %.2f' % coef3)


if __name__ == '__main__':
    main()