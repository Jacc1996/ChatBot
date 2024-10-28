import logging
import re
from datetime import datetime  # Import datetime module
import pandas as pd  # Import pandas for CSV handling
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hola Líder! 🍺")  # Added beer emoji
    await update.message.reply_text("Por favor ingresa tu identificación.")
    context.user_data['awaiting_id'] = True

# Define the command handler for /press
async def press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Choose an option:\n1. Hi\n2. Bye\n\nType /start to restart the identification process.')

# Define the message handler for user responses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    if context.user_data.get('awaiting_id'):
        if re.match(r'^\d+$', user_message):
            context.user_data['identification_number'] = user_message
            await update.message.reply_text(f"Tu número de identificación {user_message} ha sido recibido.")
            await update.message.reply_text("Selecciona Área:\n1. Ambiental\n2. Seguridad")
            context.user_data['awaiting_id'] = False
            context.user_data['awaiting_area'] = True
        else:
            await update.message.reply_text("El número de identificación no es válido. No debes utilizar puntos, comas o letras.")
            await update.message.reply_text("Por favor ingresa tu identificación.")
    elif context.user_data.get('awaiting_area'):
        if user_message == '1' or user_message.lower() == 'ambiental':
            await update.message.reply_text('Seleccione Áctividad:\n1. Consumo\n2. Descarga\n3. Residuo Sólido')
            context.user_data['awaiting_area'] = False
            context.user_data['awaiting_activity'] = True
        elif user_message == '2' or user_message.lower() == 'seguridad':
            await update.message.reply_text('WORKING ON THIS /START')
            context.user_data['awaiting_area'] = False
        else:
            await update.message.reply_text('Por favor elige una opción válida:\n1. Ambiental\n2. Seguridad')
    elif context.user_data.get('awaiting_activity'):
        if user_message == '1' or user_message.lower() == 'consumo':
            await update.message.reply_text('Consumo: Seleccione Químico:\n1. Soda\n2. Ácido Clorhídrico\n3. Dióxido de Cloro')
            context.user_data['awaiting_activity'] = False
            context.user_data['awaiting_chemical'] = True
        elif user_message == '2' or user_message.lower() == 'descarga':
            await update.message.reply_text('WORKING ON THIS /START')
            context.user_data['awaiting_activity'] = False
        elif user_message == '3' or user_message.lower() == 'residuo sólido':
            await update.message.reply_text('WORKING ON THIS /START')
            context.user_data['awaiting_activity'] = False
        else:
            await update.message.reply_text('Por favor elige una opción válida:\n1. Consumo\n2. Descarga\n3. Residuo Sólido')
    elif context.user_data.get('awaiting_chemical'):
        if user_message == '1' or user_message.lower() == 'soda':
            await update.message.reply_text('Has seleccionado Soda.')
            context.user_data['chemical'] = 'Soda'
            context.user_data['awaiting_chemical'] = False
            await update.message.reply_text("Especifique la cantidad:")
            context.user_data['awaiting_quantity'] = True
        elif user_message == '2' or user_message.lower() == 'ácido clorhídrico':
            await update.message.reply_text('Has seleccionado Ácido Clorhídrico.')
            context.user_data['chemical'] = 'Ácido Clorhídrico'
            context.user_data['awaiting_chemical'] = False
            await update.message.reply_text("Especifique la cantidad:")
            context.user_data['awaiting_quantity'] = True
        elif user_message == '3' or user_message.lower() == 'dióxido de cloro':
            await update.message.reply_text('Has seleccionado Dióxido de Cloro.')
            context.user_data['chemical'] = 'Dióxido de Cloro'
            context.user_data['awaiting_chemical'] = False
            await update.message.reply_text("Especifique la cantidad:")
            context.user_data['awaiting_quantity'] = True
        else:
            await update.message.reply_text('Por favor elige una opción válida:\n1. Soda\n2. Ácido Clorhídrico\n3. Dióxido de Cloro')
    elif context.user_data.get('awaiting_quantity'):
        if re.match(r'^\d+$', user_message):
            context.user_data['quantity'] = user_message
            await update.message.reply_text(f"Has especificado la cantidad: {user_message}.")
            await update.message.reply_text("Especifique la unidad:\n1. SS\n2. kg")
            context.user_data['awaiting_quantity'] = False
            context.user_data['awaiting_unit'] = True
        else:
            await update.message.reply_text("La cantidad no es válida. Por favor especifique un número.")
    elif context.user_data.get('awaiting_unit'):
        if user_message == '1':
            unit = 'SS'
            context.user_data['unit'] = unit
            await update.message.reply_text(f'Has especificado la unidad: {unit}.')
            await confirm_request(update, context)
            context.user_data['awaiting_unit'] = False
        elif user_message == '2':
            unit = 'kg'
            context.user_data['unit'] = unit
            await update.message.reply_text(f'Has especificado la unidad: {unit}.')
            await confirm_request(update, context)
            context.user_data['awaiting_unit'] = False
        else:
            await update.message.reply_text("Por favor elija una opción válida:\n1. SS\n2. kg")
    elif context.user_data.get('awaiting_confirmation'):
        await handle_confirmation(update, context)
    else:
        await update.message.reply_text('Por favor elige una opción válida:\n1. Hi\n2. Bye')

