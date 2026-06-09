# Robot Predictive Maintenance

A machine learning project that predicts robot failure risk using simulated sensor data. The model analyzes readings such as temperature, vibration, current, voltage, speed, torque, and operating hours to estimate whether a robot is operating normally or may require maintenance.

## Features

* Predictive maintenance model using Random Forest
* Live Streamlit dashboard
* Failure risk predictions
* Model performance metrics
* Feature importance visualization
* Interactive sensor input controls

## Files

* `app.py` – Streamlit dashboard
* `sample_sensor_data.csv` – Example dataset
* `maintenance_model.py` – Machine learning logic
* `styles.css` – Dashboard styling

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset

The dataset contains simulated robot sensor readings and a target value:

* `0` = Normal operation
* `1` = Elevated failure risk

## Purpose

This project demonstrates how machine learning can be used to monitor robot health and identify potential failures before they occur.
