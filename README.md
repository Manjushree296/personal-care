# 💄 Makeup Product Safety Check System

A web-based system that allows users to upload a photo of a cosmetic product’s ingredients and receive a safety report based on their **skin type**, **age**, and **previous reactions**.

## 🎯 Project Goal

To help users quickly understand whether a product is safe for their **particular skin type** by analyzing the ingredients using OCR and a curated safety dataset.


## 🧰 Tech Stack

| Component           | Technology              |
|---------------------|--------------------------|
| Frontend            | HTML, CSS            |
| Backend             | Python (Flask)           |
| OCR                 | Tesseract OCR            |
| Image Handling      | Pillow (PIL)             |
| Data Handling       | Pandas                   |
| ML/AI               | Rule-based logic (optional ML later) |
| Hosting (optional)  | Render / Vercel / Heroku |

---

## 📦 Features

- 📸 Upload image of product label
- 🔍 OCR scans and extracts ingredients
- 🧴 Classifies ingredients as **Safe / Not Safe / Caution** per skin type
- 👤 User inputs:
  - Skin type (Oily, Dry, Sensitive, etc.)
  - Age
  - Previous reactions
- 📊 Calculates safety rating for uploaded product

---

## 📂 Folder Structure

personal-care/
│
├── app.py
├── ingredient_safety_flags.csv
├── uploads/
│ └── (uploaded images)
├── templates/
│ └── index.html
└── README.md

yaml
Copy
Edit

---

## 🚀 How to Run Locally

### 1. Clone the Repo

git clone https://github.com/Manjushree296/personal-care.git
cd personal-care
2. Create Virtual Environment (optional)

python -m venv makeup_env
source makeup_env/bin/activate  # or `makeup_env\Scripts\activate` on Windows
3. Install Requirements

pip install flask pandas pillow pytesseract
4. Install Tesseract OCR
Download and install from: https://github.com/tesseract-ocr/tesseract

Set the path in app.py:

python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
5. Run the Flask App

python app.py
Open in browser: http://127.0.0.1:5000

📊 Dataset
ingredient_safety_flags.csv contains:
Comedogenic & irritant ratings
Safety flags for: Normal, Oily, Dry, Sensitive, and Combination skin
Columns: ingredient_name, not_safe_for_oily, not_safe_for_dry, etc.
