import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# === SOZLAMALAR ===
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # @BotFather dan olingan token
ADMIN_ID = 123456789  # Sizning Telegram ID'ingiz

# === BOTLAR RO'YXATI (15 ta dan ortiq) ===
BOTS = {
    "1": {
        "name": "🎵 Musiqa Yuklovchi Bot",
        "description": "YouTube, Spotify, SoundCloud dan musiqa yuklovchi. Sifatli MP3 format!",
        "price": 15000,
        "category": "media",
        "token": "@MusicDownloaderBot",
        "rating": 4.8,
        "sales": 234
    },
    "2": {
        "name": "🎬 Video Yuklovchi Bot",
        "description": "YouTube, TikTok, Instagram, Facebook dan video yuklovchi bot.",
        "price": 20000,
        "category": "media",
        "token": "@VideoDownBot",
        "rating": 4.7,
        "sales": 189
    },
    "3": {
        "name": "💰 Kriptovalyuta Bot",
        "description": "Real vaqtda kriptovalyuta narxlari, signal va tahlillar.",
        "price": 35000,
        "category": "finance",
        "token": "@CryptoSignalBot",
        "rating": 4.9,
        "sales": 312
    },
    "4": {
        "name": "🛒 Online Do'kon Boti",
        "description": "Telegram orqali mahsulot sotish va boshqarish tizimi.",
        "price": 50000,
        "category": "business",
        "token": "@ShopManagerBot",
        "rating": 4.6,
        "sales": 145
    },
    "5": {
        "name": "📚 Ta'lim Boti",
        "description": "Ingliz tili, matematika va boshqa fanlardan testlar va darslar.",
        "price": 25000,
        "category": "education",
        "token": "@EduLearnBot",
        "rating": 4.8,
        "sales": 267
    },
    "6": {
        "name": "🌤 Ob-Havo Boti",
        "description": "O'zbekiston va dunyo bo'ylab ob-havo ma'lumotlari. 7 kunlik bashorat.",
        "price": 10000,
        "category": "utility",
        "token": "@WeatherUzBot",
        "rating": 4.5,
        "sales": 423
    },
    "7": {
        "name": "🤖 GPT Chatbot",
        "description": "ChatGPT texnologiyasiga asoslangan aqlli suhbatdosh bot.",
        "price": 45000,
        "category": "ai",
        "token": "@SmartGPTBot",
        "rating": 4.9,
        "sales": 501
    },
    "8": {
        "name": "📊 Statistika Boti",
        "description": "Kanallar va guruhlar uchun statistika va tahlil boti.",
        "price": 30000,
        "category": "analytics",
        "token": "@ChannelStatsBot",
        "rating": 4.7,
        "sales": 178
    },
    "9": {
        "name": "🎮 O'yin Boti",
        "description": "Telegram ichida quiz, викторина va boshqa o'yinlar.",
        "price": 18000,
        "category": "entertainment",
        "token": "@GameQuizBot",
        "rating": 4.6,
        "sales": 334
    },
    "10": {
        "name": "📱 SMS Xabarnoma Boti",
        "description": "Ommaviy SMS va Telegram xabar yuborish tizimi.",
        "price": 40000,
        "category": "business",
        "token": "@MassSenderBot",
        "rating": 4.4,
        "sales": 89
    },
    "11": {
        "name": "💸 Valyuta Kursi Boti",
        "description": "Real vaqtda valyuta kurslari. USD, EUR, RUB va boshqalar.",
        "price": 12000,
        "category": "finance",
        "token": "@CurrencyRateBot",
        "rating": 4.8,
        "sales": 567
    },
    "12": {
        "name": "🍕 Buyurtma Boti",
        "description": "Restoran va dostavka uchun buyurtma qabul qilish tizimi.",
        "price": 55000,
        "category": "business",
        "token": "@FoodOrderBot",
        "rating": 4.7,
        "sales": 123
    },
    "13": {
        "name": "📸 Rasm Tahrirlash Boti",
        "description": "Filtrlar, sticker va watermark qo'shish. Professional sifat!",
        "price": 22000,
        "category": "media",
        "token": "@PhotoEditorBot",
        "rating": 4.5,
        "sales": 289
    },
    "14": {
        "name": "🔐 Parol Generatori",
        "description": "Kuchli parollar yaratish va saqlash xizmati.",
        "price": 8000,
        "category": "utility",
        "token": "@SecurePassBot",
        "rating": 4.6,
        "sales": 412
    },
    "15": {
        "name": "📋 Anket va So'rovnoma Boti",
        "description": "Professional anketalar yaratish va natijalarni tahlil qilish.",
        "price": 28000,
        "category": "business",
        "token": "@SurveyFormBot",
        "rating": 4.7,
        "sales": 156
    },
    "16": {
        "name": "🎓 Kurs Sotish Boti",
        "description": "Online kurslar va darsliklar sotish platformasi.",
        "price": 60000,
        "category": "education",
        "token": "@CourseSellerBot",
        "rating": 4.9,
        "sales": 78
    },
    "17": {
        "name": "🚗 Taksi Buyurtma Boti",
        "description": "Taksi xizmati uchun buyurtma va haydovchi boshqaruv tizimi.",
        "price": 70000,
        "category": "transport",
        "token": "@TaxiOrderBot",
        "rating": 4.8,
        "sales": 45
    },
    "18": {
        "name": "🏋️ Fitnes Treker Boti",
        "description": "Mashg'ulotlar, kaloriya hisobi va sport rejalari.",
        "price": 20000,
        "category": "health",
        "token": "@FitnessTrackerBot",
        "rating": 4.6,
        "sales": 198
    },
    "19": {
        "name": "🔔 Reminder Boti",
        "description": "Eslatmalar, jadval va muhim vazifalarni boshqarish.",
        "price": 14000,
        "category": "utility",
        "token": "@ReminderPlanBot",
        "rating": 4.5,
        "sales": 345
    },
    "20": {
        "name": "💬 Qo'llab-quvvatlash Boti",
        "description": "Mijozlar bilan muloqot uchun professional support tizimi.",
        "price": 38000,
        "category": "business",
        "token": "@SupportManagerBot",
        "rating": 4.8,
        "sales": 167
    },
}

