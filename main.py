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
        # Sessiyani xavfsiz yuklash yoki yaroqsiz bo'lsa yangilash
        if os.path.exists("insta_session.json"):
            try:
                cl.load_settings("insta_session.json")
                cl.login(INSTA_USER, INSTA_PW)
                print("✅ Eski sessiya orqali ulandi!")
            except Exception:
                os.remove("insta_session.json")
                print("🗑 Yaroqsiz sessiya o'chirildi, yangidan kiramiz...")
                cl.login(INSTA_USER, INSTA_PW)
                cl.dump_settings("insta_session.json")
                print("✅ Yangi sessiya yaratildi!")
        else:
            cl.login(INSTA_USER, INSTA_PW)
            cl.dump_settings("insta_session.json")
            print("✅ Yangi sessiya yaratildi!")
        
        insta_comments = [
            "@cristiano menga obuna bo‘lmaguncha to‘xtamayman! 🔥 1-kun. Maqsad aniq! 🚀",
            "CR7 FOLLOW ME! 🐐🇵🇹 Obuna bo‘lmaguncha komentariya yozaman!🐐⚽️@cristiano",
            "@cristiano Ronaldo menga obuna bo’lmaguncha taslim bo‘lmayman🚀✊",
            "@cristiano Ronaldoni taslim qilaman! 😤 Menga obuna bo‘lmaguncha har kuni komentariya yozaman!⚽️🐐"
        ]
        
        # O'zbek auditoriyasini topish uchun xeshteglar bazasi
        hashtags = [
            "reelsuzb", "uzbekistan", "toshkent", "uzb", "uzbek", "ronaldo", "cristiano", "cr7", 
            "top", "yumor", "krinjhub", "rek", "rekkachiq", "рек", "rekkachiqiplos", "rekda", 
            "topsxema", "instagram", "toptags", "abdullohdomla", "maruzalar", "shukurullohdomla", 
            "chingiz", "chingizgolos", "tiktok", "mafia", "qoriaka", "city", "abdullohqoriaka", 
            "mem", "uzbekmem", "yagir", "yumor", "aslamboi", "pubg", "70", "75", "qashqadaryo", 
            "yakkabog", "nukus", "qora yumor", "oq yumor", "epshteyin", "insta", "uzbekcore"
        ]

        while True:
            try:
                # Har siklda random xeshteg tanlaymiz
                current_hashtag = random.choice(hashtags)
                print(f"🔍 #{current_hashtag} bo'yicha Reels qidirilmoqda...")
                
                # Eng yangi Reels'larni kengroq miqyosda olish
                medias = cl.hashtag_medias_recent(current_hashtag, amount=15)
                
                # Agar tag bo'yicha umuman video chiqmasa (kamdan-kam hollarda), boshqa tag tanlash
                if not medias or len(medias) < 2:
                    print(f"⚠️ #{current_hashtag} da yetarli video topilmadi, boshqa tagga o'tamiz...")
                    continue
                
                # Oldin komment yozilmaganlarini saralab olish
                fresh_medias = [m for m in medias if m.id not in processed_reels]
                targets = []

                if len(fresh_medias) >= 2:
                    # Yangilari yetarli bo'lsa, o'shalardan 2 ta olamiz
                    targets = random.sample(fresh_medias, 2)
                else:
                    # YOKI to'xtab qolmaslik uchun boridan random qilib olamiz!
                    print("🔄 Yangi Reels kam ekan, borlaridan random qilib olamiz (To'xtash yo'q!).")
                    needed = 2 - len(fresh_medias)
                    old_medias = [m for m in medias if m not in fresh_medias]
                    fallback = random.sample(old_medias, min(needed, len(old_medias)))
                    targets = fresh_medias + fallback

                    # Mabodo baribir 2 ta chiqmasa, medias ichidan qaysi bo'lsa shuni olamiz
                    if len(targets) < 2:
                        targets = random.sample(medias, 2)
                
                # Komment yozish (Aniq 2 ta!)
                for idx, target_media in enumerate(targets):
                    cl.media_comment(target_media.id, random.choice(insta_comments))
                    print(f"💬 Instagram: [{target_media.code}] ga izoh qoldirildi (#{current_hashtag}).")
                    
                    if target_media.id not in processed_reels:
                        processed_reels.append(target_media.id)
                    
                    # Xotirani tozalab borish
                    if len(processed_reels) > 200: 
                        processed_reels.pop(0) 
                    
                    # Birinchisiga yozgach, ikkinchisiga o'tishdan oldin 3 soniya kutish
                    if idx == 0:
                        time.sleep(3)

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
