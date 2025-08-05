"""
Generate a data-drift report for the Telco churn dataset, corrected for
an Evidently API version that uses DataDefinition and Dataset.from_pandas.

* Reads the same CSV your training script uses
* Applies the identical cleaning steps
* Saves an HTML dashboard and updates an Evidently workspace
"""

import datetime as dt
from pathlib import Path

import pandas as pd
from evidently import DataDefinition, Dataset, Report
from evidently.metrics import (
    DriftedColumnsCount,
    MaxValue,
    QuantileValue,
)
from evidently.presets import DataDriftPreset
from evidently.sdk.panels import bar_plot_panel, line_plot_panel, text_panel
from evidently.ui.workspace import Workspace

CSV_URL = "https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-03-churn-prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv"
WORKSPACE_DIR = "workspace"
PROJECT_NAME = "Telco Churn Data Quality"
HTML_REPORT_PATH = "reports/churn_drift_report.html"

# For drift analysis, we treat all relevant columns as features.
# The target 'churn' is included here as a numerical feature to check its drift.
NUM_FEATURES = ["tenure", "monthlycharges", "totalcharges", "churn"]
CAT_FEATURES = []  # none in this simplified model
TARGET_COL_NAME = "churn"  # Define for cleaning, but not used in DataDefinition


def load_clean_telco(url: str) -> pd.DataFrame:
    """Loads and cleans the Telco churn dataset from a URL."""
    df = pd.read_csv(url)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.lower().str.replace(" ", "_")
    df.totalcharges = pd.to_numeric(df.totalcharges, errors="coerce").fillna(0)
    df[TARGET_COL_NAME] = (df.churn == "yes").astype(int)
    return df


def main() -> None:
    """Main function to generate and save the drift report."""
    Path("reports").mkdir(exist_ok=True)
    print("Loading reference data…")
    reference_df = load_clean_telco(CSV_URL)

    # Simulate a current batch with drift
    print("Creating synthetic drifted batch…")
    current_df = reference_df.sample(frac=0.3, random_state=42).copy()
    current_df["monthlycharges"] *= 1.15  # upward price drift
    current_df["tenure"] -= 3  # newer customers

    # Create DataDefinition without the 'target_column' argument
    definition = DataDefinition(numerical_columns=NUM_FEATURES, categorical_columns=CAT_FEATURES)

    # --- FIX: Use the `from_pandas` class method to create Dataset objects ---
    ref_ds = Dataset.from_pandas(reference_df, definition)
    cur_ds = Dataset.from_pandas(current_df, definition)

    # Build a report focusing on data drift
    report = Report(
        metrics=[
            QuantileValue(column="monthlycharges", quantile=0.5),
            MaxValue(column="monthlycharges"),
            DriftedColumnsCount(),
            DataDriftPreset(),  # full preset dashboard for data drift
        ]
    )
    # The run method takes the Dataset objects
    report.run(reference_data=ref_ds, current_data=cur_ds)
    # report.save_html(HTML_REPORT_PATH)
    print(f"HTML drift report written → {HTML_REPORT_PATH}")

    # Update Evidently workspace/dashboard (optional but nice)
    ws = Workspace(WORKSPACE_DIR)
    project = ws.create_project(PROJECT_NAME, description="Telco churn monitoring")
    ws.add_run(project.id, report)

    # Simple dashboard panels (only once)
    if not project.dashboard.panels:
        project.dashboard.add_panel(text_panel(title="Telco Churn Dashboard"))
        project.dashboard.add_panel(
            bar_plot_panel(
                title="Drifted Columns",
                values=[
                    {"metric": "DriftedColumnsCount", "legend": "count"},
                ],
                size="half",
            )
        )
        project.dashboard.add_panel(
            line_plot_panel(
                title="Median MonthlyCharges (ref vs current)",
                values=[
                    {
                        "metric": "QuantileValue(column=monthlycharges,quantile=0.5)",
                        "legend": "median",
                    },
                ],
                size="half",
            )
        )
        project.save()
        print("Dashboard panels initialised.")

    print("\nDone. Start the web UI with:\n  evidently ui --workspace workspace")


if __name__ == "__main__":
    main()

# from evidently.presets import DataDriftPreset, DataSummaryPreset

# from evidently.ui.workspace import Workspace
# from evidently.sdk.panels import *
# from evidently.legacy.renderers.html_widgets import WidgetSize

# ws = Workspace("workspace")

# project = ws.create_project("Telco Data Quality Project")
# project.description = "My project description"
# project.save()

# regular_report = Report(
#     metrics=[
#         DataSummaryPreset()
#     ],
# )

# data_definition = DataDefinition(numerical_columns=num_features + ['prediction'], categorical_columns=cat_features)

# data = Dataset.from_pandas(
#     val_data.loc[val_data.lpep_pickup_datetime.between('2022-01-28', '2022-01-29', inclusive="left")],
#     data_definition=data_definition,
# )

# regular_snapshot = regular_report.run(current_data=data, timestamp=datetime.datetime(2022,1,28))

# ws.add_run(project.id, regular_snapshot)
