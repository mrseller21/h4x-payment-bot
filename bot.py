import asyncio, time, io, qrcode
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

# --- CONFIGURATION ---
API_ID = 23163775
API_HASH = "939e799ebced03fb948ea9cca84bcb31"
BOT_TOKEN = "8534146638:AAHUD2W4NSYbfBJPMa1M6i4mAE-uShQrwAU"
ADMIN_USERNAME = "Dang_xowner1"
PLAN_UPI = "h4xseller@ibl"
# ---------------------

app = Client("h4x_full_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("🥉 Basic - ₹99", callback_data="pay_99"), InlineKeyboardButton("🥈 Bronze - ₹149", callback_data="pay_149")],
        [InlineKeyboardButton("🥇 Silver - ₹199", callback_data="pay_199"), InlineKeyboardButton("✨ Gold - ₹249", callback_data="pay_249")],
        [InlineKeyboardButton("💎 Diamond - ₹299", callback_data="pay_299"), InlineKeyboardButton("🏆 Platinum - ₹399", callback_data="pay_399")],
        [InlineKeyboardButton("👑 VIP - ₹499", callback_data="pay_499"), InlineKeyboardButton("🔥 Ultra VIP - ₹599", callback_data="pay_599")]
    ]
    await message.reply_text(
        "<b>🚀 H4X SELLER PREMIUM PLANS:</b>\n\nApna plan select karein. QR 5 min mein delete ho jayega.", 
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML
    )

@app.on_callback_query(filters.regex("^pay_"))
async def send_qr(client, q):
    price = q.data.split("_")[1]
    order_id = f"H4X-{int(time.time())}"
    upi_url = f"upi://pay?pa={PLAN_UPI}&pn=H4X_Seller&am={price}&cu=INR&tr={order_id}"
    
    bio = io.BytesIO()
    qrcode.make(upi_url).save(bio)
    bio.name = "qr.png"; bio.seek(0)
    
    qr_msg = await client.send_photo(
        q.message.chat.id, 
        bio, 
        caption=f"<b>✨ Plan: ₹{price}</b>\n🆔 ID: <code>{order_id}</code>\n\n⚠️ Ye QR 5 minute mein delete ho jayega.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤 Send Screenshot", url=f"t.me/{ADMIN_USERNAME}")]])
    )
    
    try: await q.message.delete()
    except: pass

    await asyncio.sleep(300) 
    try:
        await qr_msg.delete()
        await client.send_message(q.message.chat.id, "❌ <b>QR Expired!</b> Naye QR ke liye /start karein.")
    except:
        pass

app.run()
  
