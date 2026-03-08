import os
import logging
import asyncio
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# ============================================================
#  SOZLAMALAR
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_MARKET_BOT_TOKEN")
ADMIN_ID  = int(os.environ.get("ADMIN_ID", "123456789"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ConversationHandler holatlari
WAIT_TOKEN = 1

# Ishlab turgan botlar: {user_id: {"app": Application, "bot_id": str}}
running_bots: dict = {}

# ============================================================
#  BOTLAR RO'YXATI (15 ta)
#  Har bir bot uchun alohida handler_factory bor —
#  foydalanuvchi token kiritgach shu bot kodi ishga tushadi
# ============================================================
BOTS = {
    "1":  {"name": "Musiqa Yuklovchi Bot",   "emoji": "🎵", "price": 15_000, "type": "music"},
    "2":  {"name": "Video Yuklovchi Bot",    "emoji": "🎬", "price": 20_000, "type": "video"},
    "3":  {"name": "Kripto Signal Bot",      "emoji": "💰", "price": 35_000, "type": "crypto"},
    "4":  {"name": "Online Do'kon Bot",      "emoji": "🛒", "price": 50_000, "type": "shop"},
    "5":  {"name": "Ta'lim va Test Bot",     "emoji": "📚", "price": 25_000, "type": "edu"},
    "6":  {"name": "Ob-Havo Bot",            "emoji": "🌤", "price": 10_000, "type": "weather"},
    "7":  {"name": "GPT Chatbot",            "emoji": "🤖", "price": 45_000, "type": "gpt"},
    "8":  {"name": "Valyuta Kursi Bot",      "emoji": "💸", "price": 12_000, "type": "currency"},
    "9":  {"name": "Buyurtma Bot",           "emoji": "🍕", "price": 55_000, "type": "order"},
    "10": {"name": "Rasm Tahrirlash Bot",    "emoji": "📸", "price": 22_000, "type": "photo"},
    "11": {"name": "O'yin va Quiz Bot",      "emoji": "🎮", "price": 18_000, "type": "game"},
    "12": {"name": "Anket Bot",              "emoji": "📋", "price": 28_000, "type": "survey"},
    "13": {"name": "Reminder Bot",           "emoji": "🔔", "price": 14_000, "type": "reminder"},
    "14": {"name": "Fitnes Treker Bot",      "emoji": "🏋️", "price": 20_000, "type": "fitness"},
    "15": {"name": "Support Manager Bot",   "emoji": "💬", "price": 38_000, "type": "support"},
}

def fmt(price: int) -> str:
    return f"{price:,} so'm".replace(",", " ")

# ============================================================
#  HAR BIR BOT TURI UCHUN HANDLER YARATUVCHI
# ============================================================
def build_bot_app(token: str, bot_type: str, bot_name: str) -> Application:
    """Berilgan token va turga qarab tayyor bot Application qaytaradi."""

    # --- UNIVERSAL START ---
    async def sub_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f"👋 Salom! Men *{bot_name}*man.\n"
            f"Yordamchi buyruqlar uchun /help yozing.",
            parse_mode="Markdown"
        )

    async def sub_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        helps = {
            "music":    "🎵 Qo'shiq nomini yuboring, MP3 yuklab beraman!",
            "video":    "🎬 Video havolasini yuboring, yuklab beraman!",
            "crypto":   "💰 /btc /eth /sol — narxlarni ko'ring",
            "shop":     "🛒 /catalog — mahsulotlar ro'yxati",
            "edu":      "📚 /test — yangi test boshlash",
            "weather":  "🌤 Shahar nomini yuboring, ob-havoni aytaman!",
            "gpt":      "🤖 Istalgan savolingizni yozing!",
            "currency": "💸 /usd /eur /rub — valyuta kurslari",
            "order":    "🍕 /menu — menyu ko'rish",
            "photo":    "📸 Rasm yuboring, tahrirlash imkoniyatlarini ko'rsataman!",
            "game":     "🎮 /quiz — yangi o'yin boshlash",
            "survey":   "📋 /newsurvey — yangi so'rovnoma yaratish",
            "reminder": "🔔 /remind 10:00 Uchrashuv — eslatma qo'shish",
            "fitness":  "🏋️ /workout — bugungi mashg'ulot",
            "support":  "💬 Muammoingizni yozing, yordam beraman!",
        }
        await update.message.reply_text(
            f"ℹ️ *{bot_name}* — Yordam\n\n{helps.get(bot_type, 'Xabar yuboring!')}",
            parse_mode="Markdown"
        )

    # --- BOT TURIGA QARAB MAXSUS HANDLER ---
    async def sub_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        text = update.message.text or ""

        if bot_type == "music":
            await update.message.reply_text(f"🎵 *{text}* qo'shig'i qidirilmoqda...\n_(Demo rejim: haqiqiy bot qo'shimcha kod talab qiladi)_", parse_mode="Markdown")

        elif bot_type == "video":
            await update.message.reply_text(f"🎬 Video yuklanmoqda...\n🔗 {text}\n_(Demo rejim)_")

        elif bot_type == "crypto":
            import random
            prices = {"btc": 67000, "eth": 3500, "sol": 180, "bnb": 600}
            coin = text.lower().replace("/","")
            price = prices.get(coin, random.randint(1, 1000))
            await update.message.reply_text(f"💰 *{text.upper()}* = *${price:,}*", parse_mode="Markdown")

        elif bot_type == "weather":
            await update.message.reply_text(
                f"🌤 *{text}* shahri ob-havosi:\n\n"
                f"🌡 Harorat: 22°C\n☁️ Bulutli\n💨 Shamol: 12 km/h\n_(Demo rejim)_",
                parse_mode="Markdown"
            )

        elif bot_type == "gpt":
            await update.message.reply_text(
                f"🤖 Savolingiz: _{text}_\n\n"
                f"Javob: Bu demo rejim. Haqiqiy GPT uchun OpenAI API kerak.",
                parse_mode="Markdown"
            )

        elif bot_type == "currency":
            rates = {"usd": 12800, "eur": 13900, "rub": 140}
            coin = text.lower().replace("/","")
            rate = rates.get(coin, "—")
            await update.message.reply_text(f"💸 *{text.upper()}* = *{rate} so'm*", parse_mode="Markdown")

        elif bot_type == "reminder":
            await update.message.reply_text(f"🔔 Eslatma saqlandi: *{text}*", parse_mode="Markdown")

        elif bot_type == "fitness":
            await update.message.reply_text(
                f"🏋️ *Bugungi Mashg'ulot:*\n\n"
                f"1. Yugurish — 20 daqiqa\n2. Siqish — 3x15\n3. Tortish — 3x10\n\n"
                f"💪 Omad! _{text}_",
                parse_mode="Markdown"
            )

        elif bot_type == "support":
            await update.message.reply_text(
                f"💬 Muammoingiz qabul qilindi:\n_{text}_\n\n"
                f"Operator tez orada javob beradi!",
                parse_mode="Markdown"
            )

        else:
            await update.message.reply_text(
                f"✅ Xabaringiz qabul qilindi!\n_{text}_",
                parse_mode="Markdown"
            )

    # App yaratish
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", sub_start))
    app.add_handler(CommandHandler("help", sub_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, sub_message))
    return app

# ============================================================
#  BOT ORQA FONDA ISHGA TUSHIRISH
# ============================================================
def launch_bot_in_thread(token: str, bot_type: str, bot_name: str, user_id: int):
    """Yangi bot ni alohida thread da ishga tushiradi."""
    loop = asyncio.new_event_loop()

    def run():
        asyncio.set_event_loop(loop)
        app = build_bot_app(token, bot_type, bot_name)
        running_bots[user_id] = {"app": app, "loop": loop}
        loop.run_until_complete(app.initialize())
        loop.run_until_complete(app.start())
        loop.run_until_complete(app.updater.start_polling())
        loop.run_forever()

    t = threading.Thread(target=run, daemon=True)
    t.start()
    logger.info(f"Bot ishga tushdi: {bot_name} | user_id={user_id}")

async def stop_user_bot(user_id: int):
    """Foydalanuvchining eski botini to'xtatadi."""
    if user_id in running_bots:
        try:
            info = running_bots.pop(user_id)
            app = info["app"]
            loop = info["loop"]
            asyncio.run_coroutine_threadsafe(app.updater.stop(), loop)
            asyncio.run_coroutine_threadsafe(app.stop(), loop)
            asyncio.run_coroutine_threadsafe(app.shutdown(), loop)
        except Exception as e:
            logger.warning(f"Bot to'xtatishda xato: {e}")

# ============================================================
#  MARKET BOT — /start
# ============================================================
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🛒 Botlar Katalogi", callback_data="catalog")
    ]])
    await update.message.reply_text(
        f"👋 Salom, *{user.first_name}*!\n\n"
        "🤖 *Bot Bozori*ga xush kelibsiz!\n\n"
        "✅ Bot sotib oling\n"
        "🔑 O'zingizning tokeningizni kiriting\n"
        "🚀 Bot darhol ishga tushadi!\n\n"
        f"📦 *{len(BOTS)} ta tayyor bot* mavjud!",
        parse_mode="Markdown",
        reply_markup=kb
    )

