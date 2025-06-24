import pandas as pd
from io import StringIO
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

# === 1. DATA LOADING ===
raw_data = '''Branch,Percentile,Category
Petroleum Engineering,58.65,ST
Chemical Engineering,60.09,ST
Civil Engineering,63.74,ST
Mechanical Engineering,64,ST
Building and Construction Technology,64.71,OBC
Electronics and Electrical Engineering,66.82,ST
Building and Construction Technology,67.33,OBC
Mining Engineering,67.54,SC
Building and Construction Technology,70.59,OBC
Petroleum Engineering,71,SC
Electronics and Computer,71.33,SC
Electrical Engineering,71.66,GENERAL
Building and Construction Technology,72.18,OBC
Mechanical Engineering,73,SC
Electronics and Communication,73,SC
Building and Construction Technology,73.48,GENERAL
Electronics and Electrical Engineering,73.89,SC
Mechanical Engineering,74,SC
Building and Construction Technology,74.66,OBC
Building and Construction Technology,74.673005,GENERAL
Building and Construction Technology,75.15,OBC
Building and Construction Technology,75.55,GENERAL
Civil Engineering,75.99,SC
Electronics and Electrical Engineering,76.42,OBC
Building and Construction Technology,76.54,GENERAL
Petroleum Engineering,76.75,OBC
Building and Construction Technology,76.89,GENERAL
Petroleum Engineering,77,GENERAL
Civil Engineering,77.18,SC
Mechanical Engineering,77.47,ST
Electronics and Electrical Engineering,77.47,ST
Electronics and Electrical Engineering,77.64,EWS
Information Technology,78,SC
Electronics and Communication,78,SC
Electronics and Electrical Engineering,78.22,GENERAL
Civil Engineering,78.97,EWS
Electronics and Electrical Engineering,79.08,OBC
Building and Construction Technology,79.24,OBC
Civil Engineering,79.24,ST
Petroleum Engineering,79.29,OBC
Mining Engineering,79.86,SC
Civil Engineering,79.86,SC
Electronics and Electrical Engineering,80,OBC
Information Technology,80.09,SC
Building and Construction Technology,80.27,OBC
Electronics and Communication,80.72,SC
Petroleum Engineering,80.93,OBC
Electrical Engineering,80.96,SC
Electronics and Electrical Engineering,81.05,OBC
Civil Engineering,81.56,SC
Artificial Intelligence and Data Science,81.87,ST
Civil Engineering,81.99,ST
Civil Engineering,82.03,OBC
Mechanical Engineering,82.3,SC
Civil Engineering,82.33,ST
Production and Industrial,82.6,GENERAL
Civil Engineering,82.95,EWS
Computer Science,82.97,SC
Petroleum Engineering,83,EWS
Production and Industrial,83.27,OBC
Civil Engineering,83.79,GENERAL
Mechanical Engineering,83.88,OBC
Civil Engineering,83.89,SC
Mechanical Engineering,83.96,EWS
Petroleum Engineering,84.27,EWS
Computer Science,84.33,SC
Production and Industrial,84.44,GENERAL
Civil Engineering,84.52,OBC
Mechanical Engineering,84.6,OBC
Mechanical Engineering,84.77,OBC
Artificial Intelligence and Data Science,84.85,OBC
Production and Industrial,85,OBC
Electronics and Computer,85,SC
Electronics and Communication,85,SC
Civil Engineering,85.04,OBC
Electrical Engineering,85.5,ST
Civil Engineering,85.53,SC
Electronics and Communication,85.57,OBC
Building and Construction Technology,85.73,GENERAL
Civil Engineering,85.8,SC
Mechanical Engineering,86,EWS
Civil Engineering,86,OBC
Electronics and Electrical Engineering,86,OBC
Petroleum Engineering,86.16,EWS
Chemical Engineering,86.26,GENERAL
Petroleum Engineering,86.5,OBC
Chemical Engineering,86.82,GENERAL
Electronics and Electrical Engineering,86.99,OBC
Mechanical Engineering,87,OBC
Computer Science,87,SC
Civil Engineering,87.239,OBC
Petroleum Engineering,87.24,GENERAL
Electrical Engineering,87.24,OBC
Petroleum Engineering,87.32,OBC
Mechanical Engineering,87.5,OBC
Electronics and Electrical Engineering,87.56,GENERAL
Civil Engineering,87.67,OBC
Computer Science,87.91,SC
Mechanical Engineering,87.98,EWS
Electronics and Communication,88.02,OBC
Electrical Engineering,88.033,OBC
Civil Engineering,88.08,OBC
Mining Engineering,88.39,EWS
Petroleum Engineering,88.78,OBC
Petroleum Engineering,88.96,EWS
Electronics and Electrical Engineering,88.99,EWS
Civil Engineering,89,EWS
Civil Engineering,89,OBC
Electronics and Electrical Engineering,89,OBC
Chemical Engineering,89.33,EWS
Mechanical Engineering,89.33,OBC
Mining Engineering,89.39,OBC
Mechanical Engineering,89.4,EWS
Computer Science,89.44,SC
Petroleum Engineering,89.45,GENERAL
Electronics and Electrical Engineering,89.68,EWS
Mechanical Engineering,89.705,OBC
Artificial Intelligence and Data Science,89.998,SC
Electronics and Electrical Engineering,90,GENERAL
Electronics and Electrical Engineering,90.08,OBC
Electronics and Electrical Engineering,90.16,GENERAL
Electronics and Computer,90.2,OBC
Civil Engineering,90.23,OBC
Mechanical Engineering,90.24,OBC
Mechanical Engineering,90.24,OBC
Petroleum Engineering,90.25,OBC
Mechanical Engineering,90.3,OBC
Electrical Engineering,90.36,OBC
Petroleum Engineering,90.54,OBC
Chemical Engineering,90.7,EWS
Electronics and Computer,90.83,OBC
Electronics and Computer,90.87,OBC
Mechanical Engineering,90.89,GENERAL
Mining Engineering,90.91,OBC
Electrical Engineering,90.9617,OBC
Electronics and Computer,90.99,OBC
Civil Engineering,91,GENERAL
Electronics and Electrical Engineering,91,GENERAL
Electrical Engineering,91,OBC
Mining Engineering,91,OBC
Electronics and Computer,91.05,OBC
Electronics and Computer,91.06,EWS
Electronics and Computer,91.07,OBC
Civil Engineering,91.23,EWS
Electronics and Communication,91.23,OBC
Electrical Engineering,91.28,OBC
Civil Engineering,91.47,OBC
Mining Engineering,91.47,OBC
Electrical Engineering,91.5,EWS
Electrical Engineering,91.53,OBC
Mining Engineering,91.62,EWS
Electronics and Computer,91.63,OBC
Petroleum Engineering,91.64,OBC
Electrical Engineering,91.73,EWS
Electronics and Computer,91.8,EWS
Mining Engineering,91.83,EWS
Electronics and Computer,91.97,EWS
Petroleum Engineering,92.03,OBC
Electrical Engineering,92.16,OBC
Electronics and Communication,92.1615,EWS
Electrical Engineering,92.21,EWS
Civil Engineering,92.21,OBC
Chemical Engineering,92.23,OBC
Electronics and Computer,92.24,EWS
Mechanical Engineering,92.29,OBC
Electronics and Communication,92.31,EWS
Chemical Engineering,92.44,OBC
Electronics and Communication,92.45,GENERAL
Electrical Engineering,92.47,OBC
Electronics and Communication,92.58,EWS
Electrical Engineering,92.61,OBC
Electronics and Communication,92.63,EWS
Electronics and Computer,92.63,EWS
Electronics and Computer,92.65,GENERAL
Civil Engineering,92.66,GENERAL
Electronics and Computer,92.8,GENERAL
Electronics and Communication,92.89,GENERAL
Civil Engineering,92.92,OBC
Mechanical Engineering,92.97,OBC
Electronics and Computer,92.979,OBC
Electronics and Computer,92.98,GENERAL
Electronics and Computer,92.98,OBC
Mining Engineering,92.99,OBC
Electronics and Computer,93,GENERAL
Electronics and Computer,93.01,GENERAL
Electrical Engineering,93.22,OBC
Electrical Engineering,93.24,GENERAL
Electronics and Communication,93.26,EWS
Electronics and Computer,93.32,OBC
Mechanical Engineering,93.37,OBC
Artificial Intelligence and Data Science,93.44,EWS
Electrical Engineering,93.49,OBC
Electrical Engineering,93.56,OBC
Mining Engineering,93.6,GENERAL
Information Technology,93.64,OBC
Civil Engineering,93.65,OBC
Artificial Intelligence and Data Science,93.66,EWS
Mining Engineering,93.67,OBC
Mining Engineering,93.69,GENERAL
Civil Engineering,93.71,OBC
Artificial Intelligence and Data Science,93.8,GENERAL
Artificial Intelligence and Data Science,93.8,EWS
Mechanical Engineering,93.89,GENERAL
Civil Engineering,93.94,OBC
Information Technology,93.96,OBC
Information Technology,93.97,GENERAL
Information Technology,93.97,GENERAL
Civil Engineering,94,OBC
Artificial Intelligence and Data Science,94.05,OBC
Electronics and Communication,94.09,GENERAL
Artificial Intelligence and Data Science,94.14,GENERAL
Mining Engineering,94.19,OBC
Information Technology,94.23,OBC
Artificial Intelligence and Data Science,94.26,EWS
Electronics and Communication,94.32,GENERAL
Artificial Intelligence and Data Science,94.33,EWS
Mechanical Engineering,94.34,EWS
Artificial Intelligence and Data Science,94.39,OBC
Information Technology,94.4,GENERAL
Artificial Intelligence and Data Science,94.4,OBC
Information Technology,94.45,GENERAL
Information Technology,94.53,OBC
Information Technology,94.72,GENERAL
Information Technology,94.73,OBC
Civil Engineering,94.74,OBC
Information Technology,94.78,GENERAL
Artificial Intelligence and Data Science,94.79,GENERAL
Civil Engineering,94.8041507,OBC
Mining Engineering,94.85,OBC
Information Technology,94.86,EWS
Computer Science,94.87,OBC
Computer Science,94.87,ST
Information Technology,94.95,EWS
Mechanical Engineering,94.95,OBC
Artificial Intelligence and Data Science,94.98,OBC
Artificial Intelligence and Data Science,94.99,EWS
Information Technology,94.99,OBC
Electronics and Communication,95,EWS
Information Technology,95,EWS
Computer Science,95,OBC
Artificial Intelligence and Data Science,95.01,EWS
Petroleum Engineering,95.02,GENERAL
Computer Science,95.02,OBC
Information Technology,95.03,GENERAL
Artificial Intelligence and Data Science,95.05,OBC
Civil Engineering,95.05,OBC
Mining Engineering,95.07,OBC
Information Technology,95.17,OBC
Artificial Intelligence and Data Science,95.25,GENERAL
Artificial Intelligence and Data Science,95.32,OBC
Computer Science,95.37,OTHER
Computer Science,95.39,GENERAL
Artificial Intelligence and Data Science,95.47,OBC
Information Technology,95.49,GENERAL
Artificial Intelligence and Data Science,95.52,OBC
Information Technology,95.53,OBC
Computer Science,95.64,OBC
Electronics and Communication,95.65,OBC
Information Technology,95.67,OBC
Electronics and Communication,95.75,EWS
Computer Science,95.78,OBC
Computer Science,95.8,OBC
Computer Science,95.81,GENERAL
Computer Science,95.83,GENERAL
Electrical Engineering,95.89,OBC
Computer Science,95.91,EWS
Computer Science,95.97,OBC
Computer Science,95.97,OBC
Information Technology,96,OBC
Computer Science,96.05,EWS
Computer Science,96.13,GENERAL
Computer Science,96.2,OBC
Computer Science,96.27,OBC
Computer Science,96.29,GENERAL
Artificial Intelligence and Data Science,96.54,GENERAL
Computer Science,96.54,GENERAL
Computer Science,96.56,GENERAL
Computer Science,96.65,OBC
Electronics and Communication,96.7,EWS
Computer Science,96.71,EWS
Artificial Intelligence and Data Science,96.73,GENERAL
Computer Science,96.86,EWS
Computer Science,96.98,GENERAL
Computer Science,97.02,EWS
Electronics and Communication,97.04,GENERAL
Computer Science,97.08,GENERAL
Computer Science,97.65,ST
Computer Science,97.66,GENERAL
Artificial Intelligence and Data Science,98.2,SC
Mechanical Engineering,89.99,OBC
'''

