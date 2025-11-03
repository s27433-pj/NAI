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

Dzięki zastosowaniu reguł rozmytych oraz heurystyk, rakieta uczy się wykonywać **miękkie lądowania**, minimalizując ryzyko rozbicia.

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
git clone git clone https://github.com/s27433-pj/NAI.git
cd fuzzy-lunar-lander
```

### 2️⃣ Utworzenie środowiska wirtualnego
Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Instalacja zależności

####  Jeśli używasz **Python 3.11 lub starszy**:
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


###  Nieudane lądowanie
```
========== WYNIK LOTU ==========
Wynik: -91.33
Seed:  2
================================
```