async def confirm_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id_number = context.user_data.get('identification_number')
    activity = 'Consumo'  # Since only "Consumo" is handled here
    quantity = context.user_data.get('quantity')
    unit = context.user_data.get('unit')
    chemical = context.user_data.get('chemical')

    confirmation_message = (
        f"Usuario {id_number}, usted ha solicitado un(a) {activity} de {quantity} {unit} de {chemical}, por favor confirme su solicitud.\n"
        "1. ✅ Confirmar\n2. ❌ Cancelar"
    )
    
    await update.message.reply_text(confirmation_message)

    # Set the state to await confirmation
    context.user_data['awaiting_confirmation'] = True

async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    id_number = context.user_data.get('identification_number')
    activity = 'Consumo'
    quantity = context.user_data.get('quantity')
    unit = context.user_data.get('unit')
    chemical = context.user_data.get('chemical')

    # Get the current date and time
    confirmation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format datetime

    if user_message == '1':  # Confirmar
        await update.message.reply_text("Tu solicitud ha sido registrada en el sistema. Para realizar nuevamente solicitudes presiones /start")
        
        # Save to CSV
        save_to_csv(id_number, activity, quantity, unit, chemical, confirmation_time)
        
        context.user_data.clear()  # Clear user data after processing
    elif user_message == '2':  # Cancelar
        await update.message.reply_text("Tu solicitud ha sido cancelada. Para volver a realizar el proceso por favor presiones /start")
        context.user_data.clear()  # Clear user data after processing
    else:
        await update.message.reply_text("Por favor, elija una opción válida: 1 para confirmar, 2 para cancelar.")

def save_to_csv(id_number, activity, quantity, unit, chemical, confirmation_time):
    # Create a DataFrame with the data
    data = {
        'ID Number': [id_number],
        'Activity': [activity],
        'Quantity': [quantity],
        'Unit': [unit],
        'Chemical': [chemical],
        'Confirmation Time': [confirmation_time]
    }
    df = pd.DataFrame(data)

    # Append to CSV file
    try:
        df.to_csv('user_requests.csv', mode='a', index=False, header=not pd.io.common.file_exists('user_requests.csv'))
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# New handler for non-text messages
async def handle_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Lo siento, solo se permiten mensajes de texto.")

def main() -> None:
    app = ApplicationBuilder().token('YOUR TOKEN HERE').build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("press", press))
    
    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.ALL, handle_non_text))  # This will catch all non-text messages

    # Run the bot
    app.run_polling()

if __name__ == '__main__':
    main()