df = pd.read_csv(StringIO(raw_data))
df['Category'] = df['Category'].astype(str).str.strip().str.upper()
df['Branch'] = df['Branch'].astype(str).str.strip()
df['Percentile'] = pd.to_numeric(df['Percentile'], errors='coerce')

def suggest_branches(percentile, category):
    category = category.strip().upper()
    filtered = df[
        (df['Percentile'] <= percentile) &
        (df['Category'].str.strip().str.upper().str.startswith(category))
    ]
    branches = filtered['Branch'].unique()
    if len(branches) == 0:
        return "Koi branch nahi mili aapke percentile aur category ke hisaab se."
    return "Aapko mil sakti hain MBMU me:\n" + "\n".join(branches)

# === 3. TELEGRAM BOT HANDLER ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    import re
    match = re.search(r'([0-9]{2,}\.?[0-9]*)\s*(percentile|%tile|percent|%)?\s*([a-z]+)', text)
    if match:
        percentile = float(match.group(1))
        category = match.group(3)
        reply = suggest_branches(percentile, category)
    else:
        only_number = re.match(r'^[0-9]{2,}(\.[0-9]*)?$', text.strip())
        if only_number:
            reply = "Kripya apni category bhi likhein (jaise: 85 OBC, 90 SC, 92 General, etc.)"
        else:
            reply = "Kripya apna percentile aur category is format me bheje: '85 OBC percentile' ya '90 %tile SC'"
    await update.message.reply_text(reply)

# === 4. MAIN BOT RUNNER ===
if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("Error: Please set the TELEGRAM_BOT_TOKEN environment variable.")
        exit(1)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling() 