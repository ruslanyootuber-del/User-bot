import os
import asyncio
import random
import time
import multiprocessing
import json
from pyrogram import Client
from instagrapi import Client as InstaClient

# --- KONFIGURATSIYA ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("STRING_SESSION")
INSTA_USER = os.environ.get("INSTA_USERNAME")
INSTA_PW = os.environ.get("INSTA_PASSWORD")

# --- TELEGRAM BOT QISMI ---
async def telegram_worker():
    app = Client("my_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    async with app:
        groups = ["@YOSHI_KATTALARY", "@Jupiter_Chat01", "@vodiy_tanishuvlar9", "@ajrashganlar_tanishaaa", "@Ilk_Tanishuv_chati20", "@Tanxo_12_viloyat1", "@a_2005_2004", "@x_2008_2007", "@uchrashuv_ilk", "@glavni66"]
        messages = [
            "Профилимда янги 18+ ведиолар бор утволамиз гоо😍",
            "Profilimdagi yopiq kanalda Shaxatini 18+ vediolari bor o'tvolamiz🍑👈🍌",
            "Profildagi yopiq kanalda 18+ vediolar bor 24-soatdan keyin kanal o'chadi🍌🔥✨",
            "Zerikkanlar bormi? Profildagi yopiq kanalga o'tvoling🍑🍌"
        ]
        replied_users = {group: [] for group in groups}
        print("✅ Telegram Userbot ishga tushdi!")
        while True:
            for group in groups:
                try:
                    current_message = random.choice(messages)
                    recent_messages = []
                    async for msg in app.get_chat_history(group, limit=20):
                        recent_messages.append(msg)
                    valid_messages = [m for m in recent_messages if m.from_user and not m.from_user.is_self and not m.from_user.is_bot and m.from_user.id not in replied_users[group]]
                    if valid_messages:
                        chosen_msg = random.choice(valid_messages)
                        await chosen_msg.reply_text(current_message)
                        replied_users[group].append(chosen_msg.from_user.id)
                        if len(replied_users[group]) > 20: replied_users[group].pop(0)
                    else:
                        await app.send_message(group, current_message)
                except Exception as e: print(f"Telegram xatosi: {e}")
                await asyncio.sleep(5)
            await asyncio.sleep(300)

# --- INSTAGRAM BOT QISMI ---
def start_instagram():
    print("🚀 Instagram Bot ishga tushmoqda...")
    cl = InstaClient()
    processed_reels = [] # Avval yozilgan Reels'larni eslab qolish uchun

    try:
        if os.path.exists("insta_session.json"):
            cl.load_settings("insta_session.json")
            print("✅ Sessiya yuklandi!")
        
        cl.login(INSTA_USER, INSTA_PW)
        
        # DO'STINGIZNING LOGINI (@ belgisiz)
        FRIEND_USERNAME = "uzb_9577" 
        friend_id = cl.user_id_from_username(FRIEND_USERNAME)
        print(f"✅ Do'st topildi (ID: {friend_id})")
        
        insta_comments = [
            "Necha kishi menga like bosadi rekord qo'yamiz goo🔥",
            "Profilimga o'tib patpiska tashab qo'yinglar✊🥲!",
            "Kim ota onasini yaxshi ko'rsa like!👍😸",
            "Layk bosmanglar qaytib ko'rmay reelsni😐"
        ]
        
        while True:
            try:
                # Yangi 5 ta Reels'ni olish
                medias = cl.hashtag_medias_recent("reelsuzb", amount=5)
                
                target_media = None
                for media in medias:
                    if media.id not in processed_reels:
                        target_media = media
                        break
                
                if target_media:
                    # 1. Komment yozish
                    cl.media_comment(target_media.id, random.choice(insta_comments))
                    print(f"💬 Instagram: [{target_media.code}] ga izoh qoldirildi.")
                    
                    # 2. Directga yuborish
                    try:
                        cl.video_share(target_media.id, "", thread_ids=[], user_ids=[friend_id])
                        print(f"✈️ Instagram: {FRIEND_USERNAME} ga Reels yuborildi.")
                    except Exception as de:
                        print(f"⚠️ Direct xatosi: {de}")
                    
                    # IDni eslab qolish
                    processed_reels.append(target_media.id)
                    if len(processed_reels) > 100: processed_reels.pop(0)

                else:
                    print("🔄 Yangi Reels topilmadi, keyingi safar tekshiramiz.")

                # ANIQ 10 DAQIQA KUTISH (600 soniya)
                print("💤 10 daqiqa tanaffus...")
                time.sleep(600)

            except Exception as e:
                print(f"⚠️ Instagram sikl xatosi: {e}")
                time.sleep(60) # Xato bo'lsa 1 daqiqa kutib qayta urinish
                
    except Exception as e:
        print(f"❌ Instagram Login xatosi: {e}")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=lambda: asyncio.run(telegram_worker()))
    p2 = multiprocessing.Process(target=start_instagram)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
