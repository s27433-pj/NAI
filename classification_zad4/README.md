
# Opis

Projekt ma na celu klasyfikację jakości białego wina na podstawie jego właściwości chemicznych, z wykorzystaniem dwóch modeli uczenia maszynowego:
SVM (Support Vector Machine) oraz Decision Tree (drzewo decyzyjne).

# Zbiór danych
Używany zbiór: winequality-white.csv

# Analiza danych (EDA)

Tabela 1. Podsumowanie statystyczne wszystkich kolumn zbioru danych.
<img width="942" height="444" alt="1_wyniki_EDA" src="https://github.com/user-attachments/assets/fbcaa73d-73c0-4535-b6a0-cdaefb1488e4" />



(1 Histogram rozkładu jakości (PRZED transformacją) )<img width="991" height="676" alt="histogram_1_przed" src="https://github.com/user-attachments/assets/7b662677-ca84-4ce2-8bf2-b3f40d0a5d50" />

Rozkład klas jakości po sprowadzeniu wartości do przedziału [4, 8]

(2 Histogram rozkładu jakości (PO transformacji))<img width="987" height="647" alt="histogram_2_po" src="https://github.com/user-attachments/assets/565d69ce-ca5f-41af-be02-08f8e5632e15" />



# Przygotowanie danych

oddzielenie cech (X) od etykiet (y),

podział na zbiór treningowy i testowy (80/20),

standaryzacja cech w modelu SVM.

# Modele i strojenie hiperparametrów

Wyniki GridSearch — SVM

Najlepsze kombinacje hiperparametrów SVM według dokładności CV

(2 tabela) <img width="683" height="266" alt="Tabela_2" src="https://github.com/user-attachments/assets/6b6e6a01-9139-4e09-a611-146e4d08b45e" />


Najlepsze konfiguracje hiperparametrów dla drzewa decyzyjnego.”
(3 tabela)<img width="952" height="365" alt="Tabela_3_decison_tree" src="https://github.com/user-attachments/assets/6f424537-9e7f-4e31-b928-d53067fa593d" />



Porównanie wyników modeli SVM i Decision Tree
<img width="642" height="106" alt="4_porownanie" src="https://github.com/user-attachments/assets/3cafadd9-587f-46ef-9074-00f0f7cd1766" />





# Wizualizacja macierzy pomyłek

Macierz pomyłek — najlepszy model SVM (rbf)
(SVM)<img width="518" height="463" alt="svm_rbf" src="https://github.com/user-attachments/assets/9b75fd2e-89e5-4789-971b-f97bf0ffb154" />


Macierz pomyłek — najlepszy model SVM (linear).
(SVM linear)<img width="442" height="457" alt="svm_linear" src="https://github.com/user-attachments/assets/2064e59f-ef6d-46e2-92b6-2afdb354ec5e" />



Macierz pomyłek — najlepsze drzewo decyzyjne
(Decision tree)<img width="563" height="472" alt="Decision_tree" src="https://github.com/user-attachments/assets/dd8eafc7-576c-413e-ad09-b8cf411ec2fd" />



# testowanie modeli

Porównanie prawdziwych etykiet z predykcjami modeli
<img width="464" height="196" alt="last" src="https://github.com/user-attachments/assets/f18c4707-c3ea-4bee-a0b7-2bfbc6502708" />




## Authors

- [@s28866]()
- [@s27433]()

