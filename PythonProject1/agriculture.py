import tkinter as tk
from tkinter import ttk
import requests
import json
from time import sleep
import sv_ttk  # For modern themed widgets

import io
import base64

# Firebase configuration
FIREBASE_URL = "https://project-dsa-2fc5f-default-rtdb.firebaseio.com/sensorData.json"


# Function to create rounded rectangle
def create_rounded_frame(parent, width, height, radius, bg_color="#FFFFFF"):
    frame = tk.Frame(parent, width=width, height=height, bg=parent["bg"], bd=0, highlightthickness=0)

    # Create a canvas with transparent background
    canvas = tk.Canvas(frame, width=width, height=height, bg=parent["bg"],
                       highlightthickness=0, bd=0)
    canvas.pack()

    # Draw rounded rectangle on canvas
    canvas.create_rectangle(radius, 0, width - radius, height, fill=bg_color, outline="", tags="rectangle")
    canvas.create_rectangle(0, radius, width, height - radius, fill=bg_color, outline="", tags="rectangle")
    canvas.create_arc(0, 0, 2 * radius, 2 * radius, start=90, extent=90, fill=bg_color, outline="", tags="arc1")
    canvas.create_arc(width - 2 * radius, 0, width, 2 * radius, start=0, extent=90, fill=bg_color, outline="",
                      tags="arc2")
    canvas.create_arc(0, height - 2 * radius, 2 * radius, height, start=180, extent=90, fill=bg_color, outline="",
                      tags="arc3")
    canvas.create_arc(width - 2 * radius, height - 2 * radius, width, height, start=270, extent=90, fill=bg_color,
                      outline="", tags="arc4")

    # Create an inner frame for content
    inner_frame = tk.Frame(frame, bg=bg_color)
    inner_frame.place(relx=0.5, rely=0.5, width=width - 20, height=height - 20, anchor="center")

    return frame, inner_frame


def fetch_data():
    try:
        response = requests.get(FIREBASE_URL)
        if response.status_code == 200:
            data = response.json()
            if data:
                update_labels(data)
    except Exception as e:
        print("Error fetching data:", e)


def update_labels(data):
    # Update values
    temp_val = data.get('temperature', 'N/A')
    humidity_val = data.get('humidity', 'N/A')
    soil_val = data.get('soilMoisture', 'N/A')
    light_val = data.get('lightIntensity', 'N/A')

    temperature_value.config(text=f"{temp_val}°C")
    humidity_value.config(text=f"{humidity_val}%")
    soil_value.config(text=f"{soil_val}")
    light_value.config(text=f"{light_val}")

    # Update progress bars
    try:
        temp_progress["value"] = float(temp_val) if temp_val != 'N/A' else 0
        humidity_progress["value"] = float(humidity_val) if humidity_val != 'N/A' else 0
        soil_progress["value"] = float(soil_val) if soil_val != 'N/A' else 0
        light_progress["value"] = float(light_val) if light_val != 'N/A' else 0
    except:
        pass

    # Update pump state with visual indicator
    pump_state = data.get('Pump', 'N/A')
    pump_value.config(text=f"{pump_state}")

    if pump_state == "ON":
        pump_indicator.config(bg="#4CAF50")  # Green when ON
        pump_status_text.config(text="ACTIVE", fg="#4CAF50")
    else:
        pump_indicator.config(bg="#F44336")  # Red when OFF
        pump_status_text.config(text="INACTIVE", fg="#F44336")

    # Schedule next update
    root.after(1000, fetch_data)  # Refresh every second


# GUI setup
root = tk.Tk()
root.title("Smart Greenhouse Monitor")
root.geometry("800x600")
root.configure(bg="#F0F8FF")  # Light blue background

# Apply modern theme
sv_ttk.set_theme("light")

# Create a gradient header
header_frame = tk.Frame(root, height=100, bg="#2E7D32")
header_frame.pack(fill=tk.X)

title_label = tk.Label(
    header_frame,
    text="SMART GREENHOUSE",
    font=("Montserrat", 24, "bold"),
    bg="#2E7D32",
    fg="white"
)
title_label.place(relx=0.5, rely=0.3, anchor="center")

subtitle_label = tk.Label(
    header_frame,
    text="Real-time Monitoring System",
    font=("Montserrat", 14),
    bg="#2E7D32",
    fg="#B3E5FC"
)
subtitle_label.place(relx=0.5, rely=0.7, anchor="center")

# Main content frame
content_frame = tk.Frame(root, bg="#F0F8FF", pady=20)
content_frame.pack(fill=tk.BOTH, expand=True)

# Dashboard title
dashboard_label = tk.Label(
    content_frame,
    text="DASHBOARD",
    font=("Montserrat", 16, "bold"),
    bg="#F0F8FF",
    fg="#1A237E"
)
dashboard_label.pack(pady=(0, 20))

# Create a frame for sensor readings
readings_frame = tk.Frame(content_frame, bg="#F0F8FF")
readings_frame.pack(fill=tk.BOTH, expand=True, padx=30)

# Temperature card
temp_outer_frame, temp_frame = create_rounded_frame(readings_frame, 320, 180, 15, "#FFFFFF")
temp_outer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

