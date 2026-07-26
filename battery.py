import psutil

# Function to get the battery status
def get_battery():
    return psutil.sensors_battery()