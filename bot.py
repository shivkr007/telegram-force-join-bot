import os
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
    "https://t.me/Czarmy007"
]

verified_users = set()
# ==========================================

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in verified_users:
        await update.message.reply_text(
            "✅ You are already verified.\nUse /menu to continue."
        )
        return

    buttons = []
    for ch in CHANNELS:
        buttons.append([
            InlineKeyboardButton(
                text=f"📢 Join Channel",
                url=ch
            )
        ])
    buttons.append([InlineKeyboardButton("✅ Verify", callback_data="verify")])
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "👇 Please join all channels below and then click Verify:",
        reply_markup=reply_markup
    )

# VERIFY BUTTON
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    not_joined = []

    # Check using get_chat_member if possible
    for ch in CHANNELS:
        try:
            # Extract username from link if possible
            if "t.me/" in ch:
                username = ch.split("t.me/")[-1].replace("+","")
                member = await context.bot.get_chat_member(username, user_id)
                if member.status not in ["member", "administrator", "creator"]:
                    not_joined.append(ch)
        except:
            not_joined.append(ch)

    if not_joined:
        await query.answer()
        await query.message.reply_text(
            "❌ You must join all channels to continue.\nMissing:\n" +
            "\n".join(not_joined)
        )
    else:
        verified_users.add(user_id)
        await query.answer()
        await query.message.reply_text(
            "✅ Verification successful!\nNow you can use all bot commands 🎉\nType /menu"
        )

# MENU COMMAND (only for verified)
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in verified_users:
        await update.message.reply_text(
            "❌ You must join all channels to continue.\nUse /start"
        )
        return

    await update.message.reply_text(
        "📋 MAIN MENU\n• Feature 1\n• Feature 2\n• Feature 3"
    )

# HELP COMMAND
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in verified_users:
        await update.message.reply_text(
            "❌ Please verify first using /start"
        )
        return
    await update.message.reply_text("ℹ️ Help Section\nContact admin if needed.")

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

