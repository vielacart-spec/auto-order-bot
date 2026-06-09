from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

def format_rupiah(amount):
    return f"Rp {amount:,}".replace(",", ".")

def main_menu(name):
    saldo = 0

    text = (
        f"👋 Halo, {name}!\n\n"
        f"💰 Saldo: {format_rupiah(saldo)}\n\n"
        "Silakan pilih menu:"
    )

    keyboard = [
        [
            InlineKeyboardButton("💰 Saldo", callback_data="saldo"),
            InlineKeyboardButton("📦 Produk", callback_data="produk"),
        ],
        [
            InlineKeyboardButton("🛒 Pesanan", callback_data="pesanan"),
            InlineKeyboardButton("ℹ️ Informasi", callback_data="info"),
        ],
        [
            InlineKeyboardButton("👤 Profil", callback_data="profil"),
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
