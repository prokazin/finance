import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Хранилище данных (простое, в памяти)
users_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users_data[user_id] = {"доходы": [], "расходы": [], "долги": []}
    await update.message.reply_text("👋 Привет! Я помогу вести твои финансы.\n\nКоманды:\n"
                                    "/add_income – добавить доход\n"
                                    "/add_expense – добавить расход\n"
                                    "/add_debt – добавить долг\n"
                                    "/close_debt – закрыть долг\n"
                                    "/report – показать отчёт")

async def add_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("💰 Введи сумму дохода: /add_income 50000")
        return
    amount = float(context.args[0])
    users_data[user_id]["доходы"].append(amount)
    await update.message.reply_text(f"✅ Доход {amount}₽ добавлен!")

async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("💸 Введи сумму расхода: /add_expense 2000")
        return
    amount = float(context.args[0])
    users_data[user_id]["расходы"].append(amount)
    await update.message.reply_text(f"💸 Расход {amount}₽ добавлен!")

async def add_debt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("📉 Введи сумму долга: /add_debt 15000")
        return
    amount = float(context.args[0])
    users_data[user_id]["долги"].append({"сумма": amount, "закрыт": False})
    await update.message.reply_text(f"📉 Долг {amount}₽ добавлен.")

async def close_debt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    debts = users_data[user_id]["долги"]
    open_debts = [d for d in debts if not d["закрыт"]]
    if not open_debts:
        await update.message.reply_text("✅ У тебя нет открытых долгов!")
        return
    open_debts[0]["закрыт"] = True
    await update.message.reply_text("💪 Один долг закрыт!")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = users_data[user_id]
    income = sum(data["доходы"])
    expense = sum(data["расходы"])
    debts_total = sum(d["сумма"] for d in data["долги"])
    debts_open = sum(d["сумма"] for d in data["долги"] if not d["закрыт"])
    balance = income - expense
    await update.message.reply_text(
        f"📊 Отчёт:\n"
        f"Доходы: {income}₽\n"
        f"Расходы: {expense}₽\n"
        f"Баланс: {balance}₽\n"
        f"Всего долгов: {debts_total}₽\n"
        f"Открытые долги: {debts_open}₽"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add_income", add_income))
app.add_handler(CommandHandler("add_expense", add_expense))
app.add_handler(CommandHandler("add_debt", add_debt))
app.add_handler(CommandHandler("close_debt", close_debt))
app.add_handler(CommandHandler("report", report))

if __name__ == "__main__":
    app.run_polling()