CATEGORIES = {
    "media": "🎬 Media",
    "finance": "💰 Moliya",
    "business": "🛒 Biznes",
    "education": "📚 Ta'lim",
    "utility": "🔧 Utilitalar",
    "ai": "🤖 Sun'iy Intellekt",
    "analytics": "📊 Tahlil",
    "entertainment": "🎮 Ko'ngil ochar",
    "transport": "🚗 Transport",
    "health": "🏋️ Salomatlik",
}

# State
WAITING_PAYMENT = 1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === YORDAMCHI FUNKSIYALAR ===

def format_price(price: int) -> str:
    return f"{price:,} so'm".replace(",", " ")

def get_bot_by_id(bot_id: str):
    return BOTS.get(bot_id)

def stars(rating: float) -> str:
    full = int(rating)
    return "⭐" * full + f" {rating}"

# === ASOSIY MENYULAR ===

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛒 Botlar Do'koniga Kirish", callback_data="shop")],
        [InlineKeyboardButton("📦 Mening Xaridlarim", callback_data="my_purchases")],
        [InlineKeyboardButton("ℹ️ Biz Haqimizda", callback_data="about"),
         InlineKeyboardButton("📞 Aloqa", callback_data="contact")],
    ]
    return InlineKeyboardMarkup(keyboard)

