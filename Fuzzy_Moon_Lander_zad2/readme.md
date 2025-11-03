#  Fuzzy Lunar Lander  
**Projekt systemu sterowania rakietą z użyciem logiki rozmytej (Fuzzy Logic).**

---

##  Opis projektu
Celem projektu jest implementacja systemu sterowania lądownikiem księżycowym w środowisku **Gymnasium (LunarLanderContinuous-v3)** z wykorzystaniem **logiki rozmytej Mamdaniego**.  
System decyduje o mocy silnika głównego i bocznych, analizując parametry takie jak:
- pozycja (x, y),
- prędkość pionowa i pozioma,
- kąt nachylenia i prędkość kątowa,
- kontakt z podłożem.

---

##  Autorzy
- **s27433**
- **s28866**

---

##  Wymagania systemowe
- Python **3.11** lub **3.12**  
---

##  Przygotowanie środowiska

### 1️⃣ Klonowanie projektu
```bash
# Klonowanie repozytorium
git clone https://github.com/s27433-pj/NAI
```
#### 2️⃣ Jeśli używasz **Python 3.11 lub starszy**:
```bash
pip install -r requirements.txt
```

####  Jeśli używasz **Python 3.12**:
```bash
pip install -r requirements_3.12.txt
```
---
##  Uruchomienie programu
Po aktywowaniu środowiska uruchom:
```bash
python main.py
```

Każde uruchomienie programu:
- wykonuje **jeden losowy lot**,  
- wyświetla symulację,  
- i wypisuje wynik punktowy w konsoli.

---

##  Interpretacja wyników
Po zakończeniu symulacji w konsoli pojawi się raport:
```
========== WYNIK LOTU ==========
Wynik: -24.53
Seed:  8745621
================================
```

Im wyższy wynik (bliżej +200), tym **lepsze i bardziej miękkie lądowanie**.

---

##  Podgląd wyników

###  Udane miękkie lądowanie
![lander_loop](https://github.com/user-attachments/assets/7c8954f1-3541-452b-814f-28b21df8ec40)



###  Nieudane lądowanie
![lander_loop_failed](https://github.com/user-attachments/assets/0c62f28d-4fb2-46a2-a9e8-94f35ec97f43)


```
========== WYNIK LOTU ==========
Wynik: -91.33
Seed:  2
================================
```


