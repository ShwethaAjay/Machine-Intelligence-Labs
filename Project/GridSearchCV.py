import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
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


# Function for cross-validation and hyperparameter tuning
def train_and_tune_model(pipeline, param_grid, X_train, y_train):
    grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error',
                               verbose=1, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print(f"Best Parameters: {grid_search.best_params_}")
    print(f"Best Cross-Validation Score: {np.sqrt(-grid_search.best_score_):.4f}")
    return grid_search.best_estimator_


# Function to evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mse)

    print("\nModel Evaluation:")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"R² Score: {r2:.4f}")

    return y_pred


# Household Electricity Prediction
print("\n--- Household Monthly Electricity Bill Prediction ---\n")
X_train, X_test, y_train, y_test = preprocess_data("Household energy data.csv", "amount_paid")
numeric_features = X_train.select_dtypes(include=["float64", "int64"]).columns

# Linear Regression with Pipeline
lr_model = LinearRegression()
lr_pipeline = build_pipeline(lr_model, numeric_features)
param_grid_lr = {
    "model__fit_intercept": [True, False]
}

best_lr_pipeline = train_and_tune_model(lr_pipeline, param_grid_lr, X_train, y_train)
evaluate_model(best_lr_pipeline, X_test, y_test)

# Solar Power Generation Prediction
print("\n--- Solar Power Generation Prediction ---\n")
X_train, X_test, y_train, y_test = preprocess_data("SolarPowerGeneration.csv", "Power Generated")
numeric_features = X_train.select_dtypes(include=["float64", "int64"]).columns

# Random Forest Regressor with Pipeline
rf_model = RandomForestRegressor(random_state=42)
rf_pipeline = build_pipeline(rf_model, numeric_features)
param_grid_rf = {
    "model__n_estimators": [200, 250, 300],
    "model__max_depth": [None, 10, 20],
    "model__min_samples_split": [2, 5, 10],
    "model__min_samples_leaf": [1, 2, 4]
}

best_rf_pipeline = train_and_tune_model(rf_pipeline, param_grid_rf, X_train, y_train)
evaluate_model(best_rf_pipeline, X_test, y_test)
