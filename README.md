# gyro-allan-deviation
A lightweight Python pipeline for analyzing gyroscope sensor noise using Allan Deviation (ADEV). Computes and visualizes noise characteristics from raw CSV IMU logs.
# Gyroscope Allan Deviation Analysis

A lightweight, vectorized Python tool designed to analyze and visualize the noise characteristics of Inertial Measurement Unit (IMU) gyroscope sensors using **Allan Deviation (ADEV)**. 

By calculating the Allan Variance across varying cluster times ($\tau$), this tool assists in identifying underlying stochastic error processes in inertial sensors, such as **Angle Random Walk (white noise)** and **Rate Random Walk**.

---

## 📈 Theoretical Overview

Allan Deviation is a time-domain analysis technique used to characterize noise in precision instruments. For gyroscopes, rather than analyzing raw angular rates directly, the data is first integrated into phase angles ($\theta$). The overlapping Allan Variance at a cluster time $\tau = m \cdot t_s$ is mathematically evaluated using:

$$\sigma^2(\tau) = \frac{1}{2\tau^2(N-2m)} \sum_{k=1}^{N-2m} \left( \theta_{k+2m} - 2\theta_{k+m} + \theta_k \right)^2$$

Where:
- $N$ is the total number of data points.
- $m$ is the cluster size factor.
- $t_s$ is the sensor sampling period ($1/f_s$).

---

## 🚀 Features

- **Vectorized Math:** Utilizes optimized `NumPy` array math to speed up calculation over long log durations.
- **Logarithmic Spacing:** Uses geometric spacing (`np.geomspace`) to safely evaluate up to $N/2$ cluster sizes without hitting memory/processing bottlenecks.
- **Data Resiliency:** Automatically detects and filters out missing or corrupt data points (`NaN` values) in the CSV log.
- **Tri-Axial Plotting:** Generates clear, side-by-side log-log plots comparing the $X$, $Y$, and $Z$ gyroscope axes.

---

## 📁 Repository Structure

```text
├── gyro-data.csv        # Raw IMU CSV log containing timestamp, x, y, and z axes
├── Gyro data.py         # Main execution script computing and plotting ADEV
└── README.md            # Project documentation
