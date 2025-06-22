import pandas as pd

# Allowed NER labels for manual labeling
LABELS = ['B-Product', 'I-Product', 'B-LOC', 'I-LOC', 'B-PRICE', 'I-PRICE', 'O']

def tokenize(text):
    # Basic whitespace tokenizer; can be enhanced for Amharic language specifics
    return text.strip().split()

def label_message(message):
    tokens = tokenize(message)
    labeled_tokens = []

    print("\nLabel tokens for the message:\n", message)
    print("Use labels:", ', '.join(LABELS))
    print("Type label and press Enter for each token.")

    for token in tokens:
        while True:
            label = input(f"Token: '{token}'\nLabel: ").strip()
            if label in LABELS:
                labeled_tokens.append((token, label))
                break
            else:
                print("Invalid label. Try again.")

    return labeled_tokens

def save_conll(labeled_messages, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for message in labeled_messages:
            for token, label in message:
                f.write(f"{token} {label}\n")
            f.write("\n")  # Blank line between messages as per CoNLL format

def main():
    # Load your cleaned CSV file; update the path if needed
    df = pd.read_csv('../data/processed/telegram_data_cleaned.csv', encoding='utf-8')

    # Filter to keep only rows with non-empty cleaned_message
    messages = df['cleaned_message'].dropna().tolist()

    print(f"Total messages available for labeling: {len(messages)}")

    labeled_messages = []
    max_label = 50  # Label up to 50 messages max
    count = 0

    for msg in messages:
        count += 1
        print(f"\nLabeling message {count}/{max_label}")
        labeled = label_message(msg)
        labeled_messages.append(labeled)

        if count >= max_label:
            break

    save_conll(labeled_messages, 'labeled_subset.conll')
    print("\n✅ Labeling completed. Data saved to labeled_subset.conll")

if __name__ == "__main__":
    main()
