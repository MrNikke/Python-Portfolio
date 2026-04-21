import pandas as pd
import numpy as np
import seaborn as sns
hki = pd.read_csv("Vantaa Helsinki-Vantaan lentoasema_ 1.1.1990 - 19.2.2025.csv",na_values="-")
hki.head()
hki.apply(pd.isnull).sum()
null_pct = hki.apply(pd.isnull).sum()/hki.shape[0]
null_pct

hki.head()
group_cols = ["Havaintoasema", "Vuosi", "Kuukausi", "Päivä"]
hki_combined = hki.groupby(group_cols, as_index=False).apply(lambda g: g.bfill().iloc[0])
hki_combined.reset_index(drop=True, inplace=True)
hki_combined
hki_combined.apply(pd.isnull).sum()
null_pct2 = hki_combined.apply(pd.isnull).sum()/hki_combined.shape[0]
null_pct2
valid_columns = hki_combined.columns[null_pct2 < 0.05]
valid_columns
hki = hki_combined[valid_columns].copy()
hki.apply(pd.isnull).sum()
hki.head()
hki = hki.ffill()
hki.apply(pd.isnull).sum()
hki.dtypes
hki.index
hki.Vuosi.value_counts().sort_index()
hki["Lumensyvyys [cm]"].plot()
hki['date'] = pd.to_datetime(hki['Vuosi'].astype(str) + '-' + 
                              hki['Kuukausi'].astype(str) + '-' + 
                              hki['Päivä'].astype(str))

# Optionally, drop the separate columns if you no longer need them:
hki.drop(columns=['Vuosi', 'Kuukausi', 'Päivä'], inplace=True)
hki['date'] = pd.to_datetime(hki['date'])
hki.set_index('date', inplace=True)
hki.index
hki["Lumensyvyys [cm]"].plot()
hki.loc["1990-01":"2025-12","Ilman keskilämpötila [°C]"].plot()
sns.scatterplot(x="Ilman keskilämpötila [°C]", y="Sademäärä [mm]", data=hki, hue="Lumensyvyys [cm]")
hki.dtypes
hki.head()
hki["Target"] = hki.shift(-1)["Ylin lämpötila [°C]"]
hki
hki = hki.ffill()
hki.info()
hki.to_csv("Weather_cleaned_data")
hki
corr_matrix = hki.corr(numeric_only=True)
corr_matrix

sns.heatmap(corr_matrix, annot=True)
from sklearn.linear_model import Ridge
rr = Ridge(alpha=.1)
# predictors = hki.columns[~hki.columns.isin(["Target", "Havaintoasema","Aika [Paikallinen aika]"])]
predictors = [
    "Sademäärä [mm]",
    "Lumensyvyys [cm]",
    "Ilman keskilämpötila [°C]",
    "Ylin lämpötila [°C]",
    "Alin lämpötila [°C]"
]
predictors
def backtest(weather, model, predictors, start=3650, step=90):
    all_predictions = []
    
    for i in range(start, weather.shape[0], step):
        train = weather.iloc[:i,:]
        test = weather.iloc[i:(i+step),:]
        
        model.fit(train[predictors], train["Target"])
        
        preds = model.predict(test[predictors])
        preds = pd.Series(preds, index=test.index)
        combined = pd.concat([test["Target"], preds], axis=1)
        combined.columns = ["actual", "prediction"]
        combined["diff"] = (combined["prediction"] - combined["actual"]).abs()
        
        all_predictions.append(combined)
    return pd.concat(all_predictions)
predictions = backtest(hki, rr, predictors)
predictions
from sklearn.metrics import mean_absolute_error, mean_squared_error

mean_absolute_error(predictions["actual"], predictions["prediction"])
predictions["diff"].mean()
def pct_diff(old, new):
    return (new - old) / old

def compute_rolling(hki, horizon, col):
    label = f"rolling_{horizon}_{col}"
    hki[label] = hki[col].rolling(horizon).mean()
    hki[f"{label}_pct"] = pct_diff(hki[label], hki[col])
    return hki
    
rolling_horizons = [3, 14]
for horizon in rolling_horizons:
    for col in ["Sademäärä [mm]", "Lumensyvyys [cm]", "Ilman keskilämpötila [°C]","Ylin lämpötila [°C]", "Alin lämpötila [°C]"]:
        hki = compute_rolling(hki, horizon, col)
hki
hki = hki.iloc[14:,:]
hki
hki.apply(pd.isnull).sum() #Missing values due to division with 0
hki = hki.fillna(0)
hki.apply(pd.isnull).sum()
def expand_mean(df):
    return df.expanding(1).mean()

for col in ["Sademäärä [mm]", "Lumensyvyys [cm]", "Ilman keskilämpötila [°C]","Ylin lämpötila [°C]", "Alin lämpötila [°C]"]:
    hki[f"month_avg_{col}"] = hki[col].groupby(hki.index.month, group_keys=False).apply(expand_mean)
    hki[f"day_avg_{col}"] = hki[col].groupby(hki.index.day_of_year, group_keys=False).apply(expand_mean)
hki
predictors = [
    "Sademäärä [mm]",
    "Lumensyvyys [cm]",
    "Ilman keskilämpötila [°C]",
    "Ylin lämpötila [°C]",
    "Alin lämpötila [°C]"
]
predictors
predictions = backtest(hki, rr, predictors)
mean_absolute_error(predictions["actual"], predictions["prediction"])
mean_absolute_error(predictions["actual"], predictions["prediction"])
predictions.sort_values("diff",ascending=False)
hki.loc["2006-01-12":"2006-01-30"] #check anomalies in temp regard to jan 22 2006
(predictions["diff"].round().value_counts().sort_index()) #Showing counts of different differences
(predictions["diff"].round().value_counts().sort_index().plot())
predictions
 
