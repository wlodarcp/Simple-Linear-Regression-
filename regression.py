#! /usr/bin/env python
# -*- coding: utf-8 -*-

from io import BytesIO
from zipfile import ZipFile
import urllib.request
import os.path
import numpy as np
from sklearn import linear_model
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from random import choices

def dealWithDirtyValuesForActiveWind(data):
    i = int(0)
    index = list()
    while i < len(data[:,0]):
    #czemu tak - wiatraki pracuja w przedziale pr wiatru od 2 do 25 wiec wnioskuje ze dane z poza tego zakresu sa bledne
    #dodatkowo zakres 50 i 1600 dla mocy, 50 poniewaz zauwazylem duza ilosc niskich wartosci mocy dla duzych pr wiatru - cos nie tak
    #1600 aby wyeliminowac jakies odstajace dane typu 30000, i tak wiekszosc danych nie wykracza poza 1400(zapewne max?)
        if data[i,1] > 2 and data[i,1]<=25 and data[i,0] > 50 and data[i,0]<=1600:
            index.append(i)
        i+=1
    data2 = data[index,:]
    return data2
def dealWithDirtyValuesForReActiveWind(data):
    i = int(0)
    index = list()
    while i < len(data[:,0]):
        if data[i,1] > 0 and data[i,1]<=25 and abs(data[i,0]) > 5:
            index.append(i)
        i+=1
    data2 = data[index,:]
    return data2
ur = 'https://s3.eu-central-1.amazonaws.com/windally-test/dataset.csv.zip'
filename = 'dataset.csv'

#sprawdza czy istnieje plik filename i jak nie to pobiera zipa i go rozpakowuje
if not os.path.exists(filename):
    url = urllib.request.urlopen(ur)
    with ZipFile(BytesIO(url.read())) as my_zip_file:
        my_zip_file.extractall()
else:
    print('File exist')

# czyta dane do dataframe    
df = pd.read_csv(filename, infer_datetime_format = True, encoding = "ISO-8859-1", engine='python')
size1 = len(df[['WINDSPEED']]) #ilosc danych przed czyszczeniem
#ladujemy do macierzy
active_wind_matrix = np.array(df[['ACTIVE POWER', 'WINDSPEED']].as_matrix())
reactive_wind_matrix = np.array(df[['REACTIVE POWER', 'WINDSPEED']].as_matrix())
#sprawdzenie zakresow
#plt.boxplot(active_wind_matrix[1:10000, 0]) #nie dla całoego zbioru poniewaz danych bylo za dużo jak na możliwosci mojego sprzetu ;)
#plt.show()
#plt.boxplot(active_wind_matrix[1:10000, 1])
#plt.show()
#plt.boxplot(reactive_wind_matrix[1:10000, 0])
#plt.show()
#plt.boxplot(reactive_wind_matrix[1:10000, 1])
#plt.show()

active_wind_matrix = dealWithDirtyValuesForActiveWind(active_wind_matrix)
reactive_wind_matrix = dealWithDirtyValuesForReActiveWind(reactive_wind_matrix)
#nowy rozmiar po czyszczeniu
size = len(active_wind_matrix[:,0])
re_size = len(reactive_wind_matrix[:,0])
#do zbioru uczacego biore losowe 40% danych (z 1 połowy pomiarów)
items = range(1,(int)(size*0.5))
re_items = range(1,(int)(re_size*0.5))
train_index = choices(items, k=(int)(0.4*size))
re_train_index = choices(re_items, k=(int)(0.4*re_size))

#pozostałe dane na testowe, jest ich duzo więc żeby było cos widac na wykresach dziele je na kilka mniejszych zbiorow i dla kazdego testuje oddzielnie
items = range((int)(size*0.5), (int)(size*0.6))
test_index = list()
re_items = range((int)(re_size*0.5), (int)(re_size*0.6))
re_test_index = list()
tmp = 0.6
#selekcja danych do zbioróW testowych
while tmp<1:
    test_index.append(choices(items, k=(int)(0.01*size)))
    items = range((int)(size*tmp), (int)(size*(tmp+0.1)))
    re_test_index.append(choices(re_items, k=(int)(0.05*re_size)))
    re_items = range((int)(re_size*tmp), (int)(re_size*(tmp+0.1)))
    tmp +=0.1

