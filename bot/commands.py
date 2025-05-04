from utils import verify_user, check_token, check_verification, get_token
from info import VERIFY, VERIFY_TUTORIAL, BOT_USERNAME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters  # Replace with your framework imports

@Client.on_message(filters.command("start"))
async def start(client, message):
    data = message.command[1]
    if data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True
            )
        is_valid = await check_token(client, userid, token)
        if is_valid:
            await message.reply_text(
                text=f"<b>Hey {message.from_user.mention}, You are successfully verified!\nNow you have unlimited access for all files till today midnight.</b>",
                protect_content=True
            )
            await verify_user(client, userid, token)
        else:
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True
            )

@Client.on_message(filters.private)
async def verify(client, message):
    if not await check_verification(client, message.from_user.id) and VERIFY == "True":
        btn = [[
            InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{BOT_USERNAME}?start="))
        ], [
            InlineKeyboardButton("How To Open Link & Verify", url=VERIFY_TUTORIAL)
        ]]
        await message.reply_text(
            text="<b>You are not verified!\nKindly verify to continue!</b>",
            protect_content=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return
