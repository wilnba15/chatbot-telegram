import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext

usuarios = {}

TOKEN = os.environ.get("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    usuarios[chat_id] = {"estado": "inicio", "datos": {}}
    update.message.reply_text("¡Hola! Soy el Asistente Virtual de Motor en Ventas 🚗\nEscribe 'menu' para comenzar.")

#####
def procesar(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    texto = update.message.text.strip().lower()

    if chat_id not in usuarios:
        usuarios[chat_id] = {"estado": "inicio", "datos": {}}

    estado = usuarios[chat_id]["estado"]
    datos = usuarios[chat_id]["datos"]

    def mostrar_menu():
        return (
            "¿En qué te gustaría que te apoye hoy?\n"
            "1. Conocer nuestros servicios\n"
            "2. Agendar asesoría gratuita\n"
            "3. Ver promociones y precios\n"
            "4. Descargar contenidos útiles\n"
            "5. Hablar con un asesor humano\n"
            "Digita: 1,2,3,4 o 5 segun lo que necesitas"
        )

    if texto in ["menú","menu", "inicio"]:
        usuarios[chat_id]["estado"] = "inicio"
        update.message.reply_text(mostrar_menu())
    elif estado == "inicio":
        if texto == "1":
            usuarios[chat_id]["estado"] = "menu_servicios"
            update.message.reply_text(
                "Ofrecemos servicios de marketing digital especializado, incluyendo:\n"
                "- Campañas en Meta, Google, TikTok, X\n"
                "- Diseño web optimizado (SEO/SEM)\n"
                "- Fotografía y video profesional\n"
                "- Branding y posicionamiento digital\n"
                "- COFEPRIS (salud)\n"
                "- Consultoría comercial y ventas\n"
                "\n¿Te gustaría agendar una asesoría gratuita?\n1. Sí, agendar asesoría\n2. Volver al menú principal"
            )
        elif texto == "2":
            usuarios[chat_id]["estado"] = "esperando_nombre"
            update.message.reply_text("¡Perfecto! Por favor, dime tu nombre completo:")
        elif texto == "3":
            usuarios[chat_id]["estado"] = "menu_promociones"
            update.message.reply_text(
                "Nuestros paquetes inician desde $4,500 MXN e incluyen:\n"
                "- 8 reels + 4 diseños de imagen\n"
                "- Sesión de foto y video\n"
                "- 2 campañas pagadas (Meta/Google)\n"
                "- Optimización de plataformas (Meta, TikTok, Google)\n"
                "\n¿Deseas más información?\n1. Sí, quiero más info\n2. Volver al menú principal"
            )
        elif texto == "4":
            update.message.reply_text(
                "Aquí tienes algunos contenidos que pueden ayudarte:\n"
                "📘 eBook gratuito: https://drive.google.com/file/d/1VCqn50grfCdWAGcXYJmBhcIilgbrSdE4/view\n"
                "🌐 Blog: https://www.motorenventas.com/"
            )
        elif texto == "5":
            usuarios[chat_id]["estado"] = "esperando_contacto"
            update.message.reply_text("Por favor, deja tu nombre y teléfono, y un asesor se comunicará contigo.")
        else:
            update.message.reply_text("No entendí tu mensaje. Escribe 'menu' para ver opciones.")
    elif estado == "menu_servicios":
        if texto == "1":
            usuarios[chat_id]["estado"] = "esperando_nombre"
            update.message.reply_text("¡Perfecto! Por favor, dime tu nombre completo:")
        elif texto == "2":
            usuarios[chat_id]["estado"] = "inicio"
            update.message.reply_text(mostrar_menu())
        else:
            update.message.reply_text("Por favor responde con 1 para agendar o 2 para volver al menú.")
    elif estado == "menu_promociones":
        if texto == "1":
            update.message.reply_text("¡Genial! Un asesor te brindará más información pronto. ¿Deseas volver al menú? (escribe 'menu')")
        elif texto == "2":
            usuarios[chat_id]["estado"] = "inicio"
            update.message.reply_text(mostrar_menu())
        else:
            update.message.reply_text("Por favor responde con 1 para más info o 2 para volver al menú.")
    elif estado == "esperando_nombre":
        datos["nombre"] = update.message.text
        usuarios[chat_id]["estado"] = "esperando_telefono"
        update.message.reply_text("Gracias. ¿Cuál es tu número de teléfono?")
    elif estado == "esperando_telefono":
        datos["telefono"] = update.message.text
        usuarios[chat_id]["estado"] = "esperando_email"
        update.message.reply_text("Perfecto. ¿Cuál es tu correo electrónico?")
    elif estado == "esperando_email":
        datos["email"] = update.message.text
        usuarios[chat_id]["estado"] = "esperando_giro"
        update.message.reply_text("¿Cuál es tu especialidad o giro comercial?")
    elif estado == "esperando_giro":
        datos["giro"] = update.message.text
        usuarios[chat_id]["estado"] = "esperando_fecha"
        update.message.reply_text("¿Qué fecha y hora deseas para la asesoría?")
    elif estado == "esperando_fecha":
        datos["fecha"] = update.message.text
        usuarios[chat_id]["estado"] = "final"
        update.message.reply_text(
            "✅ ¡Listo! Hemos registrado tu solicitud de asesoría:\n"
            f"📌 Nombre: {datos.get('nombre')}\n"
            f"📞 Teléfono: {datos.get('telefono')}\n"
            f"✉️ Email: {datos.get('email')}\n"
            f"🏢 Giro: {datos.get('giro')}\n"
            f"📅 Fecha deseada: {datos.get('fecha')}\n\n"
            "Un asesor te contactará pronto por WhatsApp para confirmarla.\n"
            "Gracias por tu interés en Motor en Ventas. 🚀"
        )
    elif estado == "esperando_contacto":
        update.message.reply_text("Gracias. Hemos recibido tus datos. Un asesor se pondrá en contacto contigo. ¿Deseas volver al menú?")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, procesar))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

#####


