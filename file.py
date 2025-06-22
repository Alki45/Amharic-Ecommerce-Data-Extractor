import os

# Define the directory structure
project_structure = {
    "amharic-ecommerce-ner": [
        "data/raw",
        "data/processed",
        "labeling",
        "models/fine_tuned_xlm_roberta",
        "notebooks",
        "scripts",
        "vendor_scorecard",
        "outputs"
    ]
}

# Placeholder files to create in each subfolder
placeholder_files = {
    "labeling": ["amharic_ner.conll"],
    "models": ["model_comparison.md"],
    "notebooks": [
        "01_data_ingestion.ipynb",
        "02_preprocessing.ipynb",
        "03_labeling_visual.ipynb",
        "04_finetune_ner.ipynb",
        "05_model_interpretability.ipynb",
        "06_vendor_scorecard.ipynb"
    ],
    "scripts": ["telegram_scraper.py", "preprocess.py"],
    "vendor_scorecard": ["scorecard_results.csv"],
    "outputs": ["metrics_report.json", "interpretability_report.md"]
}

# Main files in the root
root_files = ["README.md", "requirements.txt", "interim_summary.pdf"]

# Create folders
for root, subfolders in project_structure.items():
    os.makedirs(root, exist_ok=True)
    for subfolder in subfolders:
        path = os.path.join(root, subfolder)
        os.makedirs(path, exist_ok=True)

# Create placeholder files
for folder, files in placeholder_files.items():
    folder_path = os.path.join("amharic-ecommerce-ner", folder)
    for file in files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'w') as f:
            f.write(f"# {file}\n")

# Create files at root level
for file in root_files:
    file_path = os.path.join("amharic-ecommerce-ner", file)
    with open(file_path, 'w') as f:
        f.write(f"# {file}\n")

print("✅ Project structure created successfully!")
