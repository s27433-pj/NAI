Klasyfikacja jakości białego wina

Projekt ma na celu klasyfikację jakości białego wina na podstawie jego właściwości chemicznych, z wykorzystaniem modeli:

SVM (Support Vector Machine)

Decision Tree (drzewo decyzyjne)

Zbiór danych

Używany zbiór: winequality-white.csv
Dane zawierają 4898 próbek oraz 11 cech numerycznych opisujących właściwości chemiczne wina.

Analiza danych (EDA)
Tabela 1. Podsumowanie statystyczne zbioru danych
<p align="center"> <img width="942" alt="1_wyniki_EDA" src="https://github.com/user-attachments/assets/fbcaa73d-73c0-4535-b6a0-cdaefb1488e4" /> </p>
Histogram rozkładu jakości (przed transformacją)
<p align="center"> <img width="700" alt="histogram_1_przed" src="https://github.com/user-attachments/assets/7b662677-ca84-4ce2-8bf2-b3f40d0a5d50" /> </p>
Histogram rozkładu jakości (po transformacji)
<p align="center"> <img width="700" alt="histogram_2_po" src="https://github.com/user-attachments/assets/565d69ce-ca5f-41af-be02-08f8e5632e15" /> </p>
Przygotowanie danych

Oddzielenie cech (X) od etykiet (y).

Podział na zbiór treningowy i testowy (80/20).

Standaryzacja cech w modelu SVM.

Modele i strojenie hiperparametrów
Wyniki GridSearch — SVM

Najlepsze kombinacje hiperparametrów według dokładności CV

<p align="center"> <img width="680" alt="Tabela_2" src="https://github.com/user-attachments/assets/6b6e6a01-9139-4e09-a611-146e4d08b45e" /> </p>
Wyniki GridSearch — Decision Tree

Najlepsze konfiguracje hiperparametrów

<p align="center"> <img width="900" alt="Tabela_3_decison_tree" src="https://github.com/user-attachments/assets/6f424537-9e7f-4e31-b928-d53067fa593d" /> </p>
Porównanie wyników modeli SVM i Decision Tree
<p align="center"> <img width="500" alt="4_porownanie" src="https://github.com/user-attachments/assets/3cafadd9-587f-46ef-9074-00f0f7cd1766" /> </p>
Wizualizacja macierzy pomyłek
SVM – kernel RBF
<p align="center"> <img width="450" alt="svm_rbf" src="https://github.com/user-attachments/assets/9b75fd2e-89e5-4789-971b-f97bf0ffb154" /> </p>
SVM – kernel Linear
<p align="center"> <img width="420" alt="svm_linear" src="https://github.com/user-attachments/assets/2064e59f-ef6d-46e2-92b6-2afdb354ec5e" /> </p>
Decision Tree – najlepszy model
<p align="center"> <img width="520" alt="Decision_tree" src="https://github.com/user-attachments/assets/dd8eafc7-576c-413e-ad09-b8cf411ec2fd" /> </p>
Testowanie modeli
Porównanie prawdziwych etykiet z predykcjami modeli
<p align="center"> <img width="400" alt="last" src="https://github.com/user-attachments/assets/f18c4707-c3ea-4bee-a0b7-2bfbc6502708" /> </p>
Autorzy

@s28866

@s27433
