import os
import zipfile
import telebot
from PIL import Image, ImageDraw
import easyocr
import requests

# Bot API Token yahan dalein (BotFather wala Token)
BOT_TOKEN = 8920265890:AAEVjYmbKS9V9BbFtOfLjYj6_3ZXzwun59k
bot = telebot.TeleBot(BOT_TOKEN)

# EasyOCR Reader setup (Japanese & English support)
reader = easyocr.Reader(['ja', 'en'])

def translate_text(text, target_lang='hi'):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={text}"
        res = requests.get(url).json()
        return res[0][0][0]
    except:
        return text

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste! Mujhe Manga ZIP file bhejein, main translate kar dunga.")

@bot.message_handler(content_types=['document'])
def process_zip(message):
    if not message.document.file_name.endswith('.zip'):
        bot.reply_to(message, "Kripya ZIP file hi bhejein!")
        return

    bot.reply_to(message, "File mil gayi hai! OCR aur Translation shuru ho raha hai...")
    
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    
    input_zip = "input.zip"
    with open(input_zip, 'wb') as f:
        f.write(downloaded)
        
    extract_dir = "extracted"
    output_dir = "processed"
    os.makedirs(extract_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    with zipfile.ZipFile(input_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
    for filename in os.listdir(extract_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            img_path = os.path.join(extract_dir, filename)
            img = Image.open(img_path).convert("RGB")
            draw = ImageDraw.Draw(img)
            
            # Text detection
            results = reader.readtext(img_path)
            for (bbox, text, prob) in results:
                if prob > 0.3:
                    # White box overlay over old text
                    (top_left, top_right, bottom_right, bottom_left) = bbox
                    draw.rectangle([top_left[0], top_left[1], bottom_right[0], bottom_right[1]], fill="white")
                    
                    # Translation
                    trans_text = translate_text(text, 'hi')
                    
                    # New translated text
                    draw.text((top_left[0], top_left[1]), trans_text, fill="black")
            
            img.save(os.path.join(output_dir, filename))
            
    # Zip output
    out_zip_path = "translated_manga.zip"
    with zipfile.ZipFile(out_zip_path, 'w') as zip_out:
        for root, _, files in os.walk(output_dir):
            for file in files:
                zip_out.write(os.path.join(root, file), file)
                
    with open(out_zip_path, 'rb') as f:
        bot.send_document(message.chat.id, f)

bot.polling()
