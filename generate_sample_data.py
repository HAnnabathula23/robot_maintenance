from __future__ import annotations

import csv
import math
import random
from pathlib import Path


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_sensor_data.csv"


# keeps sensor values inside realistic-ish bounds.
def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


# turns sensor readings into a failure probability using a simple fake risk formula.
def failure_probability(
    motor_temp_c: float,
    vibration_g: float,
    current_a: float,
    battery_voltage_v: float,
    wheel_speed_rpm: float,
    torque_nm: float,
    operating_hours: float,
) -> float:
    score = -4.0
    score += (motor_temp_c - 65.0) / 12.0
    score += (vibration_g - 1.2) * 1.4
    score += (current_a - 22.0) / 8.0
    score += (12.0 - battery_voltage_v) * 1.3
    score += (torque_nm - 16.0) / 7.0
    score += (operating_hours - 180.0) / 160.0
    score += 0.25 if wheel_speed_rpm > 3600 else 0.0
    return 1.0 / (1.0 + math.exp(-score))


# creates one random robot sensor row for the csv.
def make_row() -> dict[str, float | int]:
    operating_hours = random.uniform(0, 520)
    load = random.betavariate(2.2, 2.8)
    wear = operating_hours / 520

    motor_temp_c = random.gauss(42 + 34 * load + 18 * wear, 5.5)
    vibration_g = random.gauss(0.35 + 1.7 * wear + 0.7 * load, 0.22)
    current_a = random.gauss(10 + 24 * load + 6 * wear, 3.2)
    battery_voltage_v = random.gauss(12.8 - 1.0 * load - 0.55 * wear, 0.25)
    wheel_speed_rpm = random.gauss(1250 + 2900 * load, 260)
    torque_nm = random.gauss(5.5 + 25 * load + 8 * wear, 2.6)

    motor_temp_c = clamp(motor_temp_c, 25, 115)
    vibration_g = clamp(vibration_g, 0.05, 5.0)
    current_a = clamp(current_a, 2, 55)
    battery_voltage_v = clamp(battery_voltage_v, 9.0, 13.2)
    wheel_speed_rpm = clamp(wheel_speed_rpm, 150, 5200)
    torque_nm = clamp(torque_nm, 1.0, 48.0)

    probability = failure_probability(
        motor_temp_c,
        vibration_g,
        current_a,
        battery_voltage_v,
        wheel_speed_rpm,
        torque_nm,
        operating_hours,
    )
    failure_risk = int(random.random() < probability)

    return {
        "motor_temp_c": round(motor_temp_c, 2),
        "vibration_g": round(vibration_g, 3),
        "current_a": round(current_a, 2),
        "battery_voltage_v": round(battery_voltage_v, 2),
        "wheel_speed_rpm": round(wheel_speed_rpm, 1),
        "torque_nm": round(torque_nm, 2),
        "operating_hours": round(operating_hours, 1),
        "failure_risk": failure_risk,
    }


# writes the full fake dataset into the data folder.
def main() -> None:
    random.seed(42)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = [make_row() for _ in range(1200)]
    with OUTPUT_PATH.open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
