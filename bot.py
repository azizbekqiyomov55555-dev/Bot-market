import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# ============================================================
#  SOZLAMALAR
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_MARKET_BOT_TOKEN")
ADMIN_ID   = int(os.environ.get("ADMIN_ID", "123456789"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
#  BOTLAR RO'YXATI (15 ta)
#  !! "token" maydoniga BotFather dan olingan tokenlarni yozing !!
# ============================================================
BOTS = {
    "1": {
        "name": "Musiqa Yuklovchi Bot",
        "desc": "YouTube va Spotify'dan MP3 sifatida musiqa yuklab beradi.",
        "price": 15_000,
        "token": "111111111:AAFakeToken_MusicBot_ReplaceMe",
        "emoji": "🎵",
    },
    "2": {
        "name": "Video Yuklovchi Bot",
        "desc": "YouTube, TikTok, Instagram'dan video yuklab beradi.",
        "price": 20_000,
        "token": "222222222:AAFakeToken_VideoBot_ReplaceMe",
        "emoji": "🎬",
    },
    "3": {
        "name": "Kripto Signal Bot",
        "desc": "Real vaqtda kriptovalyuta narxlari va signallar.",
        "price": 35_000,
        "token": "333333333:AAFakeToken_CryptoBot_ReplaceMe",
        "emoji": "💰",
    },
    "4": {
        "name": "Online Do'kon Bot",
        "desc": "Telegram orqali mahsulot sotish va boshqarish tizimi.",
        "price": 50_000,
        "token": "444444444:AAFakeToken_ShopBot_ReplaceMe",
        "emoji": "🛒",
    },
    "5": {
        "name": "Ta'lim va Test Bot",
        "desc": "Ingliz tili va matematikadan testlar, darslar.",
        "price": 25_000,
        "token": "555555555:AAFakeToken_EduBot_ReplaceMe",
        "emoji": "📚",
    },
    "6": {
        "name": "Ob-Havo Bot",
        "desc": "O'zbekiston bo'yicha 7 kunlik ob-havo bashorati.",
        "price": 10_000,
        "token": "666666666:AAFakeToken_WeatherBot_ReplaceMe",
        "emoji": "🌤",
    },
    "7": {
        "name": "GPT Chatbot",
        "desc": "ChatGPT texnologiyasiga asoslangan aqlli suhbatdosh bot.",
        "price": 45_000,
        "token": "777777777:AAFakeToken_GPTBot_ReplaceMe",
        "emoji": "🤖",
    },
    "8": {
        "name": "Valyuta Kursi Bot",
        "desc": "USD, EUR, RUB va boshqa valyutalar real vaqtda.",
        "price": 12_000,
        "token": "888888888:AAFakeToken_CurrencyBot_ReplaceMe",
        "emoji": "💸",
    },
    "9": {
        "name": "Buyurtma Bot",
        "desc": "Restoran va dostavka uchun buyurtma qabul qilish.",
        "price": 55_000,
        "token": "999999999:AAFakeToken_FoodBot_ReplaceMe",
        "emoji": "🍕",
    },
    "10": {
        "name": "Rasm Tahrirlash Bot",
        "desc": "Filtrlar, sticker va watermark qo'shish.",
        "price": 22_000,
        "token": "100100100:AAFakeToken_PhotoBot_ReplaceMe",
        "emoji": "📸",
    },
    "11": {
        "name": "O'yin va Quiz Bot",
        "desc": "Telegram ichida quiz va mini o'yinlar.",
        "price": 18_000,
        "token": "110110110:AAFakeToken_GameBot_ReplaceMe",
        "emoji": "🎮",
    },
    "12": {
        "name": "Anket va So'rovnoma Bot",
        "desc": "Professional anketalar yaratish va natijalar tahlili.",
        "price": 28_000,
        "token": "120120120:AAFakeToken_SurveyBot_ReplaceMe",
        "emoji": "📋",
    },
    "13": {
        "name": "Reminder Bot",
        "desc": "Eslatmalar, jadval va muhim vazifalarni boshqarish.",
        "price": 14_000,
        "token": "130130130:AAFakeToken_ReminderBot_ReplaceMe",
        "emoji": "🔔",
    },
    "14": {
        "name": "Fitnes Treker Bot",
        "desc": "Mashg'ulotlar, kaloriya hisobi va sport rejalari.",
        "price": 20_000,
        "token": "140140140:AAFakeToken_FitnessBot_ReplaceMe",
        "emoji": "🏋️",
    },
    "15": {
        "name": "Support Manager Bot",
        "desc": "Mijozlar bilan muloqot uchun professional support tizimi.",
        "price": 38_000,
        "token": "150150150:AAFakeToken_SupportBot_ReplaceMe",
        "emoji": "💬",
    },
}

# ============================================================
#  YORDAMCHI
# ============================================================
def fmt(price: int) -> str:
    return f"{price:,} so'm".replace(",", " ")

# ============================================================
#  /start
# ============================================================
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🛒 Botlar Katalogi", callback_data="catalog")
    ]])
    await update.message.reply_text(
        f"👋 Salom, *{user.first_name}*!\n\n"
        "🤖 *Bot Bozori*ga xush kelibsiz!\n\n"
        "Bu yerda tayyor Telegram botlarni sotib olib,\n"
        "darhol ishga tushirishingiz mumkin!\n\n"
        f"📦 Hozirda *{len(BOTS)} ta bot* mavjud!",
        parse_mode="Markdown",
        reply_markup=kb
    )

