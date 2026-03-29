# 🎬Movie Review Data Bias Explorer

### Investigating Gender Bias in Movie Ratings using Data Science & Statistical Analysis


## 🚀 Overview

**Data Bias Explorer** is an interactive data science project that analyzes whether films directed by women receive systematically lower ratings than those directed by men.

Instead of relying on assumptions, this project uses **real IMDb data**, **statistical testing**, and **regression modeling** to uncover whether observed differences are due to bias or underlying confounding factors.


## 🎯 Problem Statement

> Do films directed by women receive lower ratings than those directed by men?

This project explores:

* Whether a rating gap exists
* Whether the gap is statistically significant
* Whether the gap persists after controlling for confounders


## 🧠 Approach

### 📊 1. Data Collection

* Source: IMDb Non-Commercial Datasets
* Files used:

  * `title.basics.tsv.gz`
  * `title.ratings.tsv.gz`
  * `title.crew.tsv.gz`
  * `name.basics.tsv.gz`

### 🧹 2. Data Cleaning & Processing

* Filtered only **movies**
* Removed low-vote entries (`numVotes > 100`)
* Extracted **directors**
* Inferred **gender from names**
* Handled missing and inconsistent values

### 📈 3. Statistical Analysis

* Compared rating distributions (women vs men)
* Computed:

  * Mean difference
  * Confidence intervals
  * Welch’s t-test
  * p-values
  * Effect size (Cohen’s d)

### 🤖 4. Regression Modeling

To control for confounders:

```
rating ~ gender + year + votes
```

This helps determine whether gender still affects ratings **after accounting for**:

* Release year
* Popularity (number of votes)

### 🎮 5. Interactive Features

* Load real dataset
* Simulate bias artificially
* Visual comparison of ratings
* Dynamic chart updates

## 🛠 Tech Stack

### Frontend

* HTML, CSS, JavaScript
* Chart.js (data visualization)

### Backend

* Python
* Pandas (data processing)
* Statsmodels (regression analysis)

## 📂 Project Structure

```
data-bias-explorer/
│
├── Backend/
│   ├── analysis.py
│   ├── title.basics.tsv.gz
│   ├── title.ratings.tsv.gz
│   ├── title.crew.tsv.gz
│   ├── name.basics.tsv.gz
│   └── movies_clean.csv
│
├── Frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── real_data.json
│
├── README.md
└── requirements.txt
```

---

## ▶️ How to Run

### 🔹 Step 1: Install dependencies

```bash
pip install pandas statsmodels
```

### 🔹 Step 2: Run backend (data processing)

```bash
cd Backend
python analysis.py
```

This will generate:

* `movies_clean.csv`
* `Frontend/real_data.json`


### 🔹 Step 3: Open frontend

Open:

```
Frontend/index.html
```

Click:
👉 **Load Real Data**


## 📊 Key Insights

* Raw data may show differences in average ratings
* Statistical testing determines if the gap is significant
* Regression reveals whether gender remains a factor after controlling variables


## ⚠️ Limitations

* Gender inference is approximate (based on names)
* Does not account for:

  * Budget
  * Marketing
  * Studio influence
* Correlation ≠ causation


## 🔥 Future Improvements

* Use gender APIs for higher accuracy
* Add genre-based regression
* Build Flask API backend
* Deploy as a full-stack web app
* Add user dataset upload


## 💡 Why This Project Matters

Bias in data leads to biased systems.

This project demonstrates how:

* Data can reflect societal patterns
* Statistical tools can uncover hidden bias
* Careful analysis is required before drawing conclusions

---

