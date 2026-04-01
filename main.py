import os
import asyncio
from pyrogram import Client

# Environment variables orqali ma'lumotlarni olish
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("STRING_SESSION")

async def main():
    async with Client("my_account", api_id=api_id, api_hash=api_hash, session_string=session_string) as app:
        # Xabar yuboriladigan user va xabar matni
        target_user = "@Doktorgolivud"
        message = "Assalomu alaykum! Bu avtomatik yuborilgan xabar."
        
        try:
            await app.send_message(target_user, message)
            print(f"Xabar {target_user} ga muvaffaqiyatli yuborildi!")
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    asyncio.run(main())
