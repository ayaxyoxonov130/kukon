from pyrogram import Client, filters
import os

# Telegram hisobingiz uchun ma'lumotlar
api_id = '24154017'  # my.telegram.org saytidan olingan API ID
api_hash = '620063153251e503fbaf4f64209ac052'  # my.telegram.org saytidan olingan API Hash
phone_number = '+998337644819'  # Telefon raqamingiz, masalan: '+123456789'

# Kalit so'zlar faylining nomi
keyword_file = 'keyWord.txt'

# Xabarni yuborish kerak bo'lgan guruh ID'si
target_group_id = -10012345678  # Xabar yuboriladigan guruh ID

# Kalit so'zlar ro'yxatini yuklash funksiyasi
def load_keywords():
    if not os.path.exists(keyword_file):
        return []
    with open(keyword_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

# Yangi kalit so'zlarni faylga qo'shish funksiyasi
def add_keyword(new_keyword):
    with open(keyword_file, 'a', encoding='utf-8') as f:
        f.write(f'{new_keyword}\n')

# Telegram mijozini yaratish (MemoryStorage bilan)
app = Client("my_account", api_id=api_id, api_hash=api_hash, no_updates=True)

# Yangi xabar uchun hodisa
@app.on_message(filters.text | filters.voice)
async def handler(client, message):
    # Xabar matni
    message_text = message.text or ""

    # Kalit so'zlarni yuklash
    keywords = load_keywords()

    # Xabar ovozli bo'lsa (voice message)
    if message.voice:
        # Ovozli xabarni boshqa guruhga yuborish
        await app.send_message(target_group_id, "Yangi ovozli xabar!")
        await app.send_voice(target_group_id, message.voice.file_id)
        print(f"Ovozli xabar yuborildi! Guruh ID: {message.chat.id}")

    # Agar kalit so'zlardan biri xabar matnida mavjud bo'lsa
    elif any(keyword.lower() in message_text.lower() for keyword in keywords):
        # Xabarni qaysi guruhdan kelganini chiqarish (guruh ID)
        group_id = message.chat.id
        print(f"Kalit so'z topildi! Guruh ID: {group_id}")
        
        # Xabarni boshqa guruhga yuborish
        await app.send_message(target_group_id, f"Yangi xabar: {message_text}")

    # Yangi kalit so'z qo'shish buyrug'i (masalan: /addword yangi_soz)
    if message_text.startswith('/addword'):
        # Buyruqdan so'nggi so'zni ajratib olish
        new_word = message_text.split(' ', 1)[1]
        add_keyword(new_word)
        await message.reply_text(f'Yangi kalit soʻz "{new_word}" qoʻshildi!')

# Mijozni ishga tushirish
app.run()
