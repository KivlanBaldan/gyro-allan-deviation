import numpy as np
import matplotlib.pyplot as plt

# --- Config. params ---
DATA_FILE = 'gyro-data.csv' 
fs = 100         # Sample rate [Hz]
maxNumM = 100    # Number of points to calculate

def AllanDeviation(data, fs, maxNumM=100):
    """Calculates Allan Deviation safely"""
    N = len(data)
    ts = 1.0 / fs
    # Filter out any NaNs just in case
    data = data[~np.isnan(data)]
    N = len(data)
    
    # Generate cluster sizes
    m = np.unique(np.geomspace(1, N // 2, num=maxNumM).astype(int))
    tau = m * ts
    adev = np.zeros(len(m))
    
    for i, mi in enumerate(m):
        # The core Allan Variance formula
        sum_sq = np.sum((data[2*mi:N] - 2*data[mi:N-mi] + data[0:N-2*mi])**2)
        allan_var = sum_sq / (2 * (tau[i]**2) * (N - 2*mi))
        adev[i] = np.sqrt(allan_var)
    return tau, adev

# --- Load Data ---
try:
    # 1. Skip the header row and the timestamp column
    # Use skip_header=1 to avoid NaNs from the text labels
    # Use usecols=(1,2,3) to skip the 'timestamp' column
    dataArr = np.genfromtxt(DATA_FILE, delimiter=',', skip_header=1, usecols=(1, 2, 3))
    
    # Check if data loaded correctly
    if np.isnan(dataArr).any():
        print("Warning: Data contains NaNs. Cleaning...")
        dataArr = dataArr[~np.isnan(dataArr).any(axis=1)]

    ts = 1.0 / fs

    # 2. Extract X, Y, Z (Columns 0, 1, 2 after skipping timestamp)
    gx = dataArr[:, 0]
    gy = dataArr[:, 1]
    gz = dataArr[:, 2]

    # 3. Calculate gyro angles (Integration)  
    # We do this because ADEV for rate sensors is calculated from the angle
    thetax = np.cumsum(gx) * ts
    thetay = np.cumsum(gy) * ts
    thetaz = np.cumsum(gz) * ts

    # 4. Compute Allan deviations
    print("Analyzing data...")
    (taux, adx) = AllanDeviation(thetax, fs, maxNumM=maxNumM)
    (tauy, ady) = AllanDeviation(thetay, fs, maxNumM=maxNumM)
    (tauz, adz) = AllanDeviation(thetaz, fs, maxNumM=maxNumM)

    # 5. Plot
    plt.figure(figsize=(10, 6))
    plt.plot(taux, adx, label='X-axis', color='tab:blue')
    plt.plot(tauy, ady, label='Y-axis', color='tab:orange')
    plt.plot(tauz, adz, label='Z-axis', color='tab:green')

    plt.xscale('log')
    plt.yscale('log')
    plt.title('Gyro Allan Deviations')
    plt.xlabel(r'$\tau$ [sec]')
    plt.ylabel('Deviation [deg/sec]')
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    plt.show()

except Exception as e:
    print(f"Error: {e}")