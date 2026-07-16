import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------- Logging ----------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- Config ----------
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN environment variable is not set. "
        "Set it in your .env file (local) or in Railway's Variables tab (deployed)."
    )

# ---------- Rule-based responses ----------
RULES = {
    "hello": "Hey there! 👋 How can I help you today?",
    "hi": "Hi! 👋",
    "help": (
        "Here's what I can do:\n"
        "/start - Greet you\n"
        "/help - Show this message\n"
        "Or just say hello, thanks, or ask about the project!"
    ),
    "thanks": "You're welcome! 😊",
    "thank you": "Anytime! 😊",
    "bye": "See you later! 👋",
    "project": "This bot is part of a project — ask me anything and I'll do my best to help!",
}

DEFAULT_REPLY = (
    "I didn't quite catch that. Try /help to see what I can do, "
    "or just say hello!"
)


def get_rule_based_reply(text: str) -> str:
    text_lower = text.lower().strip()
    for keyword, reply in RULES.items():
        if keyword in text_lower:
            return reply
    return DEFAULT_REPLY


# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Welcome, {user.first_name}! 🎉\nI'm ttosinbot. Type /help to see what I can do."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(get_rule_based_reply("help"))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    reply = get_rule_based_reply(text)
    await update.message.reply_text(reply)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update %s caused error %s", update, context.error)


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
