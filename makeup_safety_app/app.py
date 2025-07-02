from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import pandas as pd
import os
import sys

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set Tesseract path (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load dataset
csv_path = 'ingredient_data/ingredient_safety_flags.csv'
if not os.path.exists(csv_path):
    sys.exit(f"❌ ERROR: Missing dataset at {csv_path}")

df = pd.read_csv(csv_path)
df['ingredient_name'] = df['ingredient_name'].str.lower().str.strip()

# Safety rating function
def calculate_safety_rating(total, unsafe):
    if total == 0:
        return "Unknown", 0
    ratio = unsafe / total
    if ratio == 0:
        return "All ingredients are safe", 5
    elif ratio <= 0.2:
        return "Minor concerns, mostly safe", 4
    elif ratio <= 0.5:
        return "Some ingredients may not be safe", 3
    elif ratio <= 0.8:
        return "Majority ingredients are unsafe", 2
    else:
        return "Unsafe for this skin type", 1

@app.route('/', methods=['GET', 'POST'])
def index():
    report = ""
    safety_score = ""

    if request.method == 'POST':
        skin_type = request.form.get('skin', '').lower()
        reaction = request.form.get('reaction', '')
        file = request.files.get('image')

        if not file:
            return render_template('index.html', report="⚠️ No image uploaded.", safety_score="")

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # OCR: extract text
        text = pytesseract.image_to_string(Image.open(file_path))
        ingredients_found = [word.strip().lower() for word in text.replace('\n', ',').split(',') if word.strip()]

        result = []
        unsafe_count = 0
        total_checked = 0
        column_name = f"not_safe_for_{skin_type}"

        for ingredient in ingredients_found:
            match = df[df['ingredient_name'] == ingredient]
            if not match.empty:
                is_not_safe = match.iloc[0][column_name]
                total_checked += 1
                if is_not_safe == 1:
                    unsafe_count += 1
                    result.append(f"<b>{ingredient.capitalize()}</b>: ❌ Not Safe")
                else:
                    result.append(f"<b>{ingredient.capitalize()}</b>: ✅ Safe")
            # Skip unknown ingredients

        if not result:
            report = "No recognized ingredients from the dataset were found in the image."
            safety_score = ""
        else:
            report = "<br>".join(result)
            message, score = calculate_safety_rating(total_checked, unsafe_count)
            safety_score = f"<br><br><b>Overall Safety Rating:</b> {message} (Score: {score}/5)"

    return render_template('index.html', report=report, safety_score=safety_score)

if __name__ == '__main__':
    app.run(debug=True)
