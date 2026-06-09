import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.getenv("8977530157:AAFjGBFACBEaJA6O6SxngX3Ofui93MqCsqY")
ADMIN_ID = 7568261625
DB = "store.db"


def db():
    return sqlite3.connect(DB)


def init_db():
    con = db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        stock INTEGER DEFAULT 0,
        active INTEGER DEFAULT 1
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        status TEXT DEFAULT 'pending'
    )
    """)
    con.commit()
    con.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Produk", callback_data="products")],
        [InlineKeyboardButton("🧾 Riwayat Order", callback_data="history")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="help")]
    ]

    if update.effective_user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin")])

    await update.message.reply_text(
        "halo, selamat datang di bot auto order reseller.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "products":
        con = db()
        cur = con.cursor()
        cur.execute("SELECT id, name, price, stock FROM products WHERE active=1")
        products = cur.fetchall()
        con.close()

        if not products:
            await q.edit_message_text("produk belum tersedia.")
            return

        keyboard = []
        for p in products:
            keyboard.append([
                InlineKeyboardButton(
                    f"{p[1]} | Rp{p[2]:,} | Stok {p[3]}",
                    callback_data=f"order_{p[0]}"
                )
            ])

        keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="back")])
        await q.edit_message_text("pilih produk:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif q.data.startswith("order_"):
        product_id = int(q.data.split("_")[1])

        con = db()
        cur = con.cursor()
        cur.execute("SELECT name, price, stock FROM products WHERE id=?", (product_id,))
        product = cur.fetchone()

        if not product:
            await q.edit_message_text("produk tidak ditemukan.")
            return

        if product[2] <= 0:
            await q.edit_message_text("stok produk habis.")
            return

        cur.execute(
            "INSERT INTO orders (user_id, product_id, status) VALUES (?, ?, ?)",
            (q.from_user.id, product_id, "pending_payment")
        )
        order_id = cur.lastrowid
        con.commit()
        con.close()

        keyboard = [
            [InlineKeyboardButton("✅ Simulasi Sudah Bayar", callback_data=f"paid_{order_id}")]
        ]

        await q.edit_message_text(
            f"invoice #{order_id}\n\n"
            f"produk: {product[0]}\n"
            f"harga: Rp{product[1]:,}\n\n"
            f"silakan bayar via QRIS.\n"
            f"untuk versi test, klik tombol simulasi bayar.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif q.data.startswith("paid_"):
        order_id = int(q.data.split("_")[1])

        con = db()
        cur = con.cursor()
        cur.execute("""
            SELECT orders.product_id, products.name, products.stock
            FROM orders
            JOIN products ON orders.product_id = products.id
            WHERE orders.id=? AND orders.user_id=?
        """, (order_id, q.from_user.id))
        order = cur.fetchone()

        if not order:
            await q.edit_message_text("order tidak ditemukan.")
            return

        if order[2] <= 0:
            await q.edit_message_text("stok habis, hubungi admin.")
            return

        cur.execute("UPDATE products SET stock = stock - 1 WHERE id=?", (order[0],))
        cur.execute("UPDATE orders SET status='paid' WHERE id=?", (order_id,))
        con.commit()
        con.close()

        await q.edit_message_text(
            f"pembayaran berhasil.\n\n"
            f"order #{order_id}\n"
            f"produk: {order[1]}\n"
            f"status: paid\n\n"
            f"produk akan diproses otomatis/admin."
        )

        await context.bot.send_message(
            ADMIN_ID,
            f"order paid\n\ninvoice #{order_id}\nuser: {q.from_user.id}\nproduk: {order[1]}"
        )

    elif q.data == "admin":
        if q.from_user.id != ADMIN_ID:
            await q.edit_message_text("akses ditolak.")
            return

        await q.edit_message_text(
            "admin panel\n\n"
            "command:\n"
            "/addproduk nama|harga|stok\n\n"
            "contoh:\n"
            "/addproduk Netflix 1 Bulan|25000|10"
        )

    elif q.data == "history":
        con = db()
        cur = con.cursor()
        cur.execute("""
            SELECT orders.id, products.name, orders.status
            FROM orders
            JOIN products ON orders.product_id = products.id
            WHERE orders.user_id=?
            ORDER BY orders.id DESC
            LIMIT 10
        """, (q.from_user.id,))
        rows = cur.fetchall()
        con.close()

        if not rows:
            await q.edit_message_text("belum ada riwayat order.")
            return

        text = "riwayat order:\n\n"
        for r in rows:
            text += f"#{r[0]} - {r[1]} - {r[2]}\n"

        await q.edit_message_text(text)

    elif q.data == "back":
        await q.edit_message_text("ketik /start untuk kembali ke menu utama.")

    elif q.data == "help":
        await q.edit_message_text("gunakan tombol produk untuk mulai order.")


async def add_produk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = update.message.text.replace("/addproduk", "").strip()

    try:
        name, price, stock = text.split("|")
        price = int(price)
        stock = int(stock)
    except:
        await update.message.reply_text("format salah.\ncontoh: /addproduk Netflix 1 Bulan|25000|10")
        return

    con = db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
        (name.strip(), price, stock)
    )
    con.commit()
    con.close()

    await update.message.reply_text("produk berhasil ditambahkan.")


def main():
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addproduk", add_produk))
    app.add_handler(CallbackQueryHandler(buttons))

    app.run_polling()


if __name__ == "__main__":
    main()
