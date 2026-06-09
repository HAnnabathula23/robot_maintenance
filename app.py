from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.maintenance_model import FEATURE_COLUMNS, predict_single, train_model


DATA_PATH = Path(__file__).resolve().parent / "data" / "sample_sensor_data.csv"
STYLE_PATH = Path(__file__).resolve().parent / "styles.css"


st.set_page_config(
    page_title="Robot Predictive Maintenance",
    page_icon="robot",
    layout="wide",
)


# loads the local css file so the app has a real frontend layer to edit.
def load_css(path: Path) -> None:
    if path.exists():
        st.markdown(f"<style>{path.read_text()}</style>", unsafe_allow_html=True)


@st.cache_data
# reads the sample robot telemetry csv once and lets streamlit cache it.
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_resource
# trains the model once for the current dataset and reuses the result.
def get_training_result(data: pd.DataFrame):
    return train_model(data)


# renders the top section that introduces the project.
def show_header() -> None:
    st.markdown(
        """
        <section class="hero">
          <div>
            <h1>Robot Predictive Maintenance</h1>
            <p class="hero-copy">
            </p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


# renders the model score cards and confusion matrix.
def show_model_performance(result) -> None:
    st.subheader("Model Performance")
    metric_cols = st.columns(4)
    for column, (label, value) in zip(
        metric_cols,
        result.metrics.items(),
    ):
        column.metric(label.title(), f"{value:.2f}")

    st.write("Confusion Matrix")
    confusion = pd.DataFrame(
        result.confusion,
        index=["Actual Normal", "Actual Risk"],
        columns=["Predicted Normal", "Predicted Risk"],
    )
    st.dataframe(confusion, use_container_width=True)


# renders the bar chart showing which signals mattered most.
def show_feature_importance(result) -> None:
    st.subheader("Most Important Signals")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(result.feature_importance["feature"], result.feature_importance["importance"])
    ax.invert_yaxis()
    ax.set_xlabel("Importance")
    ax.set_ylabel("")
    st.pyplot(fig)


# builds the sliders that act like a robot sensor reading.
def collect_sensor_values() -> dict[str, float]:
    st.subheader("Test a Robot Reading")
    return {
        "motor_temp_c": st.slider("Motor temperature (C)", 25.0, 115.0, 72.0),
        "vibration_g": st.slider("Vibration (g)", 0.05, 5.0, 1.4),
        "current_a": st.slider("Current draw (A)", 2.0, 55.0, 24.0),
        "battery_voltage_v": st.slider("Battery voltage (V)", 9.0, 13.2, 12.1),
        "wheel_speed_rpm": st.slider("Wheel speed (RPM)", 150.0, 5200.0, 2800.0),
        "torque_nm": st.slider("Torque (Nm)", 1.0, 48.0, 18.0),
        "operating_hours": st.slider("Operating hours", 0.0, 520.0, 210.0),
    }


# renders the live prediction for the slider values.
def show_prediction(result, values: dict[str, float]) -> None:
    st.subheader("Prediction")
    prediction, probability = predict_single(result.model, values)
    risk_label = "Elevated Failure Risk" if prediction else "Normal Operation"
    st.metric("Risk Probability", f"{probability * 100:.2f}%")
    st.progress(probability)

    if probability < 0.3:
        st.success(f"🟢 Low Risk ({probability * 100:.2f}%)")
    elif probability < 0.7:
        st.warning(f"🟡 Moderate Risk ({probability * 100:.2f}%)")
    else:
        st.error(f"🔴 High Risk ({probability * 100:.2f}%)")

    health = 100 - (probability * 100)
    st.metric("Robot Health Score", f"{health:.2f}/100")

    if prediction:
        st.error(risk_label)
        st.write("Recommended action: Inspect drivetrain, check cooling, and review recent robot logs.")
    else:
        st.success(risk_label)
        st.write("Recommended action: Continue monitoring sensor trends during operation.")

    sensor_df = pd.DataFrame(
        values.items(),
        columns=["Sensor", "Reading"]
    )

    st.dataframe(sensor_df)


# renders a quick peek at the generated dataset.
def show_dataset_preview(data: pd.DataFrame) -> None:
    st.divider()
    st.subheader("Dataset Preview")
    st.dataframe(data.head(12), use_container_width=True)


# wires the whole dashboard together from top to bottom.
def main() -> None:
    load_css(STYLE_PATH)
    data = load_data(DATA_PATH)
    result = get_training_result(data)

    show_header()

    metrics_col, chart_col = st.columns([1, 1.3])
    with metrics_col:
        show_model_performance(result)
    with chart_col:
        show_feature_importance(result)


    st.divider()
    input_col, output_col = st.columns([1, 1])
    with input_col:
        values = collect_sensor_values()
    with output_col:
        show_prediction(result, values)

    show_dataset_preview(data)


main()
