import pandas as pd

TARGET = "churn"
CSV_URL = "https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-03-churn-prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv"


def load_clean_telco(url: str) -> pd.DataFrame:
    """Loads and cleans the Telco churn dataset."""
    df = pd.read_csv(url)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.lower().str.replace(" ", "_")
    df.totalcharges = pd.to_numeric(df.totalcharges, errors="coerce").fillna(0)
    df[TARGET] = (df.churn == "yes").astype(int)
    return df
