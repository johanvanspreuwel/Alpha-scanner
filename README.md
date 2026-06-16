# 🔎 Alpha Scanner

> Streamlit stock scanner · bodemfase · accumulatie detectie

Een interactieve beurscanner die aandelen zoekt die **kortstondig in een dip** zitten en klaar kunnen zijn voor een herstelbeweging.

## Actieve strategie — Alpha Scanner

| Criterium | Waarde |
|-----------|--------|
| Fase | Bodemfase / accumulatie |
| RSI (14) | ≤ 45 |
| Koers vs support | 0.0 – 5.0 % boven support |
| Volume | ≥ 0.8× 20-daags gemiddelde (laag volume = accumulatie) |

---

## Ondersteunde markten

| Index | Beurs |
|-------|-------|
| S&P 500 | NYSE / Nasdaq |
| S&P 400 MidCap | NYSE / Nasdaq |
| Nasdaq-100 | Nasdaq |
| AEX | Amsterdam (Euronext) |
| DAX | Frankfurt (XETRA) |
| CAC 40 | Parijs (Euronext) |
| FTSE 100 | Londen (LSE) |
| IBEX 35 | Madrid (BME) |
| SMI | Zürich (SIX) |
| BEL 20 | Brussel (Euronext) |
| OMX Stockholm | Stockholm |
| OMX Helsinki | Helsinki |
| OMX Copenhagen | Kopenhagen |
| PSI | Lissabon |
| ATX | Wenen |
| MIB | Milaan (Borsa Italiana) |

---

## Lokaal draaien

```bash
# 1. Clone de repo
git clone https://github.com/JOUW_GEBRUIKERSNAAM/alpha-scanner.git
cd alpha-scanner

# 2. Virtuele omgeving (aanbevolen)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Dependencies
pip install -r requirements.txt

# 4. Starten
streamlit run app.py
```

De app opent automatisch op `http://localhost:8501`.

---

## Deployen op Streamlit Cloud (gratis)

1. **Push naar GitHub**

```bash
git init
git add .
git commit -m "initial commit: Alpha Scanner"
git remote add origin https://github.com/JOUW_GEBRUIKERSNAAM/alpha-scanner.git
git push -u origin main
```

2. **Streamlit Cloud**
   - Ga naar [share.streamlit.io](https://share.streamlit.io)
   - Klik **New app**
   - Kies je GitHub-repo
   - Main file: `app.py`
   - Klik **Deploy**

Streamlit installeert automatisch de `requirements.txt` en de app is binnen een minuut live.

---

## Projectstructuur

```
alpha-scanner/
├── app.py            # Streamlit UI
├── scanner.py        # Scanner logica (RSI, support, volume)
├── tickers.py        # Ticker universum (alle beurzen)
├── requirements.txt  # Python dependencies
├── .streamlit/
│   └── config.toml   # Donker thema
└── README.md
```

---

## Hoe werkt de scanner?

```
Voor elk aandeel in het universum:
  1. Download 6 maanden OHLCV (Yahoo Finance)
  2. Bereken RSI-14
  3. Bereken support = laagste low afgelopen 20 beursdagen
  4. Bereken volume-ratio t.o.v. 20-daags gemiddelde
  5. Check alle Alpha-criteria
  6. Toon hits gesorteerd op RSI (laagste eerst)
```

### Support definitie

Support wordt berekend als het **laagste low van de afgelopen 20 handelsdagen** (excl. huidige dag). Dit is een eenvoudig maar effectief niveau om recente bodems te identificeren.

---

## Uitbreiden met meer scanners

De architectuur is modulair. Voeg een nieuwe scanner toe door:

1. Een functie `beta_conditions(ind, params)` in `scanner.py` te maken
2. Een nieuwe tab in `app.py` toe te voegen
3. De scanner via `run_scan(..., condition_fn=beta_conditions)` aan te roepen

---

## Disclaimer

> Dit project is uitsluitend bedoeld voor educatieve doeleinden.  
> Niets hier is beleggingsadvies. Data via Yahoo Finance.
