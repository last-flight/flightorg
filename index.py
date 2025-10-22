import re, os, asyncio
from telethon import TelegramClient
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

API_ID = 20514298
API_HASH = "3d434c7ba192470ee2cb80c22e646090"
BOT_TOKEN = "8319559064:AAGdomnhiSqYWpd6igZHHwf2UgtAQYKNZUs"
SESSION_NAME = "session"

REQUIRED_CHANNELS = ["@texthamy", "@CatSelfCh"]

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

async def check_subscription_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("عضو شدن در کانال ♻️", url="https://t.me/texthamy"),
            InlineKeyboardButton("عضو شدن در کانال ♻️", url="https://t.me/CatSelfCh")
        ],
        [InlineKeyboardButton("«عضو شدم🙋🏻‍♂»", callback_data="check_subscription")]
    ])
    await update.effective_message.reply_text(
        "برای حمایت از ما لطفا داخل کانال های زیر عضو شوید و سپس لینک خود را ارسال کنید 👇🏼",
        reply_markup=keyboard
    )

async def subscription_check_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_user_subscribed(user_id, context):
        await query.answer("عضویت شما با موفقیت تایید شد . ✅", show_alert=True)
        try:
            await query.message.delete()
        except:
            pass
        await context.bot.send_message(
            chat_id=user_id,
            text="✅ عضویت شما تایید شد.\nسپاس از اینکه از ربات ما استفاده می‌کنید!\nلطفاً لینک محدود شده رو دوباره بفرستید تا براتون ارسالش کنم 🌚"
        )
    else:
        await query.answer("هنوز عضو کانال های ما نشدی .❗️", show_alert=True)

async def fetch_and_send(link: str, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    match = re.match(r'^(?:https?://)?t\.me/(c/\d+|[\w]+)(?:/\d+)?/(\d+)(?:\?.*)?$', link)
    if not match:
        return

    entity_part = match.group(1)
    msg_id = int(match.group(2))

    if entity_part.startswith("c/"):
        return

    try:
        target_msg = await client.get_messages(entity_part, ids=msg_id)
        if not target_msg:
            return

        if target_msg.media:
            file = await client.download_media(target_msg)
            try:
                with open(file, "rb") as f:
                    await context.bot.send_document(chat_id=user_id, document=f, caption=target_msg.text or "")
            except:
                pass
            finally:
                try:
                    if os.path.exists(file):
                        os.remove(file)
                except:
                    pass
        elif target_msg.text:
            await context.bot.send_message(chat_id=user_id, text=target_msg.text)

        await context.bot.send_message(chat_id=user_id, text='''
با موفقیت فوروارد شد به شما کاربر گرامی ✅  
محتوا با دقت و عشق آماده شده تا تجربه‌ی خوبی براتون رقم بزنه ✨  
اگه ازش خوشتون اومد، خوشحال می‌شم همراهش باشید و به اشتراک بذارید 💫  
آیدی ربات برای دسترسی مستقیم و راحت‌تر: @YourBotUsername 🤖  
ممنون که هستید و وقت گذاشتید 🌿''')
    except:
        return

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📢 کانال ما", url="https://t.me/coditeam"),
            InlineKeyboardButton("🌀 درباره ما", callback_data="about_us")
        ]
    ])

    await update.effective_message.reply_text('''سلام! 👋
💈با من میتونی فایل‌هایی که محدود شدن و اصطلاحاً قفل فوروارد و دانلود دارن رو براحتی و بدون مشکل دانلود و یا برای بقیه فوروارد کنی!

👈 فقط کافیه لینک پست یا اون فایل رو برام بفرستی تا بدون محدودیت و قفل برات بفرستمش!

(این ترفند فعلاً برای کانال‌ها یا گروه‌های عمومی جواب می‌ده!)
''', reply_markup=keyboard)

async def about_us_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about_us":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_start"),
                InlineKeyboardButton("📢 کانال ما", url="https://t.me/thegruuugd")
            ]
        ])

        await query.edit_message_text(
            text=('''
مایی در کار نیست 💭  
همه چی رو خودم، تکی و دلی پیش می‌برم ✨  
امیدوارم خوشتون بیاد و باهاش ارتباط بگیرید 🤍  
اگه سوال، انتقاد یا مشکلی داشتید، خوشحال می‌شم پیوی بگید 📨  
مرسی که هستید 🙏

آیدی من: @YeNu_ll 🔗'''),
            reply_markup=keyboard
        )

    elif query.data == "back_to_start":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📢 کانال ما", url="https://t.me/coditeam"),
                InlineKeyboardButton("🌀 درباره ما", callback_data="about_us")
            ]
        ])

        await query.edit_message_text(
            text=('''سلام! 👋
💈با من میتونی فایل‌هایی که محدود شدن و اصطلاحاً قفل فوروارد و دانلود دارن رو براحتی و بدون مشکل دانلود و یا برای بقیه فوروارد کنی!

👈 فقط کافیه لینک پست یا اون فایل رو برام بفرستی تا بدون محدودیت و قفل برات بفرستمش!

(این ترفند فعلاً برای کانال‌ها یا گروه‌های عمومی جواب می‌ده!)
'''),
            reply_markup=keyboard
        )

async def direct_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    user_id = update.effective_chat.id
    text = update.effective_message.text.strip()
    match = re.match(r'^(?:https?://)?t\.me/(c/\d+|[\w]+)(?:/\d+)?/(\d+)(?:\?.*)?$', text)
    if not match:
        return

    if not await is_user_subscribed(user_id, context):
        await check_subscription_prompt(update, context)
        return

    await fetch_and_send(text, user_id, context)

async def main():
    await client.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(about_us_handler, pattern="about_us|back_to_start"))
    app.add_handler(CallbackQueryHandler(subscription_check_handler, pattern="check_subscription"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, direct_link_handler))

    await app.initialize()
    await app.start()
    await asyncio.gather(
        client.run_until_disconnected(),
        app.updater.start_polling()
    )

asyncio.run(main())