import pandas as pd
import pytest

from src.data_processing import load_clean_telco


# A simple fixture to create a sample DataFrame for testing
@pytest.fixture
def sample_raw_dataframe():
    """Create a sample raw DataFrame that mimics the real data."""
    data = {
        "gender": ["Female", "Male"],
        "Monthly Charges": [29.85, 53.85],
        "TotalCharges": ["29.85", "108.15"],
        "Churn": ["No", "Yes"],
    }
    return pd.DataFrame(data)


def test_load_clean_telco(sample_raw_dataframe):
    """
    Unit test for the data cleaning and preprocessing function.
    """

    df = sample_raw_dataframe
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.lower().str.replace(" ", "_")
    df.totalcharges = pd.to_numeric(df.totalcharges, errors="coerce").fillna(0)
    df["churn"] = (df.churn == "yes").astype(int)

    # Assertions: Check if the cleaning was successful
    assert "monthly_charges" in df.columns
    assert "totalcharges" in df.columns
    assert df["churn"].dtype == "int"
    assert df["churn"].tolist() == [0, 1]
    assert df["totalcharges"].dtype == "float64"
