from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split


FEATURE_COLUMNS = [
    "motor_temp_c",
    "vibration_g",
    "current_a",
    "battery_voltage_v",
    "wheel_speed_rpm",
    "torque_nm",
    "operating_hours",
]

TARGET_COLUMN = "failure_risk"


@dataclass
# keeps everything from training in one easy object.
class TrainingResult:
    model: RandomForestClassifier
    metrics: dict[str, float]
    confusion: list[list[int]]
    feature_importance: pd.DataFrame
    test_rows: pd.DataFrame
    predictions: pd.Series


# checks that the csv has the columns the model expects.
def validate_dataset(data: pd.DataFrame) -> None:
    required = set(FEATURE_COLUMNS + [TARGET_COLUMN])
    missing = sorted(required - set(data.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")


# trains a random forest and returns the model plus useful dashboard stats.
def train_model(data: pd.DataFrame) -> TrainingResult:
    validate_dataset(data)

    x = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=7,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=160,
        max_depth=8,
        random_state=7,
        class_weight="balanced",
    )
    model.fit(x_train, y_train)

    y_pred = pd.Series(model.predict(x_test), index=x_test.index, name="predicted_risk")

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
    }

    importance = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    return TrainingResult(
        model=model,
        metrics=metrics,
        confusion=confusion_matrix(y_test, y_pred).tolist(),
        feature_importance=importance,
        test_rows=x_test,
        predictions=y_pred,
    )


# predicts one manual sensor reading from the dashboard sliders.
def predict_single(model: RandomForestClassifier, values: dict[str, float]) -> tuple[int, float]:
    row = pd.DataFrame([{column: values[column] for column in FEATURE_COLUMNS}])
    prediction = int(model.predict(row)[0])
    probability = float(model.predict_proba(row)[0][1])
    return prediction, probability
