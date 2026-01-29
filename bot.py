from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ================= CONFIG =================

BOT_TOKEN = "7427886699:AAEeWzaOGjSuQUkwxrMd6VpzYaEQCn7gCho"

CHANNELS = [
    "https://t.me/+yhJuQDHiJ61kYWM1",
    "https://t.me/Czarmy007",
]

# verified users store (temporary)
verified_users = set()

# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # agar already verified hai
    if user_id in verified_users:
        await update.message.reply_text(
            "✅ You are already verified.\n\nUse /menu to continue."
        )
        return

    buttons = []

    for ch in CHANNELS:
        buttons.append([
            InlineKeyboardButton(
                text=f"📢 Join {ch}",
                url=f"https://t.me/{ch.replace('@','')}"
            )
        ])

    buttons.append([
        InlineKeyboardButton("✅ Verify", callback_data="verify")
    ])

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "👇 Please join all channels below and then click Verify:",
        reply_markup=reply_markup
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    not_joined = []

    for ch in CHANNELS:
        try:
            member = await context.bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(ch)
        except:
            not_joined.append(ch)

    if not_joined:
        await query.answer()
        await query.message.reply_text(
            "❌ You must join all channels to continue.\n\n"
            "Missing:\n" + "\n".join(not_joined)
        )
    else:
        verified_users.add(user_id)
        await query.answer()
        await query.message.reply_text(
            "✅ Verification successful!\n\n"
            "Now you can use all bot commands 🎉\n\n"
            "Type /menu"
        )

# ================= BLOCK OTHER COMMANDS =================

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in verified_users:
        await update.message.reply_text(
            "❌ You must join all channels to continue.\n\nUse /start"
        )
        return

    await update.message.reply_text(
        "📋 MAIN MENU\n\n"
        "• Feature 1\n"
        "• Feature 2\n"
        "• Feature 3"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in verified_users:
        await update.message.reply_text(
            "❌ Please verify first using /start"
        )
        return

    await update.message.reply_text(
        "ℹ️ Help Section\n\nContact admin if needed."
    )

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_cmd))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
