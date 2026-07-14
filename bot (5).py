import logging
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variáveis do usuário
PIX_CODE = "00020101021226810014br.gov.bcb.pix2559qr.woovi.com/qr/v2/cob/70404d48-e786-4aa1-b5d6-0cb75dde5825520400005303986540539.995802BR5906Madbot6012PORTO ALEGRE62290525e952769eef3e42f183b89d0276304CF4F"
SUPPORT_LINK = "https://t.me/infocartoes"
NOTIFICATION_GROUP_ID = "-1002363784110" # ID do grupo extraído do link fornecido ou aproximado
# Como o link é privado (+bldFn6Dyz6szMjg5), o bot precisa estar no grupo como admin para enviar.
AD_LINK_1 = "https://omg10.com/4/11287749"
AD_LINK_2 = "https://omg10.com/4/11291875"
AD_LINK_3 = "https://omg10.com/4/11287749"

WAIT_TIME = 20 # Segundos de espera obrigatória

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = (
        "🔍 *PRECISA ENCONTRAR ALGUÉM OU UM ENDEREÇO?* 📍\n\n"
        "Com o nosso *BOT DE CONSULTA DE DADOS*, você tem o poder da informação na palma da sua mão! 🚀\n\n"
        "👇 *ESCOLHA UMA OPÇÃO ABAIXO:*"
    )
    keyboard = [
        [InlineKeyboardButton("💎 COMPRAR ACESSO VITALÍCIO (R$ 39,99)", callback_data='buy_lifetime')],
        [InlineKeyboardButton("🎁 ASSISTIR 3 COMERCIAIS E LIBERAR GRÁTIS", callback_data='ad_step_1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Notificação de entrada no grupo
    try:
        # Tenta enviar para o chat ID do grupo (ajustar conforme necessário se o bot for admin)
        # Usaremos o link direto para facilitar o acesso se o ID falhar
        notification_text = f"👤 *Novo Usuário:* {user.full_name} (@{user.username})\n🆔 ID: `{user.id}`\n🚀 Acabou de iniciar o bot!"
        await context.bot.send_message(chat_id="-1002363784110", text=notification_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {e}")

    try:
        with open('/home/ubuntu/upload/bot_consulta_dados.png', 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception:
        await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'buy_lifetime':
        text = "💎 *PAGAMENTO PIX*\n\nCopie o código abaixo e envie o comprovante no suporte.\n\n" + f"`{PIX_CODE}`"
        keyboard = [[InlineKeyboardButton("✅ ENVIAR COMPROVANTE", url=SUPPORT_LINK)], [InlineKeyboardButton("🔙 Voltar", callback_data='back_to_start')]]
        try:
            with open('/home/ubuntu/upload/pasted_file_3cUiWb_image.png', 'rb') as photo:
                await query.message.reply_photo(photo=photo, caption=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        except Exception:
            await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data.startswith('ad_step_'):
        step = int(query.data.split('_')[-1])
        links = [AD_LINK_1, AD_LINK_2, AD_LINK_3]
        current_link = links[step-1]
        
        await query.edit_message_caption(caption=f"⏳ *Validando anúncio...*", reply_markup=None) if query.message.photo else await query.edit_message_text(text=f"⏳ *Validando anúncio...*", reply_markup=None)
        
        text = (
            f"🎁 *PASSO {step} DE 3*\n\n"
            f"👉 [CLIQUE AQUI PARA ASSISTIR AO COMERCIAL]({current_link})\n\n"
            "⚠️ *O sistema está validando sua visualização.* Não feche o anúncio!"
        )
        
        msg = await query.edit_message_caption(caption=text, reply_markup=None, parse_mode='Markdown') if query.message.photo else await query.edit_message_text(text=text, reply_markup=None, parse_mode='Markdown')
        
        for i in range(WAIT_TIME, 0, -1):
            new_text = text + f"\n\n⏳ *Validando anúncio {i} segundos...*"
            try:
                await msg.edit_caption(caption=new_text, parse_mode='Markdown') if query.message.photo else await msg.edit_text(text=new_text, parse_mode='Markdown')
            except: pass
            await asyncio.sleep(1)
        
        next_call = f'ad_step_{step+1}' if step < 3 else 'unlock_final'
        btn_text = "➡️ PRÓXIMO PASSO" if step < 3 else "🔓 LIBERAR CONSULTA"
        
        keyboard = [[InlineKeyboardButton(btn_text, callback_data=next_call)]]
        final_text = text + "\n\n✅ *Anúncio validado! Clique abaixo para continuar.*"
        await msg.edit_caption(caption=final_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown') if query.message.photo else await msg.edit_text(text=final_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'unlock_final':
        text = (
            "🎉 *SISTEMA LIBERADO!*\n\n"
            "Você concluiu todos os anúncios com sucesso.\n\n"
            "⚠️ *INSTRUÇÃO:* Assim que você entrar em contato, envie o **CPF ou Nome Completo**. "
            "Iremos enviar sua consulta grátis em até **2 horas**.\n\n"
            "👇 *CLIQUE ABAIXO PARA SOLICITAR:*"
        )
        keyboard = [[InlineKeyboardButton("💬 SOLICITAR CONSULTA GRÁTIS", url=SUPPORT_LINK)], [InlineKeyboardButton("🔙 Início", callback_data='back_to_start')]]
        await query.edit_message_caption(caption=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown') if query.message.photo else await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'back_to_start':
        await query.message.delete()
        await start(query.message, context)

def main() -> None:
    token = "8851356392:AAFQiyL3sbWGSxjMCLqoiHfVX8ggtt-vpUc"
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Bot reiniciado com as novas configurações!")
    application.run_polling()

if __name__ == '__main__':
    main()