#zbiory treningowe 
active_power_matrix = np.array(active_wind_matrix[:,0]).reshape(size,1)
active_power_train = active_power_matrix[train_index]
re_active_power_matrix = np.array(reactive_wind_matrix[:,0]).reshape(re_size,1)
re_active_power_train = re_active_power_matrix[re_train_index]
#cd zbiory treningowe
windspeed_matrix = np.array(active_wind_matrix[:,1]).reshape(size,1)
windspeed_matrix_train = windspeed_matrix[train_index]
re_windspeed_matrix = np.array(reactive_wind_matrix[:,1]).reshape(re_size,1)
re_windspeed_matrix_train = re_windspeed_matrix[re_train_index]

active_power_test = list()
windspeed_matrix_test = list()
re_active_power_test = list()
re_windspeed_matrix_test = list()
#zbiory testowe
for i in test_index:
    active_power_test.append(active_power_matrix[i])
    windspeed_matrix_test.append(windspeed_matrix[i])
for i in re_test_index:
    re_active_power_test.append(re_active_power_matrix[i])
    re_windspeed_matrix_test.append(re_windspeed_matrix[i])
#tworzy obiekt do regresji liniowej
regr = linear_model.LinearRegression()

regr.fit(windspeed_matrix_train, active_power_train)


k=int(0)
fig, axes = plt.subplots(nrows=5, figsize=(10,30))
while k < len(windspeed_matrix_test):
    active_power_predict = regr.predict(windspeed_matrix_test[k])

    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(active_power_test[k], active_power_predict))
    # Explained variance score: 1 is perfect prediction
    print('Coefficient of determination: %.2f' % r2_score(active_power_test[k], active_power_predict))

    # Plot outputs
    axes[k].scatter(windspeed_matrix_test[k],active_power_test[k],  color='black', marker = '.', label = "Test values")
    axes[k].plot(windspeed_matrix_test[k],active_power_predict, color='blue', linewidth=3,  label = "Predict line")
    axes[k].legend(loc = 'upper right')
    axes[k].set_ylabel('Active Power [MW]', size = 15)
    axes[k].set_xlabel('Wind Speed [m/s]', size = 15)
    axes[k].set_xticks(range(25))
    textstr = 'Mean squared error: %.2f \nVariance score: %.2f' % (mean_squared_error(active_power_test[k], active_power_predict) , r2_score(active_power_test[k], active_power_predict))
    axes[k].text(s = textstr, x = 0, y = 1400)
    k+=1
plt.savefig("Active Power Prediction.png")
plt.show()

re_regr = linear_model.LinearRegression()

re_regr.fit(re_windspeed_matrix_train, re_active_power_train)

# Make predictions using the testing set
re_active_power_predict = list()
k=int(0)
fig, axes = plt.subplots(nrows=5, figsize=(10,30))
while k < len(re_windspeed_matrix_test):
    re_active_power_predict = re_regr.predict(re_windspeed_matrix_test[k])

    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(re_active_power_test[k], re_active_power_predict))
    # Explained variance score: 1 is perfect prediction
    print('Coefficient of determination: %.2f' % r2_score(re_active_power_test[k], re_active_power_predict))

    # Plot outputs
    axes[k].scatter(re_windspeed_matrix_test[k],re_active_power_test[k],  color='black', marker = '.', label = "Test values")
    axes[k].plot(re_windspeed_matrix_test[k],re_active_power_predict, color='blue', linewidth=3,  label = "Predict line")
    axes[k].legend(loc = 'upper right')
    axes[k].set_ylabel('Reactive Active Power [VAR]', size = 15)
    axes[k].set_xlabel('Wind Speed [m/s]', size = 15)
    axes[k].set_xticks(range(25))
    textstr = 'Mean squared error: %.2f \nVariance score: %.2f' % (mean_squared_error(re_active_power_test[k], re_active_power_predict) , r2_score(re_active_power_test[k], re_active_power_predict))
    axes[k].text(s = textstr, x = 0, y = 300)
    k+=1
plt.savefig("Reactive Power Prediction.png")
plt.show()
