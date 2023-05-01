import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Application
import database as db
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext):
    welcome_message = (
        "¡Bienvenido al administrador de deudas! Aquí puedes agregar y gestionar tus deudas fácilmente usando comandos de Telegram. ¡Empecemos!\n\n"
        "Comandos disponibles:\n"
        "/add_debtor [nombre] - Agrega un nuevo deudor con el nombre proporcionado.\n"
        "/add_debt [nombre] [concepto] [monto] (fecha) - Agrega una deuda al deudor especificado. La fecha es opcional.\n"
        "/add_payment [nombre] [concpto] [monto] (nota) (fecha) - Agrega un pago al deudor especificado. La nota y la fecha son opcionales.\n"
        "/show_debtors_summary - Muestra un resumen de las deudas de todos los deudores.\n"
        "/show_debtor_details [nombre] - Muestra los detalles de la deuda del deudor especificado, incluidos los pagos realizados y el monto adeudado.\n"
    )
    await update.message.reply_text(welcome_message)


async def add_debtor(update: Update, context: CallbackContext):
    owner = update.message.from_user.username
    debtor_name = context.args[0]
    db.add_debtor(debtor_name, owner)
    await update.message.reply_text(f"Deudor '{debtor_name}' agregado.")


async def add_debt(update: Update, context: CallbackContext):
    owner = update.message.from_user.username
    debtor_name, concept, amount, *date = context.args
    amount = float(amount)
    date = date[0] if date else None
    db.add_debt(owner, debtor_name, concept, amount, date)
    await update.message.reply_text(
        f"Deuda de {amount} para '{debtor_name}' agregada en {date if date else 'hoy'} (concepto: {concept}).")


async def add_payment(update: Update, context: CallbackContext):
    owner = update.message.from_user.username
    debtor_name, concept, amount, *rest = context.args
    amount = float(amount)

    payment_date = None
    note = None

    for arg in rest:
        if note is None:
            note = arg
        else:
            try:
                date = datetime.strptime(arg, "%Y-%m-%d")
                payment_date = date.strftime("%Y-%m-%d")
            except ValueError:
                pass

    if payment_date is None:
        payment_date = datetime.now().strftime("%Y-%m-%d")

    db.add_payment(owner, debtor_name, concept, payment_date, amount, note)
    await update.message.reply_text(
        f"Abono de {amount} para '{debtor_name}' registrado en {payment_date} (concepto: {concept}){'' if note is None else f' - Nota: {note}'}.")


async def show_debtors_summary(update: Update, context: CallbackContext):
    owner = update.message.from_user.username
    debtors = db.get_all_debtors(owner)

    if not debtors:
        await update.message.reply_text("No tienes deudores registrados.")
        return

    message = "Resumen de deudores:\n\n"
    for debtor in debtors:
        debtor_name = debtor["name"]
        total_debt = sum([debt["amount"] for debt in debtor["debts"]])
        total_paid = sum([payment["amount"] for debt in debtor["debts"] for payment in debt["payments"]])
        remaining_balance = total_debt - total_paid
        message += f"{debtor_name}: Deuda total: {total_debt}, Total abonado: {total_paid}, Saldo restante: {remaining_balance}\n"

    await update.message.reply_text(message)


async def show_debtor_details(update: Update, context: CallbackContext):
    owner = update.message.from_user.username
    debtor_name = context.args[0]
    debtor = db.get_debtor(owner, debtor_name)

    if not debtor:
        await update.message.reply_text(f"No se encontró el deudor {debtor_name}")
        return

    total_debt = sum([debt["amount"] for debt in debtor["debts"]])
    total_paid = sum([payment["amount"] for debt in debtor["debts"] for payment in debt["payments"]])
    remaining_balance = total_debt - total_paid

    message = f"Información detallada de {debtor_name}:\n\n"
    message += f"Deuda total: {total_debt}\n"
    message += f"Total abonado: {total_paid}\n"
    message += f"Saldo restante: {remaining_balance}\n\n"

    if not debtor["debts"]:
        message += "No se encontraron deudas para este deudor."
    else:
        message += "Deudas:\n"
        for debt in debtor["debts"]:
            debt_message = f"{debt['amount']} - {debt['concept']}"
            if debt['payments']:
                paid_amount = sum([payment["amount"] for payment in debt["payments"]])
                debt_message += f", Abonado: {paid_amount}"
            message += f"{debt_message}\n"

    await update.message.reply_text(message)


def error(update: Update, context: CallbackContext):
    logger.warning(f'Update "{update}" caused error "{context.error}"')


def main():
    application = Application.builder().token("token").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_debtor", add_debtor))
    application.add_handler(CommandHandler("add_debt", add_debt))
    application.add_handler(CommandHandler("add_payment", add_payment))
    application.add_handler(CommandHandler("show_debtors_summary", show_debtors_summary))
    application.add_handler(CommandHandler("show_debtor_details", show_debtor_details))

    application.add_error_handler(error)

    application.run_polling()


if __name__ == '__main__':
    main()
