import logging
import os
import threading
from flask import Flask, send_from_directory
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURAÇÕES DO BOT ---
TOKEN = "8851356392:AAFQiyL3sbWGSxjMCLqoiHfVX8ggtt-vpUc"
SUPPORT_LINK = "https://t.me/infocartoes"
PIX_CODE = "00020101021226810014br.gov.bcb.pix2559qr.woovi.com/qr/v2/cob/70404d48-e786-4aa1-b5d6-0cb75dde5825520400005303986540539.995802BR5906Madbot6012PORTO ALEGRE62290525e952769eef3e42f183b89d0276304CF4F"
# O Render define a URL automaticamente, mas usamos o domínio que você já tem
MINI_APP_URL = "https://pgssmartbot.onrender.com" 

# --- SERVIDOR WEB PARA O MINI APP ---
app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

def run_flask():
    # O Render usa a porta definida na variável de ambiente PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- LÓGICA DO BOT ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔍 *PRECISA ENCONTRAR ALGUÉM OU UM ENDEREÇO?* 📍\n\n"
        "Com o nosso *BOT DE CONSULTA DE DADOS*, você tem o poder da informação na palma da sua mão! 🚀\n\n"
        "👇 *ESCOLHA UMA OPÇÃO ABAIXO:*"
    )
    keyboard = [
        [InlineKeyboardButton("💎 COMPRAR ACESSO VITALÍCIO (R$ 39,99)", callback_data='buy')],
        [InlineKeyboardButton("🎁 CONSULTA GRÁTIS (ASSISTIR ANÚNCIO)", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'buy':
        text = "💎 *PAGAMENTO PIX*\n\nCopie o código abaixo e envie o comprovante no suporte.\n\n" + f"`{PIX_CODE}`"
        keyboard = [[InlineKeyboardButton("✅ ENVIAR COMPROVANTE", url=SUPPORT_LINK)], [InlineKeyboardButton("🔙 Voltar", callback_data='back_to_start')]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'back_to_start':
        await query.message.delete()
        await start(query.message, context)

def main():
    # Inicia o Flask em uma thread separada
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Inicia o Bot
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("Bot e Servidor Web iniciados com sucesso!")
    application.run_polling()

if __name__ == '__main__':
    main()
