import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, auc, f1_score, precision_recall_curve
from sklearn.model_selection import train_test_split


def main():
    """
    Main function to run the model training and logging workflow
    with advanced evaluation metrics.
    """
    # Load and Prepare Data
    print("Loading and preparing data...")
    data_url = "https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-03-churn-prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    df = pd.read_csv(data_url)

    # Basic data cleaning
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    categorical_columns = list(df.dtypes[df.dtypes == "object"].index)
    for c in categorical_columns:
        df[c] = df[c].str.lower().str.replace(" ", "_")
    df.totalcharges = pd.to_numeric(df.totalcharges, errors="coerce")
    df.totalcharges = df.totalcharges.fillna(0)
    df["churn"] = (df.churn == "yes").astype(int)

    # For this MVP, I'll use a simplified feature set
    numerical = ["tenure", "monthlycharges", "totalcharges"]
    y = df["churn"]
    X = df[numerical]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Model and Log with MLflow
    print("Training model and logging with MLflow...")
    mlflow.set_experiment("churn-prediction-mvp")

    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("features", "numerical_only")

        # Train the model
        lr = LogisticRegression()
        lr.fit(X_train, y_train)

        # Evaluate Model with Advanced Metrics
        # Get predicted probabilities for the positive class (churn=1)
        y_probs = lr.predict_proba(X_val)[:, 1]
        # Get binary predictions (0 or 1)
        y_pred = lr.predict(X_val)

        # Calculate metrics
        accuracy = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred)

        # Calculate PR-AUC
        precision, recall, _ = precision_recall_curve(y_val, y_probs)
        pr_auc = auc(recall, precision)

        # Log the metrics
        print(f"Accuracy: {accuracy:.4f}")
        print(f"F1-Score: {f1:.4f}")
        print(f"PR-AUC: {pr_auc:.4f}")

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("pr_auc", pr_auc)

        # Log the model
        mlflow.sklearn.log_model(lr, "model")

        print("\nRun complete. Check the MLflow UI.")
        print("A 'mlruns' directory has been created to store the experiment data.")


if __name__ == "__main__":
    main()
