import logging
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# CONFIGURAÇÕES
TOKEN = "8851356392:AAFQiyL3sbWGSxjMCLqoiHfVX8ggtt-vpUc"
SUPPORT_LINK = "https://t.me/infocartoes"
PIX_CODE = "00020101021226810014br.gov.bcb.pix2559qr.woovi.com/qr/v2/cob/70404d48-e786-4aa1-b5d6-0cb75dde5825520400005303986540539.995802BR5906Madbot6012PORTO ALEGRE62290525e952769eef3e42f183b89d0276304CF4F"
AD_LINKS = ["https://omg10.com/4/11287749", "https://omg10.com/4/11291875", "https://omg10.com/4/11287749"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    text = "🔍 *BOT DE CONSULTA DE DADOS* 📍\n\nEscolha uma opção abaixo para começar:"
    kb = [[InlineKeyboardButton("💎 COMPRAR VITALÍCIO (R$ 39,99)", callback_data='buy')],
          [InlineKeyboardButton("🎁 CONSULTA GRÁTIS (ANÚNCIOS)", callback_data='ad_1')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'buy':
        await query.edit_message_text(f"💎 *PAGAMENTO PIX*\n\n`{PIX_CODE}`\n\nEnvie o comprovante: {SUPPORT_LINK}", parse_mode='Markdown')
    elif query.data.startswith('ad_'):
        step = int(query.data.split('_')[1])
        link = AD_LINKS[step-1]
        msg = await query.edit_message_text(f"🎁 *PASSO {step}/3*\n\n👉 [CLIQUE AQUI PARA VER O ANÚNCIO]({link})\n\n⏳ Validando anúncio em 20s...", parse_mode='Markdown')
        await asyncio.sleep(20)
        next_step = f'ad_{step+1}' if step < 3 else 'final'
        btn = "➡️ PRÓXIMO" if step < 3 else "🔓 LIBERAR"
        await msg.edit_text(f"✅ Anúncio {step} validado!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(btn, callback_data=next_step)]]), parse_mode='Markdown')
    elif query.data == 'final':
        await query.edit_message_text(f"🎉 *LIBERADO!*\n\nEnvie CPF/Nome no suporte: {SUPPORT_LINK}\nPrazo: 2 horas.", parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle))
    app.run_polling()

if __name__ == '__main__':
    main()