# ============================================================
#  KATALOG — 15 ta bot ro'yxati
# ============================================================
async def show_catalog(query):
    rows = []
    for bid, b in BOTS.items():
        rows.append([InlineKeyboardButton(
            f"{b['emoji']} {b['name']}  —  {fmt(b['price'])}",
            callback_data=f"view|{bid}"
        )])
    rows.append([InlineKeyboardButton("🏠 Bosh Sahifa", callback_data="home")])
    await query.edit_message_text(
        "🛒 *Botlar Katalogi*\n\n"
        "Quyidagi botlardan birini tanlang:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(rows)
    )

# ============================================================
#  BOT TAFSILOTI
# ============================================================
async def show_bot(query, bid: str):
    b = BOTS.get(bid)
    if not b:
        await query.answer("Bot topilmadi!", show_alert=True)
        return

    text = (
        f"{b['emoji']} *{b['name']}*\n"
        f"{'─'*32}\n"
        f"📝 *Tavsif:*\n{b['desc']}\n\n"
        f"💵 *Narxi: {fmt(b['price'])}*\n\n"
        f"✅ Sotib olgach *bot tokeni darhol* yuboriladi!\n"
        f"🚀 Tokenni Railway'ga qo'yib ishga tushirasiz."
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"💳 Sotib Olish — {fmt(b['price'])}", callback_data=f"buy|{bid}")],
        [InlineKeyboardButton("◀️ Katalog", callback_data="catalog")],
    ])
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

# ============================================================
#  TO'LOV SAHIFASI
# ============================================================
async def show_buy(query, bid: str):
    b = BOTS.get(bid)
    if not b:
        await query.answer("Bot topilmadi!", show_alert=True)
        return

    text = (
        f"💳 *To'lov*\n"
        f"{'─'*32}\n"
        f"{b['emoji']} Bot: *{b['name']}*\n"
        f"💵 Summa: *{fmt(b['price'])}*\n\n"
        f"📲 Quyidagi kartaga to'lang:\n\n"
        f"`8600 0000 0000 0000`\n"
        f"_(Nusxalash uchun bosing)_\n\n"
        f"📸 To'lovdan so'ng *chek rasmini*\n"
        f"@YourAdminUsername ga yuboring.\n\n"
        f"⚡ Tasdiqlangandan so'ng *token darhol yuboriladi!*"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ To'ladim — Tokenni Yuborsin!", callback_data=f"paid|{bid}")],
        [InlineKeyboardButton("◀️ Orqaga", callback_data=f"view|{bid}")],
    ])
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

# ============================================================
#  TOKEN YUBORISH
# ============================================================
async def send_token(query, ctx: ContextTypes.DEFAULT_TYPE, bid: str):
    b = BOTS.get(bid)
    user = query.from_user
    if not b:
        await query.answer("Bot topilmadi!", show_alert=True)
        return

    # Adminga xabar
    try:
        await ctx.bot.send_message(
            ADMIN_ID,
            f"🔔 *Yangi Xarid!*\n\n"
            f"👤 [{user.first_name}](tg://user?id={user.id})\n"
            f"🆔 `{user.id}`\n"
            f"{b['emoji']} *{b['name']}*\n"
            f"💰 {fmt(b['price'])}",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.warning(f"Admin xabar xatosi: {e}")

    # Foydalanuvchiga token + yo'riqnoma
    token_msg = (
        f"🎉 *Xaridingiz Muvaffaqiyatli!*\n"
        f"{'─'*32}\n"
        f"{b['emoji']} *{b['name']}*\n\n"
        f"🔑 *Sizning Bot Tokeningiz:*\n"
        f"`{b['token']}`\n"
        f"_(Token nusxalash uchun bosing)_\n\n"
        f"{'─'*32}\n"
        f"🚀 *Botni Ishga Tushirish — Railway:*\n\n"
        f"1️⃣ railway.app ga kiring\n"
        f"2️⃣ *New Project* → *Deploy from GitHub*\n"
        f"3️⃣ Bot kodini GitHub'ga yuklang\n"
        f"4️⃣ *Variables* bo'limiga kiring:\n"
        f"   `BOT_TOKEN` = yuqoridagi token\n"
        f"   `ADMIN_ID` = sizning Telegram ID\n"
        f"5️⃣ *Deploy* ni bosing ✅\n\n"
        f"{'─'*32}\n"
        f"📌 *requirements.txt* faylida:\n"
        f"`python-telegram-bot==20.7`\n\n"
        f"❓ Yordam kerak bo'lsa: @YourAdminUsername"
    )

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Yana Bot Sotib Olish", callback_data="catalog")],
        [InlineKeyboardButton("🏠 Bosh Sahifa", callback_data="home")],
    ])
    await query.edit_message_text(token_msg, parse_mode="Markdown", reply_markup=kb)

# ============================================================
#  BOSH SAHIFA
# ============================================================
async def show_home(query):
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🛒 Botlar Katalogi", callback_data="catalog")
    ]])
    await query.edit_message_text(
        "🏠 *Bosh Sahifa*\n\n"
        f"📦 *{len(BOTS)} ta tayyor bot* mavjud!\n\n"
        "Katalogdan botni tanlang, narxini ko'ring\n"
        "va darhol sotib oling. Token darhol beriladi! ⚡",
        parse_mode="Markdown",
        reply_markup=kb
    )

# ============================================================
#  CALLBACK HANDLER
# ============================================================
async def cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "catalog":
        await show_catalog(query)
    elif data == "home":
        await show_home(query)
    elif data.startswith("view|"):
        await show_bot(query, data.split("|")[1])
    elif data.startswith("buy|"):
        await show_buy(query, data.split("|")[1])
    elif data.startswith("paid|"):
        await send_token(query, ctx, data.split("|")[1])

# ============================================================
#  MAIN
# ============================================================
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    print("✅ Bot Bozori ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
