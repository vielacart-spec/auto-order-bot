from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7568261625

def get_greeting():
    hour = datetime.now(ZoneInfo("Asia/Jakarta")).hour

    if 0 <= hour < 5:
        return "Selamat Dini Hari"
    elif hour < 11:
        return "Selamat Pagi"
    elif hour < 15:
        return "Selamat Siang"
    elif hour < 18:
        return "Selamat Sore"
    else:
        return "Selamat Malam"

def get_wib_time():
    return datetime.now(
        ZoneInfo("Asia/Jakarta")
    ).strftime("%d %b %y - %H:%M:%S WIB")
    
def format_rupiah(amount):
    return f"Rp {amount:,}".replace(",", ".")

def main_menu(name):
    saldo = 0

    greeting = get_greeting()
    current_time = get_wib_time()

    text = (
    f"{greeting}, {name}\n\n"
    "OYCE STUFF\n\n"
    "1. Amazon Prime - 0 Stok\n"
    "2. Bstation - 0 Stok\n"
    "3. Canva - 0 Stok\n"
    "4. CapCut - 0 Stok\n"
    "5. ChatGPT - 0 Stok\n"
    "6. Gemini AI - 0 Stok\n"
    "7. Grok AI - 0 Stok\n"
    "8. Gsuite x Gopay - 0 Stok\n"
    "9. HBO - 0 Stok\n"
    "10. iQIYI - 0 Stok\n"
    "11. Kiro AI - 0 Stok\n"
    "12. Loklok - 0 Stok\n"
    "13. Meitu - 0 Stok\n"
    "14. Microsoft 365 - 0 Stok\n"
    "15. Notion AI - 0 Stok\n"
    f"{current_time}\n\n"
    "Shortcut Bot:\n"
    "/start - Menu"
)

    keyboard = [
    [InlineKeyboardButton("Saldo Rp 0", callback_data="saldo")],

    [
        InlineKeyboardButton("1", callback_data="p1"),
        InlineKeyboardButton("2", callback_data="p2"),
        InlineKeyboardButton("3", callback_data="p3"),
        InlineKeyboardButton("4", callback_data="p4"),
        InlineKeyboardButton("5", callback_data="p5"),
    ],

    [
        InlineKeyboardButton("6", callback_data="p6"),
        InlineKeyboardButton("7", callback_data="p7"),
        InlineKeyboardButton("8", callback_data="p8"),
        InlineKeyboardButton("9", callback_data="p9"),
        InlineKeyboardButton("10", callback_data="p10"),
    ],

    [
        InlineKeyboardButton("11", callback_data="p11"),
        InlineKeyboardButton("12", callback_data="p12"),
        InlineKeyboardButton("13", callback_data="p13"),
        InlineKeyboardButton("14", callback_data="p14"),
        InlineKeyboardButton("15", callback_data="p15"),
    ],

    [InlineKeyboardButton("Next", callback_data="next")],

    [InlineKeyboardButton("Absen", callback_data="absen")],

    [
        InlineKeyboardButton("Pesanan", callback_data="pesanan"),
        InlineKeyboardButton("Informasi", callback_data="info"),
    ],
]

    return text, InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "User"
    text, keyboard = main_menu(name)

    await update.message.reply_text(
        text,
        reply_markup=keyboard
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    name = query.from_user.first_name or "User"

if query.data == "next":
    await query.edit_message_text(
        "OYCE STUFF\n\n"
        "16. Picsart - 0 Stok\n"
        "17. Scribd - 0 Stok\n"
        "18. Simerah - 0 Stok\n"
        "19. Spotify - 0 Stok\n"
        "20. VPN Express - 0 Stok\n"
        "21. WeTV - 0 Stok\n"
        "22. Youku - 0 Stok\n"
        "23. YouTube - 0 Stok\n"
        "24. Zoom - 0 Stok",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("16", callback_data="p16"),
                InlineKeyboardButton("17", callback_data="p17"),
                InlineKeyboardButton("18", callback_data="p18"),
            ],
            [
                InlineKeyboardButton("19", callback_data="p19"),
                InlineKeyboardButton("20", callback_data="p20"),
                InlineKeyboardButton("21", callback_data="p21"),
            ],
            [
                InlineKeyboardButton("22", callback_data="p22"),
                InlineKeyboardButton("23", callback_data="p23"),
                InlineKeyboardButton("24", callback_data="p24"),
            ],
            [InlineKeyboardButton("Kembali", callback_data="menu")]
        ])
    )
    return
    if query.data == "saldo":
        await query.edit_message_text(
            "💰 Saldo Kamu\n\n"
            "Saldo saat ini: Rp 0\n\n"
            "Fitur top up saldo akan ditambahkan nanti.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu")]
            ])
        )

    elif query.data == "produk":
        await query.edit_message_text(
            "📦 Daftar Produk\n\n"
            "Produk belum tersedia.\n\n"
            "Admin nanti bisa menambahkan produk dari panel admin.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu")]
            ])
        )

    elif query.data == "pesanan":
        await query.edit_message_text(
            "🛒 Pesanan Kamu\n\n"
            "Belum ada pesanan.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu")]
            ])
        )

    elif query.data == "info":
        await query.edit_message_text(
            "ℹ️ Informasi\n\n"
            "Bot auto order reseller.\n"
            "Silakan pilih produk dan lakukan pembayaran sesuai instruksi.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu")]
            ])
        )

    elif query.data == "profil":
        await query.edit_message_text(
            f"👤 Profil Kamu\n\n"
            f"Nama: {name}\n"
            f"User ID: {query.from_user.id}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu")]
            ])
        )

    elif query.data == "menu":
        text, keyboard = main_menu(name)
        await query.edit_message_text(text, reply_markup=keyboard)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
