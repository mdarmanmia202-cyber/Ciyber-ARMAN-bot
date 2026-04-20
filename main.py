import sqlite3
import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from flask import Flask
from threading import Thread

# --- [ Keep Alive Server ] ---
web_app = Flask('')
@web_app.route('/')
def home(): return "Bot is Online 24/7!"
def run_web(): web_app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run_web).start()

# --- [ আপনার তথ্যসমূহ ] ---
API_ID = 22709230  
API_HASH = "afb438609fbec6be6481f71cf52ed539" 
BOT_TOKEN = "8012680077:AAENh8dC08S9nDeerp1D-c63MmX2VyfMWXU"
ADMIN_ID = 7449553757 
MY_PHONE = "01817440477"
ADMIN_USER = "@Savar_Bank_Town"

app = Client("UltimateBusinessBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

db = sqlite3.connect("pro_business.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0)")
db.commit()

def main_menu(balance):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💣 সুপার কল বুম্বার (১০৳)", callback_data="bomb"),
         InlineKeyboardButton("🕵️ প্রোফাইল লুকআপ (৫৳)", callback_data="osint")],
        [InlineKeyboardButton("📸 ক্যামেরা হ্যাক লিঙ্ক (২০৳)", callback_data="cam"),
         InlineKeyboardButton("📍 লোকেশন ট্র্যাকার (১০৳)", callback_data="track")],
        [InlineKeyboardButton("💰 টাকা যোগ করুন", callback_data="pay"),
         InlineKeyboardButton("📊 আমার অ্যাকাউন্ট", callback_data="acc")],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট", url=f"https://t.me/Savar_Bank_Town")]
    ])

@app.on_message(filters.command("start"))
async def start(client, message):
    uid = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, ?)", (uid, 0))
    db.commit()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (uid,))
    balance = cursor.fetchone()[0]
    await message.reply_text(f"👑 **প্রো-লেভেল সার্ভিস বর্টে স্বাগতম!**\n\n🆔 আইডি: `{uid}`\n💰 ব্যালেন্স: **{balance} টাকা**", reply_markup=main_menu(balance))

@app.on_callback_query()
async def handle_buttons(client, query: CallbackQuery):
    uid = query.from_user.id
    if query.data == "pay":
        pay_text = (f"💳 **টাকা অ্যাড করার নিয়ম:**\n\nবিকাশ/নগদ/রকেট: `{MY_PHONE}`\nTransaction ID ও UserID ({uid}) অ্যাডমিনকে পাঠান।")
        await query.message.edit_text(pay_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ব্যাকে যান", callback_data="home")]]))
    elif query.data == "home":
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (uid,))
        balance = cursor.fetchone()[0]
        await query.message.edit_text("আমাদের সার্ভিস মেনু:", reply_markup=main_menu(balance))

@app.on_message(filters.command("add") & filters.user(ADMIN_ID))
async def add_money(client, message):
    try:
        _, target, amount = message.text.split()
        cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, target))
        db.commit()
        await message.reply(f"✅ সফল! {target} আইডিতে {amount}৳ যোগ হয়েছে।")
        await client.send_message(target, f"🎉 অভিনন্দন! আপনার অ্যাকাউন্টে {amount} টাকা যোগ করা হয়েছে।")
    except: await message.reply("ভুল নিয়ম। উদাহরণ: `/add UserID Amount`")

if __name__ == "__main__":
    keep_alive()
    app.run()

