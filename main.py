import os
import asyncio
from pyrogram import Client

# Environment variables orqali ma'lumotlarni olish
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("STRING_SESSION")

async def main():
    # Clientni bir marta yaratamiz
    app = Client(
        "my_account", 
        api_id=API_ID, 
        api_hash=API_HASH, 
        session_string=SESSION_STRING
    )
    
    async with app:
        target_user = "@Doktorgolivud"
        message = "Bu avtomatik yuborilgan xabar😀."
        
        print("Bot ishga tushdi...")
        
        while True:  # To'xtovsiz takrorlash uchun
            try:
                await app.send_message(target_user, message)
                print(f"Xabar {target_user} ga muvaffaqiyatli yuborildi!")
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
            
            # 60 soniya (1 daqiqa) kutish
            await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
