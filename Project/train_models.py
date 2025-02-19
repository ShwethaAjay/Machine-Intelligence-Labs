import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
import optuna
import numpy as np


# Function to preprocess the data
def preprocess_data(file_path, target_column):
    df = pd.read_csv(file_path)

    # Handle missing values
    for col in df.select_dtypes(include=["float64", "int64"]):
        df[col].fillna(df[col].median(), inplace=True)
    for col in df.select_dtypes(include=["object"]):
        df[col].fillna(df[col].mode()[0], inplace=True)

    # Encode categorical features
    for col in df.select_dtypes(include=["object"]):
        df[col] = pd.factorize(df[col])[0]

    if "Average Wind Speed (Period)" in df.columns:
        df = df.drop(columns=["Average Wind Speed (Period)"])

    X = df.drop(columns=[target_column])
    y = df[target_column]

    return train_test_split(X, y, test_size=0.2, random_state=42)


# Function to build pipeline
def build_pipeline(model, numeric_features, n_components=0.95):
    # Preprocessing: Scaling and PCA
    preprocessor = ColumnTransformer(
        transformers=[
            ("scaler", StandardScaler(), numeric_features)
        ]
    )

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("pca", PCA(n_components=n_components)),
        ("model", model)
    ])

    return pipeline


# Function to print evaluation metrics
def evaluate_model(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\n--- Model Evaluation Metrics ---")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"R² Score: {r2:.4f}\n")


# Train and save Random Forest for solar power prediction
def train_solar_model():
    print("\nTraining Random Forest for Solar Power Generation Prediction...\n")
    X_train, X_test, y_train, y_test = preprocess_data("SolarPowerGeneration.csv", "Power Generated")
    numeric_features = X_train.select_dtypes(include=["float64", "int64"]).columns

    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 100, 300),
            "max_depth": trial.suggest_categorical("max_depth", [None, 10, 20, 30]),
            "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 5)
        }
        model = RandomForestRegressor(**params, random_state=42)
        pipeline = build_pipeline(model, numeric_features)
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        return mean_squared_error(y_test, y_pred)

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=50)

    # Train final model
    best_params = study.best_params
    rf_model = RandomForestRegressor(**best_params, random_state=42)
    final_pipeline = build_pipeline(rf_model, numeric_features)
    final_pipeline.fit(X_train, y_train)
    joblib.dump(final_pipeline, "solar_power_model.pkl")
    print("Solar power model saved as 'solar_power_model.pkl'.")


# Train and save Linear Regression for electricity prediction
def train_electricity_model():
    print("\nTraining Linear Regression for Electricity Bill Prediction...\n")
    X_train, X_test, y_train, y_test = preprocess_data("Household energy data.csv", "amount_paid")
    numeric_features = X_train.select_dtypes(include=["float64", "int64"]).columns

    def objective(trial):
        fit_intercept = trial.suggest_categorical("fit_intercept", [True, False])
        model = LinearRegression(fit_intercept=fit_intercept)
        pipeline = build_pipeline(model, numeric_features)
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        return mean_squared_error(y_test, y_pred)

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=50)

    # Train final model
    best_params = study.best_params
    final_model = LinearRegression(fit_intercept=best_params["fit_intercept"])
    final_pipeline = build_pipeline(final_model, numeric_features)
    final_pipeline.fit(X_train, y_train)
    joblib.dump(final_pipeline, "electricity_generation_model.pkl")
    print("Electricity bill model saved as 'electricity_bill_model.pkl'.")


def main():
    train_solar_model()
    train_electricity_model()


main()
