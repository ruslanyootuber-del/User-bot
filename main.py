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
            "@w_2008_2009_2007", "@real_qizlarbore", "@tanishuvlar_ovozli_chat_gruppa", "@ajrashganlar_tanishaaa", "@Samarqand_chat_Qashqadaryo", "@TANSHUVLAR_QADIRDONLARIM"
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
        
        print("Bot ishga tushdi. Random xabarlar va 6 daqiqalik tanaffus faol! ✅")
        
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
            
            print("Sikl tugadi. 6 daqiqa (360 sek) tanaffus boshlandi... 💤")
            # 5 daqiqalik tanaffus (360 soniya)
            await asyncio.sleep(360)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")