# Simple-Linear-Regression-
## Regresja Liniowa - podsumowanie

## Cel
Celem zadania było przeprowadzenie krótkiej analizy zbioru danych której rezultatem miały być modele regresji liniowej
dla mocy czynnej i biernej od prędkości wiatru.

## Realizacja

###### Moc czynna:

Zbiór uczący 80%, treningowy 20%

Otrzymane wyniki:

średni błąd kwadratowy: 93297.54

Współczynnik determinacji: 0.47

Z uwagi na dużą ilość wartośći odstających otrzymać czytelne wykresy przedstawiłem wyniki dla mniejszych części danych treningowych.

Poniżej przedstawiam wykresy obrazujące porównanie danych testowych z otrzymanymi wykresami modelowymi:
<p align="center">
  <img src="https://github.com/wlodarcp/Simple-Linear-Regression-/blob/master/Active%20Power%5BMW%5D%20(Simple%20LR).png">
</p>

To co można zaobserwować to duże "zanieczyszczenie" danych - w każdym zbiorze testowym występuje duża liczba wartości odstających


###### Moc bierna:

Analiza została przeprowadzona analogicznie

Zbiór uczący 80%, treningowy 20%

Otrzymane wyniki:

średni błąd kwadratowy: 25190.98

Współczynnik determinacji: 0.18

W przypadku mocy biernej rozrzut danych był jeszcze gorszy co przekłada się na większe wartości błędów oraz niższe współczynniki determinacji

## Wykresy:
<p align="center">
  <img src="https://github.com/wlodarcp/Simple-Linear-Regression-/blob/master/Reactive%20Power%20%5BMVAR%5D%20(Simple%20LR).png">
</p>

###### Moc czynna z wykorzystaniem metody walidacji krzyżowej:

średni błąd kwadratowy: 97726.91

Współczynnik determinacji: 0.44

## Wykresy:
<p align="center">
  <img src="https://github.com/wlodarcp/Simple-Linear-Regression-/blob/master/Active%20Power%5BMW%5D%20(Cross%20Val).png">
</p>

###### Moc bierna z wykorzystaniem metody walidacji krzyżowej:

średni błąd kwadratowy: 569989.31

Współczynnik determinacji: 0.16

## Wykresy:
<p align="center">
  <img src="https://github.com/wlodarcp/Simple-Linear-Regression-/blob/master/Reactive%20Power%20%5BMVAR%5D%20(Cross%20Val).png">
</p>

Moc czynna zmienia się liniowo tylko w pewnych zakresach prędkości w związku z czym lepsze rezultaty można uzyskać przeprowadzając analizę na zbiorze danych zawierających jedynie prędkości z tego zakresu

Poniżej przedstawiam wyniki dla mocy czynnej jakie można otrzymać dla zakresu prędkości od 7 do 15 m/s

średni błąd kwadratowy: 83807.99

Współczynnik determinacji: 0.38

<p align="center">
  <img src="https://github.com/wlodarcp/Simple-Linear-Regression-/blob/master/Active%20Power%5BMW%5D%20speed%207-15%20ms.png">
</p>


# Podsumowanie:
-duży rozrzut analizowanych danych wpłynął negatywnie na wyniki - aby je poprawić należało by pomyśleć nad bardziej skomplikowanym
sposobem filtracji danych tak aby uzyskać wykresy zbliżone do "książkowych"

-analizując wykresy stworzone z różnych części zbioru treningowego można zaobserwować dużą nierównomierność rozkładu danych - w pewnych obszarach otrzymujemy prawie idealnie zgodne z oczekiwaniami kształty wykresów natomiast występują również przedziały w których dane nie dają żadnej informacji o przebiegu zjawiska (wyglądają na zupełnie losowe) - należało by przeanalizować pozostałe dane w celu znalezienia czynnika który może determinować takie wyniki

-badane wartości można opisać zależnością liniową tylko na pewnych przedziałach, aby uzyskać lepsze rezultaty należało by skorzystać
z regresji nieliniowej

-wyniki uzyskane metodą walidacji krzyżowej są porównywalne a nawet gorsze od uzyskanych standardową metodą - zawewne przez tak dużą nierównomierność rozkładu

-podczas analizy nie uwzględniałem innych wartości które mogły by wnieść wiele informacji do analizy i pozwoliły by stworzyć lepsze modele