def shop_keyboard():
    keyboard = []
    # Kategoriyalar
    keyboard.append([InlineKeyboardButton("📂 Kategoriya bo'yicha", callback_data="by_category")])
    keyboard.append([InlineKeyboardButton("🔥 Eng Ommabop", callback_data="popular"),
                     InlineKeyboardButton("💎 Premium Botlar", callback_data="premium")])
    keyboard.append([InlineKeyboardButton("🆕 Yangi Botlar", callback_data="newest")])
    keyboard.append([InlineKeyboardButton("🏠 Bosh Menyu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def category_keyboard():
    keyboard = []
    row = []
    for key, name in CATEGORIES.items():
        row.append(InlineKeyboardButton(name, callback_data=f"cat_{key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("◀️ Orqaga", callback_data="shop")])
    return InlineKeyboardMarkup(keyboard)

def bots_list_keyboard(bot_list: list, back_callback: str = "shop"):
    keyboard = []
    for bot_id, bot in bot_list:
        keyboard.append([InlineKeyboardButton(
            f"{bot['name']} — {format_price(bot['price'])}",
            callback_data=f"view_{bot_id}"
        )])
    keyboard.append([InlineKeyboardButton("◀️ Orqaga", callback_data=back_callback)])
    return InlineKeyboardMarkup(keyboard)

def bot_detail_keyboard(bot_id: str):
    keyboard = [
        [InlineKeyboardButton("🛒 Sotib Olish", callback_data=f"buy_{bot_id}")],
        [InlineKeyboardButton("◀️ Orqaga", callback_data="shop")],
        [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def confirm_buy_keyboard(bot_id: str):
    keyboard = [
        [InlineKeyboardButton("✅ To'lovni Tasdiqlash", callback_data=f"confirm_{bot_id}")],
        [InlineKeyboardButton("❌ Bekor Qilish", callback_data=f"view_{bot_id}")],
    ]
    return InlineKeyboardMarkup(keyboard)

# === HANDLER FUNKSIYALAR ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"👋 Assalomu alaykum, *{user.first_name}*!\n\n"
        "🤖 *Bot Bozori*ga xush kelibsiz!\n\n"
        "Bu yerda siz tayyor Telegram botlarni sotib olishingiz mumkin.\n"
        f"📦 Hozirda *{len(BOTS)} ta bot* mavjud!\n\n"
        "Quyidagi menyudan tanlang:"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # === BOSH MENYU ===
    if data == "main_menu":
        user = update.effective_user
        text = (
            f"🏠 *Bosh Menyu*\n\n"
            f"Salom, *{user.first_name}*!\n"
            f"📦 Bizda *{len(BOTS)} ta* tayyor bot mavjud.\n\n"
            "Nimani xohlaysiz?"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

    # === DO'KON ===
    elif data == "shop":
        text = (
            "🛒 *Bot Do'koni*\n\n"
            f"Jami: *{len(BOTS)} ta bot* mavjud\n"
            "Kategoriya yoki saralash bo'yicha tanlang:"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=shop_keyboard())

    # === KATEGORIYALAR ===
    elif data == "by_category":
        text = "📂 *Kategoriyalar*\n\nQuyidagi kategoriyalardan birini tanlang:"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=category_keyboard())

    elif data.startswith("cat_"):
        cat_key = data[4:]
        cat_name = CATEGORIES.get(cat_key, "Noma'lum")
        filtered = [(bid, b) for bid, b in BOTS.items() if b["category"] == cat_key]
        if not filtered:
            await query.edit_message_text("Bu kategoriyada botlar mavjud emas.", reply_markup=category_keyboard())
            return
        text = f"📂 *{cat_name}* kategoriyasi\n\n*{len(filtered)} ta bot* topildi:\n\nBotni tanlang:"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=bots_list_keyboard(filtered, "by_category"))

    # === ENG OMMABOP ===
    elif data == "popular":
        sorted_bots = sorted(BOTS.items(), key=lambda x: x[1]["sales"], reverse=True)[:8]
        text = "🔥 *Eng Ommabop Botlar*\n\nSotuvlar soni bo'yicha:"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=bots_list_keyboard(sorted_bots))

    # === PREMIUM ===
    elif data == "premium":
        sorted_bots = sorted(BOTS.items(), key=lambda x: x[1]["price"], reverse=True)[:8]
        text = "💎 *Premium Botlar*\n\nNarx bo'yicha eng yuqori:"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=bots_list_keyboard(sorted_bots))

    # === YANGI BOTLAR ===
    elif data == "newest":
        # Oxirgi qo'shilganlar (ID bo'yicha teskari)
        sorted_bots = sorted(BOTS.items(), key=lambda x: int(x[0]), reverse=True)[:8]
        text = "🆕 *Yangi Qo'shilgan Botlar*:"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=bots_list_keyboard(sorted_bots))

    # === BOT TAFSILOTLARI ===
    elif data.startswith("view_"):
        bot_id = data[5:]
        bot = get_bot_by_id(bot_id)
        if not bot:
            await query.edit_message_text("Bot topilmadi.")
            return
        text = (
            f"*{bot['name']}*\n"
            f"{'─' * 30}\n"
            f"📝 *Tavsif:*\n{bot['description']}\n\n"
            f"⭐ *Reyting:* {stars(bot['rating'])}\n"
            f"📊 *Sotilgan:* {bot['sales']} marta\n"
            f"🏷 *Narxi:* {format_price(bot['price'])}\n\n"
            f"✅ Sotib olsangiz bot token va sozlash yo'riqnomasi beriladi."
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=bot_detail_keyboard(bot_id))

    # === SOTIB OLISH ===
    elif data.startswith("buy_"):
        bot_id = data[4:]
        bot = get_bot_by_id(bot_id)
        if not bot:
            await query.edit_message_text("Bot topilmadi.")
            return
        
        context.user_data["pending_bot_id"] = bot_id
        
        text = (
            f"🛒 *Xarid Tasdiqlash*\n"
            f"{'─' * 30}\n"
            f"Bot: *{bot['name']}*\n"
            f"💵 Narxi: *{format_price(bot['price'])}*\n\n"
            f"💳 *To'lov usuli:*\n"
            f"Quyidagi kartaga to'lov qiling:\n\n"
            f"`8600 1234 5678 9012`\n"
            f"_(Karta nusxalash uchun bosing)_\n\n"
            f"📸 To'lovdan so'ng chekni admin @YourAdminUsername ga yuboring.\n"
            f"Tasdiqlangandan so'ng bot beriladi."
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=confirm_buy_keyboard(bot_id))

    # === TO'LOV TASDIQLASH ===
    elif data.startswith("confirm_"):
        bot_id = data[8:]
        bot = get_bot_by_id(bot_id)
        user = update.effective_user

        if not bot:
            await query.edit_message_text("Bot topilmadi.")
            return

        # Adminga xabar yuborish
        try:
            admin_text = (
                f"🔔 *Yangi Buyurtma!*\n\n"
                f"👤 Foydalanuvchi: [{user.first_name}](tg://user?id={user.id})\n"
                f"🆔 ID: `{user.id}`\n"
                f"🤖 Bot: *{bot['name']}*\n"
                f"💰 Summa: *{format_price(bot['price'])}*\n\n"
                f"To'lovni tasdiqlang va botni yuboring."
            )
            await context.bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Admin xabar xatosi: {e}")

        text = (
            f"✅ *Buyurtmangiz Qabul Qilindi!*\n\n"
            f"🤖 Bot: *{bot['name']}*\n"
            f"💵 Summa: *{format_price(bot['price'])}*\n\n"
            f"📸 Iltimos to'lov chekini admin @YourAdminUsername ga yuboring.\n"
            f"⏱ Tasdiqlash 1-24 soat ichida amalga oshiriladi.\n\n"
            f"Savollar uchun: @YourAdminUsername"
        )
        keyboard = [[InlineKeyboardButton("🏠 Bosh Menyu", callback_data="main_menu")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    # === XARIDLAR ===
    elif data == "my_purchases":
        text = (
            "📦 *Mening Xaridlarim*\n\n"
            "Hali xarid qilmadingiz yoki xaridlar tarixingiz bo'sh.\n\n"
            "Bot sotib olish uchun Do'konga kiring!"
        )
        keyboard = [
            [InlineKeyboardButton("🛒 Do'konga Kirish", callback_data="shop")],
            [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="main_menu")],
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    # === BIZ HAQIMIZDA ===
    elif data == "about":
        text = (
            "ℹ️ *Biz Haqimizda*\n\n"
            "🤖 *Bot Bozori* — O'zbekistondagi eng yirik Telegram bot savdosi platformasi!\n\n"
            f"📦 *{len(BOTS)}+* tayyor bot\n"
            "✅ Sifat kafolati\n"
            "🔧 Bepul sozlash yo'riqnomasi\n"
            "📞 7/24 qo'llab-quvvatlash\n\n"
            "Har bir bot sotib olinganidan so'ng:\n"
            "• Bot token beriladi\n"
            "• Sozlash yo'riqnomasi yuboriladi\n"
            "• 30 kun bepul support"
        )
        keyboard = [[InlineKeyboardButton("🏠 Bosh Menyu", callback_data="main_menu")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    # === ALOQA ===
    elif data == "contact":
        text = (
            "📞 *Aloqa*\n\n"
            "👤 Admin: @YourAdminUsername\n"
            "📧 Email: info@botbozori.uz\n"
            "🕐 Ish vaqti: 9:00 - 22:00\n\n"
            "Savollaringiz bo'lsa bemalol yozing!"
        )
        keyboard = [[InlineKeyboardButton("🏠 Bosh Menyu", callback_data="main_menu")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# === ADMIN BUYRUQLARI ===

async def admin_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    text = f"📊 *Admin Panel*\n\nJami botlar: *{len(BOTS)} ta*\n\n"
    for bid, bot in BOTS.items():
        text += f"{bid}. {bot['name']} — {format_price(bot['price'])}\n"
    await update.message.reply_text(text, parse_mode="Markdown")

# === ASOSIY FUNKSIYA ===

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_list))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
