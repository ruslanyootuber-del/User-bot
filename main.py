import os
import asyncio
import random
from pyrogram import Client, filters

# Environment variables orqali ma'lumotlarni olish
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("STRING_SESSION")

# Client'ni global qilib ochamiz (Event va Loop uchun)
app = Client(
    "my_account", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=SESSION_STRING
)

# ==========================================
# 1-QISM: GHOST MODE VA ANTI-DELETE FUNKSIYALARI
# ==========================================
msg_cache = {}

# Ghost Mode: Pyrogram sukut bo'yicha xabarlarni o'qilgan deb belgilamaydi.
# Shuning uchun lichkaga kelgan xabarlarni faqat xotiraga yozamiz.
@app.on_message(filters.private & ~filters.me, group=1)
async def cache_messages(client, message):
    text = message.text or message.caption or "[Media/Sticker]"
    sender_name = message.from_user.first_name if message.from_user else "Noma'lum"
    
    msg_cache[message.id] = {
        "text": text,
        "sender": sender_name
    }
    # Xotira to'lib ketmasligi uchun 500 ta xabardan eskisini o'chiramiz
    if len(msg_cache) > 500:
        msg_cache.pop(list(msg_cache.keys())[0])

@app.on_deleted_messages(filters.private)
async def detect_delete(client, messages):
    for msg in messages:
        if msg.id in msg_cache:
            deleted_info = msg_cache[msg.id]
            text = (f"🗑 **Xabar o'chirildi!**\n\n"
                    f"👤 **Kimdan:** {deleted_info['sender']}\n"
                    f"💬 **Xabar:** {deleted_info['text']}")
            
            # Saqlangan xabarlarga (Saved Messages) yuborish
            await client.send_message("me", text)
            del msg_cache[msg.id]


# ==========================================
# 2-QISM: SIZNING ASOSIY GURUHLARGA YOZISH KODINGIZ
# ==========================================
async def group_sender_loop():
    # Guruhlar ro'yxati
    groups = [
        "@w_2008_2009_2007", "@tungi_opalarn", "@gulimsanu_9", "@silbek_1110", "@real_qizlarbore", "@tanishuvlar_ovozli_chat_gruppa", "@ajrashganlar_tanishaaa", "@Samarqand_chat_Qashqadaryo", "@TANSHUVLAR_QADIRDONLARIM"
    ]
    
    # 3 xil matnli xabarlar ro'yxati
    messages = [
        """Профилимда янги 18+ ведиолар бор утволамиз гоо😍🚷""",
        """Profilimdagi yopiq kanalda Shaxatini 18+ vediolari bor o'tvolamiz🍑👈🍌""",
        """Profildagi yopiq kanalda 18+ vediolar bor 24-soatdan keyin kanal o'chadi🍌🔥✨""",
        "Zerikkanlar bormi? Profildagi yopiq kanalga o'tvoling🍑🍌"
    ]
    
    # Javob berilgan odamlar xotirasi
    replied_users = {group: [] for group in groups}
    
    print("Bot ishga tushdi. Guruhlarga xabar, Anti-Delete va Ghost Mode faol! ✅")
    
    while True:
        for group in groups:
            try:
                current_message = random.choice(messages)
                recent_messages = []
                async for msg in app.get_chat_history(group, limit=30):
                    recent_messages.append(msg)
                
                valid_messages = [
                    m for m in recent_messages 
                    if m.from_user and not m.from_user.is_self and not m.from_user.is_bot 
                    and m.from_user.id not in replied_users[group]
                ]
                
                if valid_messages:
                    chosen_msg = random.choice(valid_messages)
                    await chosen_msg.reply_text(current_message)
                    print(f"[{group}] - {chosen_msg.from_user.first_name} ga REPLY yuborildi.")
                    
                    replied_users[group].append(chosen_msg.from_user.id)
                    if len(replied_users[group]) > 20:
                        replied_users[group].pop(0)
                else:
                    await app.send_message(group, current_message)
                    print(f"[{group}] - Yangi odam yo'q, ODDIY xabar ketdi.")
                
            except Exception as e:
                print(f"Xatolik yuz berdi ({group}): {e}")
            
            await asyncio.sleep(3)
        
        print("Sikl tugadi. 6 daqiqa (360 sek) tanaffus boshlandi... 💤")
        await asyncio.sleep(360)


# ==========================================
# 3-QISM: IKKALA FUNKSIYANI BIRGA ISHGA TUSHIRISH
# ==========================================
async def start_all():
    # Client'ni ishga tushiramiz (eventlar eshitishni boshlaydi)
    await app.start()
    try:
        # Asosiy guruhlarga yozish siklini uzluksiz ishlatamiz
        await group_sender_loop()
    finally:
        await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