# ============================================================
#  KATALOG
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
        "🛒 *Botlar Katalogi*\n\nBotni tanlang:",
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
        f"{'─'*30}\n"
        f"💵 *Narxi: {fmt(b['price'])}*\n\n"
        f"✅ Sotib olgach *o'zingizning bot tokeningizni* kiriting\n"
        f"⚡ Bot darhol ishga tushadi!"
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
        f"{'─'*30}\n"
        f"{b['emoji']} *{b['name']}*\n"
        f"💵 Summa: *{fmt(b['price'])}*\n\n"
        f"📲 Quyidagi kartaga to'lang:\n\n"
        f"`8600 0000 0000 0000`\n\n"
        f"To'lovdan so'ng *✅ To'ladim* tugmasini bosing."
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ To'ladim", callback_data=f"paid|{bid}")],
        [InlineKeyboardButton("◀️ Orqaga", callback_data=f"view|{bid}")],
    ])
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

# ============================================================
#  TO'LOV TASDIQLANDI — TOKEN SO'RASH
# ============================================================
async def ask_token(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Callback: paid|{bid} — tokenni so'rash."""
    query = update.callback_query
    await query.answer()
    bid = query.data.split("|")[1]
    b = BOTS.get(bid)
    if not b:
        await query.answer("Bot topilmadi!", show_alert=True)
        return

    ctx.user_data["pending_bid"] = bid

    # Adminga xabar
    user = query.from_user
    try:
        await ctx.bot.send_message(
            ADMIN_ID,
            f"🔔 *Yangi Xarid!*\n👤 [{user.first_name}](tg://user?id={user.id})\n"
            f"🆔 `{user.id}`\n{b['emoji']} *{b['name']}* — {fmt(b['price'])}",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.warning(f"Admin xabar xatosi: {e}")

    await query.edit_message_text(
        f"🎉 *Rahmat! Xaridingiz qabul qilindi.*\n\n"
        f"{b['emoji']} *{b['name']}*\n\n"
        f"{'─'*30}\n"
        f"🔑 *Endi bot tokeningizni kiriting:*\n\n"
        f"📌 Token olish uchun:\n"
        f"1. @BotFather ga yozing\n"
        f"2. /newbot buyrug'ini yuboring\n"
        f"3. Bot nomini kiriting\n"
        f"4. Olingan tokenni *bu yerga* yuboring\n\n"
        f"_Misol: `1234567890:AAHdqTcvbiJc-abcdefghijklmnopqrst`_",
        parse_mode="Markdown"
    )
    return WAIT_TOKEN

# ============================================================
#  TOKEN QABUL QILISH VA BOTNI ISHGA TUSHIRISH
# ============================================================
async def receive_token(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_token = update.message.text.strip()
    user_id    = update.effective_user.id
    bid        = ctx.user_data.get("pending_bid")

    if not bid:
        await update.message.reply_text("❌ Avval bot tanlang. /start")
        return ConversationHandler.END

    b = BOTS[bid]

    # Token formatini tekshirish
    if ":" not in user_token or len(user_token) < 30:
        await update.message.reply_text(
            "❌ *Token noto'g'ri format!*\n\n"
            "To'g'ri format:\n`1234567890:AAHdqTcvbi...`\n\n"
            "Qaytadan kiriting:",
            parse_mode="Markdown"
        )
        return WAIT_TOKEN

    # Token bilan bot mavjudligini tekshirish
    await update.message.reply_text("⏳ Bot tekshirilmoqda va ishga tushirilmoqda...")

    try:
        # Tokenni tekshirish
        test_app = Application.builder().token(user_token).build()
        await test_app.initialize()
        bot_info = await test_app.bot.get_me()
        await test_app.shutdown()

        # Eski botni to'xtatish
        await stop_user_bot(user_id)

        # Yangi botni ishga tushirish
        launch_bot_in_thread(user_token, b["type"], b["name"], user_id)

        await asyncio.sleep(2)  # Ishga tushishini kutish

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Yana Bot Sotib Olish", callback_data="catalog")],
            [InlineKeyboardButton("🏠 Bosh Sahifa", callback_data="home")],
        ])

        await update.message.reply_text(
            f"🚀 *Bot Muvaffaqiyatli Ishga Tushdi!*\n"
            f"{'─'*30}\n"
            f"{b['emoji']} *{b['name']}*\n\n"
            f"🤖 Bot username: @{bot_info.username}\n"
            f"📛 Bot nomi: {bot_info.first_name}\n\n"
            f"✅ Botingiz hozir ishlayapti!\n"
            f"👉 @{bot_info.username} ga o'ting va /start yuboring\n\n"
            f"⚠️ *Eslatma:* Bot bu server ishlagan vaqtda\n"
            f"faol bo'ladi. Doimiy ishlash uchun\n"
            f"Railway/VPS ga deploy qiling.",
            parse_mode="Markdown",
            reply_markup=kb
        )

    except Exception as e:
        logger.error(f"Bot ishga tushirishda xato: {e}")
        error_msg = str(e)
        if "Unauthorized" in error_msg or "invalid token" in error_msg.lower():
            msg = "❌ *Token noto'g'ri yoki bot allaqachon o'chirilgan!*\n\nQaytadan kiriting:"
        elif "Conflict" in error_msg:
            msg = "⚠️ *Bu bot allaqachon boshqa joyda ishlamoqda!*\n\nBotni to'xtatib qaytadan kiriting:"
        else:
            msg = f"❌ *Xato yuz berdi:*\n`{error_msg[:100]}`\n\nQaytadan urinib ko'ring:"

        await update.message.reply_text(msg, parse_mode="Markdown")
        return WAIT_TOKEN

    ctx.user_data.pop("pending_bid", None)
    return ConversationHandler.END

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
        "Bot tanlang → To'lang → Token kiriting\n"
        "⚡ Bot darhol ishga tushadi!",
        parse_mode="Markdown",
        reply_markup=kb
    )

# ============================================================
#  CANCEL
# ============================================================
async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text("❌ Bekor qilindi. /start")
    return ConversationHandler.END

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

# ============================================================
#  MAIN
# ============================================================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # ConversationHandler — token so'rash jarayoni
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(ask_token, pattern=r"^paid\|")],
        states={
            WAIT_TOKEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_token)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
        per_chat=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(cb))

    print("✅ Bot Bozori ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
