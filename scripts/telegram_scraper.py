from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
api_id = int(os.getenv('TG_API_ID'))
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')  # Optional: used for login if needed

# CSV file containing Telegram channel usernames
CHANNEL_CSV = '../data/processed/channels_to_crawl.xlsx'   # This should contain @channel_username in each row
OUTPUT_CSV = '../data/processed/telegram_data.csv'
MEDIA_DIR = '../data/processed/photos'

# Function to read channel usernames from a CSV
def load_channel_usernames(filename):
    channels = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # skip empty lines
                channels.append(row[0].strip())
    return channels

# Scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        async for message in client.iter_messages(entity, limit=10000):
            media_path = None
            if message.media and hasattr(message.media, 'photo'):
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)
            
            writer.writerow([
                channel_title,
                channel_username,
                message.id,
                message.message,
                message.date,
                media_path
            ])
    except Exception as e:
        print(f"Failed to scrape {channel_username}: {e}")

# Main execution
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start()
    
    os.makedirs(MEDIA_DIR, exist_ok=True)

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

        # Load channel usernames from CSV
        channels = load_channel_usernames(CHANNEL_CSV)
        for channel in channels:
            print(f"Scraping {channel}...")
            await scrape_channel(client, channel, writer, MEDIA_DIR)
            print(f"Finished scraping {channel}")

with client:
    client.loop.run_until_complete(main())
print("✅ Scraping completed successfully! Data saved to", OUTPUT_CSV)