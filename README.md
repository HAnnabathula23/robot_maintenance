# Robot Predictive Maintenance Dashboard

This project is a small machine-learning prototype for predictive maintenance in a robotics setting. It uses simulated sensor readings from a robot drivetrain/motor system to predict whether the robot is at risk of a near-term mechanical or electrical failure.

The goal is to show a practical robotics workflow:

- collect or simulate sensor data
- train a classifier to detect failure risk
- inspect which sensor signals matter most
- provide a simple dashboard for testing new readings

## Features

- Synthetic robot sensor dataset generator
- Random Forest failure-risk classifier
- Model metrics: accuracy, precision, recall, F1 score, and confusion matrix
- Feature importance chart
- Streamlit dashboard for live predictions
- Example input controls for temperature, vibration, current, voltage, speed, torque, and operating hours
- Custom CSS frontend styling in `styles.css`
- GitHub and Streamlit deployment notes

## Project Structure

```text
.
├── .streamlit/
│   └── config.toml
├── app.py
├── data/
│   └── sample_sensor_data.csv
├── scripts/
│   └── generate_sample_data.py
├── src/
│   └── maintenance_model.py
├── DEPLOYMENT.md
├── requirements.txt
├── styles.css
├── UI_CUSTOMIZATION_GUIDE.md
└── README.md
```

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_sample_data.py
streamlit run app.py
```

## Frontend Styling

The main visual styling lives in `styles.css`. The app loads that file from `app.py`, so design changes can be made without rewriting the machine-learning logic.

The Streamlit theme colors live in `.streamlit/config.toml`.

For ideas on using UI inspiration sites without rebuilding the app, see `UI_CUSTOMIZATION_GUIDE.md`.

## Public Deployment

This app should be pushed to a public GitHub repository, then deployed with Streamlit Community Cloud. GitHub Pages cannot run the Python backend for this project by itself.

See `DEPLOYMENT.md` for the exact steps.

## Dataset

The included dataset is simulated. Each row represents one robot operating interval with sensor values such as motor temperature, vibration, current draw, battery voltage, wheel speed, torque, and hours of use.

The target column, `failure_risk`, is:

- `0`: normal operation
- `1`: elevated failure risk

The simulation intentionally makes failures more likely when the robot shows warning signs such as high temperature, high vibration, high current draw, voltage sag, high torque, or long runtime.

## Why This Matters for Robotics

Robotics teams care about reliability. A drivetrain motor, gearbox, wheel module, or battery system can fail during testing or competition. Predictive maintenance models can help identify risky operating patterns before a robot breaks.

This project is not a production maintenance system, but it demonstrates the core idea: using sensor data to turn raw robot telemetry into an actionable risk prediction.

## Possible Improvements

- Replace the synthetic data with real robot logs
- Add time-series features such as rolling averages
- Compare multiple models
- Add model export with `joblib`
- Add alert thresholds for pit crew diagnostics
- Connect the dashboard to a robot telemetry CSV
