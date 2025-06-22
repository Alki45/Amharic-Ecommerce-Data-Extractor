import pandas as pd

# Allowed NER labels
LABELS = ['B-Product', 'I-Product', 'B-LOC', 'I-LOC', 'B-PRICE', 'I-PRICE', 'O']

def tokenize(text):
    # Basic whitespace tokenizer; can be enhanced for Amharic
    return text.strip().split()

def display_label_options():
    print("\nNER Label Options:")
    for idx, label in enumerate(LABELS, 1):
        print(f"{idx}. {label}")

def label_message(message):
    tokens = tokenize(message)
    labeled_tokens = []

    print("\n🔤 Label tokens for the message:\n", message)
    display_label_options()

    for token in tokens:
        while True:
            try:
                label_idx = input(f"\nToken: '{token}'\nChoose label [1-{len(LABELS)}]: ").strip()
                if not label_idx.isdigit():
                    print("❌ Please enter a number.")
                    continue

                label_idx = int(label_idx)
                if 1 <= label_idx <= len(LABELS):
                    label = LABELS[label_idx - 1]
                    labeled_tokens.append((token, label))
                    break
                else:
                    print("❌ Number out of range.")
            except Exception as e:
                print(f"⚠️ Error: {e}")

    return labeled_tokens

def save_conll(labeled_messages, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for message in labeled_messages:
            for token, label in message:
                f.write(f"{token} {label}\n")
            f.write("\n")

def main():
    # Load your cleaned dataset
    df = pd.read_csv('../data/processed/telegram_data_cleaned.csv', encoding='utf-8')
    messages = df['cleaned_message'].dropna().tolist()

    print(f"\n📊 Total messages available for labeling: {len(messages)}")
    labeled_messages = []
    max_label = 50

    for i, msg in enumerate(messages[:max_label]):
        print(f"\n📝 Labeling message {i + 1}/{max_label}")
        labeled = label_message(msg)
        labeled_messages.append(labeled)

    output_path = '../labeling/labeled_subset.conll'
    save_conll(labeled_messages, output_path)
    print(f"\n✅ Labeling completed. Saved to {output_path}")

if __name__ == "__main__":
    main()
