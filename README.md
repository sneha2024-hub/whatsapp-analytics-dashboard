# 📊 WhatsApp Analytics Dashboard

A clean and interactive WhatsApp Conversation Analytics Dashboard built using Python, Streamlit, Pandas, Matplotlib, and Seaborn.
This tool transforms raw exported WhatsApp chats into meaningful insights such as activity patterns, message trends, heatmaps, emoji usage, and conversation behaviour analytics.

Perfect for data analysis, portfolio projects, and learning real-world text processing.

## 🚀 Features

### 🔹 Top-Level Statistics

Total messages

Total words

Media shared

Links shared

### 🔹 Advanced Insights

Average message length

Night-time chat activity (10 PM–3 AM)

Most active day of the week

Hourly activity patterns

### 🔹 Timelines

Daily message timeline

Monthly message timeline

### 🔹 Activity Visuals

Weekly activity heatmap

Busiest days

Busiest months

### 🔹 Text Analysis

Word Cloud

Most frequently used words

### 🔹 Emoji Breakdown

Emoji frequency table

Pie chart visualization

## 🧠 Tech Stack

Python

Streamlit

Pandas

Matplotlib

Seaborn

WordCloud

URLExtract

Emoji

## 📦 Installation

### 1️⃣ Clone the repo
git clone https://github.com/your-username/whatsapp-analytics-dashboard.git

cd whatsapp-analytics-dashboard

### 2️⃣ Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

### 3️⃣ Install dependencies
pip install -r requirements.txt

### ▶️ How to Run
streamlit run app.py


The app will open at:

http://localhost:8501

## 📁 How to Export WhatsApp Chat

On WhatsApp:

Open a chat

Tap 3 dots → More → Export Chat

Choose Without Media

Upload the .txt file in the dashboard sidebar

Example input format:

[12/05/24, 10:45 pm] Sneha: Hey, what's up?
[12/05/24, 10:46 pm] Buddy: Working 😄

## ⚠️ Limitations

Works only with WhatsApp .txt exports

Large chats (1L+ messages) may load slowly

Media messages (<Media omitted>) cannot be displayed

## 🚀 Future Enhancements

Sentiment analysis

Multi-chat comparison

Conversation summarization

PDF/HTML report export

User-interaction graph

## 👩‍💻 Author

### Sneha H
### Data Analyst 
### Bengaluru, India
