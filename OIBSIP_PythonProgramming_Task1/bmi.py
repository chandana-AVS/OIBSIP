import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------- THEME ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    gender TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    date TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def convert_height_to_meters(height, unit, inches=0):
    if unit == "cm":
        return height / 100
    elif unit == "m":
        return height
    elif unit == "ft":
        return (height * 0.3048) + (inches * 0.0254)

# -------- NEW FEATURES --------
def ideal_weight_range(height):
    return 18.5 * height**2, 24.9 * height**2

def weight_difference(weight, min_w, max_w):
    if weight < min_w:
        return f"Gain {min_w - weight:.1f} kg"
    elif weight > max_w:
        return f"Lose {weight - max_w:.1f} kg"
    else:
        return "You are in ideal range"

def body_fat_percentage(bmi, age, gender):
    g = 1 if gender == "Male" else 0
    return (1.20 * bmi) + (0.23 * age) - (10.8 * g) - 5.4

def calculate_bmr(weight, height_cm, age, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height_cm - 5 * age - 161

# ---------------- CHARTS ----------------
def show_bmi_pie_chart():
    cursor.execute("SELECT bmi FROM users")
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("Info", "No data available")
        return

    categories = {"Underweight":0,"Normal":0,"Overweight":0,"Obese":0}

    for (bmi,) in data:
        if bmi < 18.5:
            categories["Underweight"] += 1
        elif bmi < 25:
            categories["Normal"] += 1
        elif bmi < 30:
            categories["Overweight"] += 1
        else:
            categories["Obese"] += 1

    plt.figure()
    plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
    plt.title("BMI Category Distribution")
    plt.show()

def view_graph():
    name = name_entry.get()
    cursor.execute("SELECT date, bmi FROM users WHERE name=?", (name,))
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("Info", "No data found")
        return

    dates = [d[0] for d in data]
    bmis = [d[1] for d in data]

    plt.plot(dates, bmis, marker='o')
    plt.xticks(rotation=45)
    plt.title("BMI Trend")
    plt.show()

# ---------------- MAIN LOGIC ----------------
def submit_data():
    try:
        name = name_entry.get()
        gender = gender_var.get()
        weight = float(weight_entry.get())
        age = int(age_entry.get())

        if unit_var.get() == "ft":
            feet = float(feet_entry.get())
            inches = float(inch_entry.get() or 0)
            height = convert_height_to_meters(feet, "ft", inches)
        else:
            height = convert_height_to_meters(float(height_entry.get()), unit_var.get())

        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)

        # NEW CALCULATIONS
        min_w, max_w = ideal_weight_range(height)
        diff_msg = weight_difference(weight, min_w, max_w)
        body_fat = body_fat_percentage(bmi, age, gender)
        height_cm = height * 100
        bmr = calculate_bmr(weight, height_cm, age, gender)

        cursor.execute("""
        INSERT INTO users (name, gender, weight, height, bmi, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, gender, weight, height, bmi,
              datetime.now().strftime("%Y-%m-%d")))
        conn.commit()

        result_label.configure(
            text=f"""BMI: {bmi:.2f} ({category})

Ideal Weight: {min_w:.1f} - {max_w:.1f} kg
{diff_msg}

Body Fat: {body_fat:.1f} %
Calories Needed: {bmr:.0f} kcal"""
        )

    except:
        messagebox.showerror("Error", "Invalid Input")

# ---------------- UI ----------------
app = ctk.CTk()
app.title("BMI Tracker")
app.geometry("420x650")

frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(pady=30, padx=30, fill="both", expand=True)

ctk.CTkLabel(frame, text="BMI Tracker", font=("Arial", 22, "bold")).pack(pady=15)

name_entry = ctk.CTkEntry(frame, placeholder_text="Enter Name")
name_entry.pack(pady=8)

gender_var = ctk.StringVar(value="Male")
ctk.CTkOptionMenu(frame, values=["Male", "Female"], variable=gender_var).pack(pady=8)

age_entry = ctk.CTkEntry(frame, placeholder_text="Age")
age_entry.pack(pady=8)

# INPUT GRID
input_frame = ctk.CTkFrame(frame, fg_color="transparent")
input_frame.pack(pady=10)

weight_entry = ctk.CTkEntry(input_frame, placeholder_text="Weight (kg)", width=140)
weight_entry.grid(row=0, column=0, padx=10, pady=10)

height_entry = ctk.CTkEntry(input_frame, placeholder_text="Height", width=140)
height_entry.grid(row=0, column=1, padx=10, pady=10)

ft_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
feet_entry = ctk.CTkEntry(ft_frame, width=60, placeholder_text="ft")
feet_entry.grid(row=0, column=0, padx=5)
inch_entry = ctk.CTkEntry(ft_frame, width=60, placeholder_text="in")
inch_entry.grid(row=0, column=1, padx=5)

unit_var = ctk.StringVar(value="cm")
ctk.CTkOptionMenu(frame, values=["cm", "m", "ft"], variable=unit_var).pack(pady=5)

def toggle_height(*args):
    if unit_var.get() == "ft":
        height_entry.grid_forget()
        ft_frame.grid(row=0, column=1, padx=10, pady=10)
    else:
        ft_frame.grid_forget()
        height_entry.grid(row=0, column=1, padx=10, pady=10)

unit_var.trace("w", toggle_height)

# BUTTONS
ctk.CTkButton(frame, text="Calculate BMI", command=submit_data, width=200).pack(pady=15)

bottom_frame = ctk.CTkFrame(frame, fg_color="transparent")
bottom_frame.pack(pady=5)

ctk.CTkButton(bottom_frame, text="View Graph", command=view_graph, width=120).grid(row=0, column=0, padx=10)
ctk.CTkButton(bottom_frame, text="Pie Chart", command=show_bmi_pie_chart, width=120).grid(row=0, column=1, padx=10)

result_label = ctk.CTkLabel(frame, text="", font=("Arial", 15))
result_label.pack(pady=20)

app.mainloop()