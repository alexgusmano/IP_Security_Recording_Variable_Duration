import cv2
import easygui as eg
import datetime
import time

# Function to calculate the time until the desired start time
def time_until_desired_start(desired_start_time):
    current_time = datetime.datetime.now().time()
    desired_time = datetime.datetime.strptime(desired_start_time, "%H:%M").time()
    time_difference = datetime.datetime.combine(datetime.date.today(), desired_time) - datetime.datetime.combine(datetime.date.today(), current_time)
    return time_difference.total_seconds()

# Use easygui to prompt the user for the IP address and port
msg = "Enter the IP address and port of your IP camera (e.g., http://192.168.1.100:8080/video):"
title = "IP Camera Setup"
default_ip = "http://your_ip_address:your_port/video"
ip_camera_url = eg.enterbox(msg, title, default=default_ip)

if ip_camera_url is None:
    exit()  # The user clicked Cancel

# Use easygui to prompt the user for a target location to save the recordings
msg = "Choose a location to save the recordings:"
title = "Select Output Location"
output_folder = eg.diropenbox(msg, title)

if output_folder is None:
    exit()  # The user clicked Cancel

# Prompt the user for the desired start time
msg = "Enter the desired start time (HH:MM):"
title = "Set Start Time"
desired_start_time = eg.enterbox(msg, title)

if desired_start_time is None:
    exit()  # The user clicked Cancel
            

# Prompt the user for the desired duration
msg = "Enter the desired recording length in hours:"
title = "Set Duration"
desired_duration = eg.enterbox(msg, title)

# Calculate the time until the desired start time
time_until_start = time_until_desired_start(desired_start_time)

if time_until_start > 0:
    print(f"Waiting for {int(time_until_start / 60)} minutes until the desired start time...")
    time.sleep(time_until_start)

# Create a VideoCapture object to connect to the camera
cap = cv2.VideoCapture(ip_camera_url)

# Get the current date and time for filenames
start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Define the codec and create a VideoWriter object with the start time in the filename
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = f'{output_folder}/recording_{start_time}.avi'
out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))  # You may need to adjust the resolution and frame rate

# Record for n hours 
record_duration = desired_duration*60*60 # converts hours in total seconds
start_timestamp = time.time()
#Alexander Gusmano

while time.time() - start_timestamp < record_duration:
    ret, frame = cap.read()  # Read a frame from the camera

    if not ret:
        print("Error: Could not read frame.")
        break

    out.write(frame)  # Write the frame to the output video file

    cv2.imshow('IP Camera Feed', frame)  # Display the live feed

    # Check if the 'q' key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the VideoCapture and VideoWriter objects
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

# At this point, you can rename the file to include the end time if desired
end_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
new_output_file = f'{output_folder}/Camera_Feed_{start_time}_to_{end_time}.avi'
import os
os.rename(output_file, new_output_file)

