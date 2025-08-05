import os

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.models.signature import infer_signature
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, auc, f1_score, precision_recall_curve
from sklearn.model_selection import train_test_split

from data_processing import CSV_URL, load_clean_telco


def main():
    """
    Main function to run the model training and logging workflow
    with advanced evaluation metrics and a model signature.
    """
    # Create the 'mlruns' directory if it doesn't exist.
    # This makes the script robust and prevents errors on the first run.
    # os.makedirs("mlruns", exist_ok=True)

    # Configure MLflow to use a local SQLite database.
    # This ensures that all artifact paths are stored relatively, making the
    # database portable and usable by a remote or containerized server.
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
    mlflow.set_tracking_uri(tracking_uri)

    # Load and Prepare Data
    print("Loading and preparing data...")
    df = load_clean_telco(CSV_URL)

    # For this MVP, I'm using a simplified feature set
    numerical = ["tenure", "monthlycharges", "totalcharges"]
    y = df["churn"]
    X = df[numerical].astype("float64")

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
        y_probs = lr.predict_proba(X_val)[:, 1]
        y_pred = lr.predict(X_val)

        accuracy = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred)
        precision, recall, _ = precision_recall_curve(y_val, y_probs)
        pr_auc = auc(recall, precision)

        print(f"Accuracy: {accuracy:.4f}")
        print(f"F1-Score: {f1:.4f}")
        print(f"PR-AUC: {pr_auc:.4f}")

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("pr_auc", pr_auc)

        # Infer the model signature from the training data to enforce schema
        signature = infer_signature(X_train, lr.predict(X_train))

        # Log the model with the signature and automatically register it under the specified name.
        mlflow.sklearn.log_model(
            sk_model=lr,
            name="model",
            signature=signature,
            registered_model_name="churn-prediction-mvp-lr",
        )

        print("\nRun complete. Check the MLflow UI.")


if __name__ == "__main__":
    main()
