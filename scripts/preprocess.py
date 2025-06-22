import pandas as pd
import re
import os

RAW_CSV = '../data/processed/telegram_data.csv'
CLEANED_CSV = '../data/processed/cleaned_telegram_data.csv'

def normalize_text(text):
    if pd.isna(text):
        return ""
    # Remove Latin letters and keep Amharic + digits + spaces
    text = str(text)
    text = re.sub(r'[^\u1200-\u137F0-9፡።፣፤፥፦፧፨ብር\s]', '', text)  # Keep Amharic + punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize spaces
    return text

# Load and process
df = pd.read_csv(RAW_CSV)
df['cleaned_message'] = df['Message Text'].apply(normalize_text)

# Save
os.makedirs(os.path.dirname(CLEANED_CSV), exist_ok=True)
df.to_csv(CLEANED_CSV, index=False, encoding='utf-8')
print(f"✅ Preprocessed data saved to: {CLEANED_CSV}")
