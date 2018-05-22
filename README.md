# Simple-Linear-Regression-
## Regresja Liniowa - podsumowanie

## Cel
Celem zadania było przeprowadzenie krótkiej analizy zbioru danych której rezultatem miały być modele regresji liniowej
dla mocy czynnej i biernej od prędkości wiatru.

## Realizacja

###### Moc czynna:

Analizę rozpocząłem od pobrania danych i przeprowadzenia "czyszczenia"

Założyłem, że analizując moc czynną mogę ograniczyć się do danych z zakresu prędkości od 2 do 25 m/s (zakres pracy turbiny)
Dziwne wydały mi się również wartości mocy czynnej bliskie 0 występujące dla relatywnie dużych prędkości wiatru - również takie
przypadki postanowiłem odfiltrować.

Jako że zbiór danych był duży - 790 620 wierszy (przed filtracją) postanowiłem wykorzystać losowe 40% rekordów z pierwszej połowy zbioru
jako zbiór uczący.

Aby otrzymać czytelne wykresy stworzyłem kilka mniejszych zbiorów testowych - pozwoli to przeprowadzić testy modeli dla różnych przypadków
oraz porównać otrzymane wyniki.

Poniżej przedstawiam wykresy obrazujące porównanie danych testowych z otrzymanymi wykresami modelowymi:
<p align="center">
  <img src="https://github.com/wlodarcp/Simple-Linear-Regression-/blob/master/Active%20Power%20Prediction.png">
</p>
To co można zaobserwować to duże "zanieczyszczenie" danych - w każdym zbiorze testowym występuje duża liczba wartości odstających

Porównując wyniki dla 5 zbiorów testowych (dla mocy czynnej): 

Największa wartość współczynnika determinacji jaką udało się uzyskać to 0.7 
Najmniejsza 0.37

Najmniejszy średni błąd kwadratowy 45 545
Największy 96 279

###### Moc bierna:

Analiza została przeprowadzona analogicznie

W procesie filtracji danych wyeliminowałem jedynie rekordy dla ujemnej oraz zbyt dużej prędkości oraz dla mocy biernej oscylującej wokół 0 (było ich bardzo dużo oraz występowały w całym przedziale prędkości)

W przypadku mocy biernej rozrzut danych był jeszcze gorszy co przekłada się na większe wartości błędów oraz niższe współczynniki determinacji

Największa wartość współczynnika determinacji jaką udało się uzyskać to 0.45
Najmniejsza 0.19

Najmniejszy średni błąd kwadratowy  17 740
Największy 25 668

## Wykresy:
<p align="center">
  <img src="https://github.com/wlodarcp/Simple-Linear-Regression-/blob/master/Reactive%20Power%20Prediction.png">
</p>
Analizowane przypadki są liniowe tylko w pewnych zakresach prędkości w związku z czym lepsze rezultaty można uzyskać przeprowadzając analizę na zbiorze danych zawierających jedynie prędkości z tego zakresu

Poniżej przedstawiam wyniki jakie można otrzymać dla zakresu prędkości od 7 do 16 m/s
<p align="center">
  <img src="https://github.com/wlodarcp/Simple-Linear-Regression-/blob/master/Active%20Power%20Prediction%20-%20cut.png">
</p>
Dla mocy czynnej udało się dzięki temu uzyskać lepsze wyniki - współczynnik determinacji 0.74 (maksymalny)
<p align="center">
  <img src="https://github.com/wlodarcp/Simple-Linear-Regression-/blob/master/Reactive%20Power%20Prediction%20-%20cut.png">
</p>
Dla mocy biernej z uwagi na bardzo duży rozrzut danych w tym zakresie otrzymane wyniki są nawet gorsze niż dla pełnego zakresu

# Podsumowanie:
-duży rozrzut analizowanych danych wpłynął negatywnie na wyniki - aby je poprawić należało by pomyśleć nad bardziej skomplikowanym
sposobem filtracji danych tak aby uzyskać wykresy zbliżone do "książkowych"

-badane wartości można opisać zależnością liniową tylko na pewnych przedziałach, aby uzyskać lepsze rezultaty należało by skorzystać
z regresji nieliniowej

-podczas analizy nie uwzględniałem innych wartości które mogły by wnieść wiele informacji do analizy i pozwoliły by stworzyć lepsze modele

