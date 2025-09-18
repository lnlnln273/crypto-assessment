import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Thay bằng token của bạn
TOKEN = "8386151833:AAFhNuILsltkD8nk64tMWcD2pKQrwHRSsEE"

# Lệnh /start để test bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Gõ /run để chạy ứng dụng main.py 🚀")

# Lệnh /run sẽ gọi file main.py
async def run_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Gọi file main.py và lấy kết quả
        result = subprocess.run(
            ["python", "main.py"],  # gọi file main.py
            capture_output=True,
            text=True,
            check=True
        )

        output = result.stdout.strip()

        if not output:
            output = "⚠️ Ứng dụng không trả kết quả nào."

        await update.message.reply_text(f"Kết quả từ main.py:\n\n{output}")

    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"❌ Lỗi khi chạy main.py:\n{e.stderr}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run_app))

    app.run_polling()

if __name__ == "__main__":
    main()
