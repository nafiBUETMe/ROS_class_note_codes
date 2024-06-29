#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import rospy
from std_msgs.msg import Int32, String

# Callback functions for button presses
def on_button1():
    publish("motor1", "1")
    wheel_pub.publish(1)

def on_button2():
    publish("motor1Status", "c")
    status_pub.publish("c")

def on_button3():
    publish("motor1Status", "a")
    status_pub.publish("a")

def on_button4():
    publish("motor1", "0")
    wheel_pub.publish(0)

def fullSpeed():
    pwm_value.publish(255);

# Callback function for slider change
def on_slider_change(value):
    int_value = int(float(value))
    slider_value_label.config(text=f"Slider: {int_value}")
    pwm_value.publish(int_value)

# Placeholder function to simulate publishing to a topic
def publish(topic, message):
    print(f"Published '{message}' to '{topic}'")


# Initialize ROS node
rospy.init_node("L298N", anonymous=True)
wheel_pub = rospy.Publisher('motor1', Int32, queue_size=10)
status_pub = rospy.Publisher('motor1Status', String, queue_size=10)
pwm_value = rospy.Publisher('pwm', Int32, queue_size=10)

# Create main application window
root = tk.Tk()
root.title("Control Panel")

# Create buttons
button1 = ttk.Button(root, text="Start", command=on_button1)
button1.grid(row=0, column=0, padx=5, pady=5)

button2 = ttk.Button(root, text="Clock-wise", command=on_button2)
button2.grid(row=0, column=1, padx=5, pady=5)

button3 = ttk.Button(root, text="Anti-clock-wise", command=on_button3)
button3.grid(row=0, column=2, padx=5, pady=5)

button4 = ttk.Button(root, text="Stop", command=on_button4)
button4.grid(row=0, column=3, padx=5, pady=5)

button5 =  ttk.Button(root, text="Full Speed", command=fullSpeed)
button5.grid(row=0, column=4, padx=5, pady=5)

# Create slider
slider = ttk.Scale(root, from_=10, to_=255, orient='horizontal', command=on_slider_change)
slider.grid(row=1, column=0, columnspan=5, sticky='ew', padx=5, pady=5)

# Create slider value label
slider_value_label = tk.Label(root, text="Slider: 10")
slider_value_label.grid(row=2, column=0, columnspan=5)


# Start the main event loop
root.mainloop()
