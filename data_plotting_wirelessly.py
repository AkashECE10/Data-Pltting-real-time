import socket
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define constants
HOST = '192.168.4.1'  # IP address of M5StickC Plus2 AP
PORT = 80             # Port number
NUM_SAMPLES = 100     # Number of samples to keep in the plot

# Initialize lists for data
accel_x = []
accel_y = []
accel_z = []
gyro_x = []
gyro_y = []
gyro_z = []

# Initialize plot
fig, (ax1, ax2) = plt.subplots(2, 1)

# Create line objects for plotting
line_ax, = ax1.plot([], [], label='Accel X')
line_ay, = ax1.plot([], [], label='Accel Y')
line_az, = ax1.plot([], [], label='Accel Z')
line_gx, = ax2.plot([], [], label='Gyro X')
line_gy, = ax2.plot([], [], label='Gyro Y')
line_gz, = ax2.plot([], [], label='Gyro Z')

# Function to update plot
def update_plot(frame):
    line_ax.set_data(range(len(accel_x[-NUM_SAMPLES:])), accel_x[-NUM_SAMPLES:])
    line_ay.set_data(range(len(accel_y[-NUM_SAMPLES:])), accel_y[-NUM_SAMPLES:])
    line_az.set_data(range(len(accel_z[-NUM_SAMPLES:])), accel_z[-NUM_SAMPLES:])
    line_gx.set_data(range(len(gyro_x[-NUM_SAMPLES:])), gyro_x[-NUM_SAMPLES:])
    line_gy.set_data(range(len(gyro_y[-NUM_SAMPLES:])), gyro_y[-NUM_SAMPLES:])
    line_gz.set_data(range(len(gyro_z[-NUM_SAMPLES:])), gyro_z[-NUM_SAMPLES:])
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    return line_ax, line_ay, line_az, line_gx, line_gy, line_gz

# Initialize plot settings
ax1.legend()
ax2.legend()
ax1.set_title('Accelerometer Data')
ax2.set_title('Gyroscope Data')
plt.tight_layout()

def data_generator():
    global connected
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            connected = True
            print(f"Connected to M5StickC Plus2 at {HOST}:{PORT}")

            while connected:
                try:
                    data = s.recv(1024).decode('utf-8')
                    if data:
                        print(f"Received data: {data.strip()}")  # Debugging: print the received data
                        # Parse and append data to the lists
                        values = data.strip().split(',')
                        if len(values) == 6:
                            accel_x.append(float(values[0]))
                            accel_y.append(float(values[1]))
                            accel_z.append(float(values[2]))
                            gyro_x.append(float(values[3]))
                            gyro_y.append(float(values[4]))
                            gyro_z.append(float(values[5]))
                        yield data  # Yield the data for animation
                    else:
                        raise ValueError("No data received.")
                except Exception as e:
                    print(f"Error receiving data: {e}")
                    connected = False
                    break
    except Exception as e:
        print(f"Error connecting to M5StickC Plus2: {e}")
        connected = False

# Connect to M5StickC Plus2
connected = False

# Start the plot animation
anim = FuncAnimation(fig, update_plot, frames=data_generator, interval=500, blit=True)
plt.show()

if not connected:
    print("Failed to maintain connection to M5StickC Plus2.")