temp_icon_label = tk.Label(temp_frame, text="🌡️", font=("Segoe UI Emoji", 28), bg="white")
temp_icon_label.pack(pady=(10, 5))

temp_label = tk.Label(temp_frame, text="Temperature", font=("Montserrat", 14, "bold"), bg="white", fg="#1A237E")
temp_label.pack()

temperature_value = tk.Label(temp_frame, text="Loading...", font=("Montserrat", 22), bg="white", fg="#FF5722")
temperature_value.pack(pady=5)

temp_progress = ttk.Progressbar(temp_frame, orient="horizontal", length=250, mode="determinate", maximum=50)
temp_progress.pack(pady=10)

# Humidity card
humidity_outer_frame, humidity_frame = create_rounded_frame(readings_frame, 320, 180, 15, "#FFFFFF")
humidity_outer_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

humidity_icon_label = tk.Label(humidity_frame, text="💧", font=("Segoe UI Emoji", 28), bg="white")
humidity_icon_label.pack(pady=(10, 5))

humidity_label = tk.Label(humidity_frame, text="Humidity", font=("Montserrat", 14, "bold"), bg="white", fg="#1A237E")
humidity_label.pack()

humidity_value = tk.Label(humidity_frame, text="Loading...", font=("Montserrat", 22), bg="white", fg="#2196F3")
humidity_value.pack(pady=5)

humidity_progress = ttk.Progressbar(humidity_frame, orient="horizontal", length=250, mode="determinate", maximum=100)
humidity_progress.pack(pady=10)

# Soil Moisture card
soil_outer_frame, soil_frame = create_rounded_frame(readings_frame, 320, 180, 15, "#FFFFFF")
soil_outer_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

soil_icon_label = tk.Label(soil_frame, text="🌱", font=("Segoe UI Emoji", 28), bg="white")
soil_icon_label.pack(pady=(10, 5))

soil_label = tk.Label(soil_frame, text="Soil Moisture", font=("Montserrat", 14, "bold"), bg="white", fg="#1A237E")
soil_label.pack()

soil_value = tk.Label(soil_frame, text="Loading...", font=("Montserrat", 22), bg="white", fg="#795548")
soil_value.pack(pady=5)

soil_progress = ttk.Progressbar(soil_frame, orient="horizontal", length=250, mode="determinate", maximum=1000)
soil_progress.pack(pady=10)

# Light Intensity card
light_outer_frame, light_frame = create_rounded_frame(readings_frame, 320, 180, 15, "#FFFFFF")
light_outer_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

light_icon_label = tk.Label(light_frame, text="☀️", font=("Segoe UI Emoji", 28), bg="white")
light_icon_label.pack(pady=(10, 5))

light_label = tk.Label(light_frame, text="Light Intensity", font=("Montserrat", 14, "bold"), bg="white", fg="#1A237E")
light_label.pack()

light_value = tk.Label(light_frame, text="Loading...", font=("Montserrat", 22), bg="white", fg="#FFC107")
light_value.pack(pady=5)

light_progress = ttk.Progressbar(light_frame, orient="horizontal", length=250, mode="determinate", maximum=1000)
light_progress.pack(pady=10)

# Configure grid weights
readings_frame.columnconfigure(0, weight=1)
readings_frame.columnconfigure(1, weight=1)
readings_frame.rowconfigure(0, weight=1)
readings_frame.rowconfigure(1, weight=1)

# Pump status section
pump_outer_frame, pump_frame = create_rounded_frame(content_frame, 700, 80, 15, "#E8F5E9")
pump_outer_frame.pack(pady=20)

pump_status_label = tk.Label(
    pump_frame,
    text="WATER PUMP STATUS:",
    font=("Montserrat", 14, "bold"),
    bg="#E8F5E9",
    fg="#1A237E"
)
pump_status_label.pack(side=tk.LEFT, padx=20)

pump_status_text = tk.Label(
    pump_frame,
    text="LOADING...",
    font=("Montserrat", 14, "bold"),
    bg="#E8F5E9",
    fg="#757575"
)
pump_status_text.pack(side=tk.LEFT, padx=5)

pump_value = tk.Label(
    pump_frame,
    text="",
    font=("Montserrat", 1),
    bg="#E8F5E9"
)
pump_value.pack(side=tk.LEFT)

pump_indicator = tk.Frame(
    pump_frame,
    width=20,
    height=20,
    bg="#757575"  # Default gray
)
pump_indicator.pack(side=tk.LEFT, padx=10)
pump_indicator.config(highlightbackground="#1A237E", highlightthickness=2, bd=0)

# Group info
group_label = tk.Label(
    content_frame,
    text="Group: 19",
    font=("Montserrat", 10, "italic"),
    bg="#F0F8FF",
    fg="#757575"
)
group_label.pack(pady=(5, 0))

# Footer
footer_frame = tk.Frame(root, bg="#2E7D32", height=40)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

footer_text = tk.Label(
    footer_frame,
    text="© 2023 Smart Greenhouse System - Real-time Monitoring",
    font=("Montserrat", 10),
    bg="#2E7D32",
    fg="white"
)
footer_text.place(relx=0.5, rely=0.5, anchor="center")

# Start data fetching
fetch_data()
root.mainloop()