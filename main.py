import os
import asyncio
import random
from pyrogram import Client

# Environment variables orqali ma'lumotlarni olish
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("STRING_SESSION")

async def main():
    app = Client(
        "my_account", 
        api_id=API_ID, 
        api_hash=API_HASH, 
        session_string=SESSION_STRING
    )
    
    async with app:
        # Guruhlar ro'yxati
        groups = [
            "@YOSHI_KATTALARY", "@vodiy_tanishuvlar9", 
            "@ajrashganlar_tanishaaa", "@Ilk_Tanishuv_chati20", 
            "@Tanxo_12_viloyat1", "@x_2008_2007"
        ]
        
        # 3 xil matnli xabarlar ro'yxati
        messages = [
            """Salom, jonim... profilimga bir kiring... 👈🌹😻
Yopiq kanalda siz kutgan eng yangi videolarim bor... 🍒🔥""",

            """𝒮𝒶𝓁ℴ𝓂, 𝓅𝓇ℴ𝒻𝒾𝓁𝒾𝓂ℊ𝒶 𝓀𝒾𝓇𝒾𝒷 𝓀ℴ'𝓇𝒾𝓃ℊ... 🍌🫦✨
𝒴ℴ𝓅𝒾𝓆 𝓀𝒶𝓃𝒶𝓁 bomb 𝒻𝒶𝓆𝒶𝓉 𝓈𝒾𝓏 𝓊𝒸_𝒽𝓊𝓃 𝓎𝒶𝓃ℊ𝒾 𝓋𝒾𝒹𝑒ℴ𝓁𝒶𝓇_𝒾𝓂 𝒷ℴ𝓇... 🍑👈❤️‍🔥""",

            """𝓢𝓪𝓵𝓸𝓶, 𝓳𝓸𝓷𝓲𝓶... 𝓹𝓻𝓸𝓯𝓲𝓵𝓲𝓶𝓰𝓪 𝓴𝓲𝓻𝓲𝓫 𝓴𝓸'𝓻𝓲𝓷𝓰 🙈🍌🌹
𝓨𝓸𝓹𝓲𝓿 𝓴𝓪𝓷𝓪𝓵𝓭𝓪 𝔂𝓪𝓷𝓰𝓲, 𝓮𝓱𝓽𝓲𝓻𝓸𝓼𝓵𝓲 𝓿𝓲𝓭𝓮𝓸𝓵𝓪𝓻𝓲𝓶 𝓫𝓸𝓻, 𝓼𝓲𝔃𝓷𝓲 𝓴𝓾𝓽𝔂𝓪𝓹𝓶𝓪𝓷... 🍓🍌🔥✨""",

            "Zerikkanlar bormi? Gaplashamiz! Profildagi guruxga o'ting🍑🍌🫦"
        ]
        
        # Javob berilgan odamlar xotirasi
        replied_users = {group: [] for group in groups}
        
        print("Bot ishga tushdi. Random xabarlar va 10 daqiqalik tanaffus faol! ✅")
        
        while True:
            for group in groups:
                try:
                    # 1. Ro'yxatdan tasodifiy bitta matnni tanlab olamiz
                    current_message = random.choice(messages)
                    
                    # 2. Oxirgi xabarlarni tekshirish
                    recent_messages = []
                    async for msg in app.get_chat_history(group, limit=30):
                        recent_messages.append(msg)
                    
                    # 3. Yangi foydalanuvchini qidirish
                    valid_messages = [
                        m for m in recent_messages 
                        if m.from_user and not m.from_user.is_self and not m.from_user.is_bot 
                        and m.from_user.id not in replied_users[group]
                    ]
                    
                    if valid_messages:
                        # AGAR YANGI ODAM TOPILSA - REPLY QILAMIZ
                        chosen_msg = random.choice(valid_messages)
                        await chosen_msg.reply_text(current_message)
                        print(f"[{group}] - {chosen_msg.from_user.first_name} ga REPLY yuborildi.")
                        
                        # Xotiraga qo'shish
                        replied_users[group].append(chosen_msg.from_user.id)
                        if len(replied_users[group]) > 20:
                            replied_users[group].pop(0)
                    else:
                        # AGAR YANGI ODAM TOPILMASA - ODDIY XABAR
                        await app.send_message(group, current_message)
                        print(f"[{group}] - Yangi odam yo'q, ODDIY xabar ketdi.")
                    
                except Exception as e:
                    print(f"Xatolik yuz berdi ({group}): {e}")
                
                # Guruhlar orasida 3 soniya kutish
                await asyncio.sleep(3)
            
            print("Sikl tugadi. 10 daqiqa (600 sek) tanaffus boshlandi... 💤")
            # 10 daqiqalik tanaffus (600 soniya)
            await asyncio.sleep(600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
