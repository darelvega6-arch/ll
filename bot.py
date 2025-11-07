import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from video_processor import VideoProcessor
from progress_animator import ProgressAnimator
from config import TELEGRAM_TOKEN, SUPPORTED_LANGUAGES, MAX_VIDEO_SIZE_MB, TEMP_DIR, OUTPUT_DIR

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

processor = None
user_videos = {}
animator = ProgressAnimator()

def get_processor():
    global processor
    if processor is None:
        logger.info("🚀 Inicializando modelos de IA...")
        processor = VideoProcessor()
    return processor

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 *Bot de Doblaje de Videos con IA* 🎬\n\n"
        "Envíame un video y lo doblaré al idioma que elijas usando IA para clonar las voces originales.\n\n"
        "Comandos:\n"
        "/start - Iniciar el bot\n"
        "/help - Ayuda\n"
        "/languages - Ver idiomas disponibles\n\n"
        "Simplemente envía un video para comenzar!",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *Cómo usar el bot:*\n\n"
        "1. Envía un video (máx. 50MB)\n"
        "2. Selecciona el idioma de destino\n"
        "3. Espera mientras proceso el video\n"
        "4. Recibe tu video doblado!\n\n"
        "*Características:*\n"
        "✅ Clonación de voz con IA\n"
        "✅ Traducción automática\n"
        "✅ Sincronización perfecta\n"
        "✅ 10+ idiomas soportados",
        parse_mode='Markdown'
    )

async def languages_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    langs = "\n".join([f"• {code}: {name}" for code, name in SUPPORTED_LANGUAGES.items()])
    await update.message.reply_text(
        f"🌍 *Idiomas disponibles:*\n\n{langs}",
        parse_mode='Markdown'
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    
    if video.file_size > MAX_VIDEO_SIZE_MB * 1024 * 1024:
        await update.message.reply_text(f"❌ El video es muy grande. Máximo: {MAX_VIDEO_SIZE_MB}MB")
        return
    
    await update.message.reply_text("📥 Descargando video...")
    
    file = await context.bot.get_file(video.file_id)
    video_path = os.path.join(TEMP_DIR, f"{update.message.chat_id}_{video.file_id}.mp4")
    await file.download_to_drive(video_path)
    
    user_videos[update.message.chat_id] = video_path
    
    keyboard = []
    for code, name in SUPPORTED_LANGUAGES.items():
        keyboard.append([InlineKeyboardButton(name, callback_data=f"lang_{code}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌍 *Paso 1:* Selecciona el idioma de destino:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat_id = query.message.chat_id
    
    if chat_id not in user_videos:
        await query.edit_message_text("❌ Error: Video no encontrado. Envía un video nuevamente.")
        return
    
    # Si es selección de idioma, preguntar por audio de fondo
    if data.startswith('lang_'):
        target_lang = data.split('_')[1]
        context.user_data['target_lang'] = target_lang
        
        keyboard = [
            [InlineKeyboardButton("🎵 Sí, mantener música/sonidos de fondo", callback_data="bg_yes")],
            [InlineKeyboardButton("🔇 No, solo voces dobladas", callback_data="bg_no")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"🎚️ *Paso 2:* ¿Mantener el audio de fondo?\n\n"
            f"(música, efectos de sonido, ambiente)\n\n"
            f"Idioma seleccionado: {SUPPORTED_LANGUAGES[target_lang]}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Si es selección de fondo, procesar video
    if data.startswith('bg_'):
        keep_background = (data == 'bg_yes')
        target_lang = context.user_data.get('target_lang', 'es')
        
        video_path = user_videos[chat_id]
        output_path = os.path.join(OUTPUT_DIR, f"dubbed_{chat_id}_{target_lang}.mp4")
        
        bg_text = "con audio de fondo" if keep_background else "solo voces"
        progress_message = await query.edit_message_text(
            animator.format_progress_message('extracting', 'Iniciando proceso', 0, bg_text),
            parse_mode='Markdown'
        )
        
        try:
            # Animación: Extrayendo audio
            asyncio.create_task(
                animator.animate_progress(progress_message, 'extracting', 'Extrayendo audio', 2)
            )
            await asyncio.sleep(2)
            
            # Animación: Separando audio
            asyncio.create_task(
                animator.animate_progress(progress_message, 'separating', 'Separando voces y fondo', 3)
            )
            await asyncio.sleep(3)
            
            # Animación: Detectando hablantes
            asyncio.create_task(
                animator.animate_progress(progress_message, 'detecting', 'Detectando hablantes', 2)
            )
            await asyncio.sleep(2)
            
            # Animación: Transcribiendo
            asyncio.create_task(
                animator.animate_progress(progress_message, 'transcribing', 'Transcribiendo con Whisper AI', 4)
            )
            await asyncio.sleep(4)
            
            # Animación: Traduciendo
            asyncio.create_task(
                animator.animate_progress(progress_message, 'translating', 'Traduciendo texto', 2)
            )
            await asyncio.sleep(2)
            
            # Animación: Clonando voz
            asyncio.create_task(
                animator.animate_progress(progress_message, 'cloning', 'Clonando voz con emociones', 5)
            )
            
            proc = get_processor()
            result_path, num_speakers, emotion = proc.process_video(
                video_path,
                target_lang,
                output_path,
                keep_background,
                None
            )
            
            # Animación: Finalizando
            await animator.animate_progress(progress_message, 'finalizing', 'Finalizando video', 2)
        
            await progress_message.edit_text("📤 Enviando video doblado...")
            
            speakers_text = f"{num_speakers} hablante(s)"
            bg_text = "🎵 Con audio de fondo" if keep_background else "🔇 Solo voces"
            emotion_emoji = {'neutral': '😐', 'happy': '😄', 'sad': '😢', 'angry': '😡', 'excited': '🤩'}
            emotion_text = f"{emotion_emoji.get(emotion, '🎭')} Emoción: {emotion.upper()}"
            
            with open(result_path, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=chat_id,
                    video=video_file,
                    caption=f"✨ *¡VIDEO DOBLADO EXITOSAMENTE!* ✨\n\n"
                            f"🌍 *Idioma:* {SUPPORTED_LANGUAGES[target_lang]}\n"
                            f"👥 *Hablantes:* {speakers_text}\n"
                            f"{emotion_text}\n"
                            f"{bg_text}\n\n"
                            f"🎤 Voz clonada con IA\n"
                            f"✅ Calidad profesional",
                    parse_mode='Markdown'
                )
            
            await progress_message.edit_text("✅ ¡Proceso completado!")
            
            os.remove(video_path)
            os.remove(result_path)
            del user_videos[chat_id]
            
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            await progress_message.edit_text(f"❌ Error al procesar el video: {str(e)}")
        return

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    
    if document.mime_type and document.mime_type.startswith('video/'):
        if document.file_size > MAX_VIDEO_SIZE_MB * 1024 * 1024:
            await update.message.reply_text(f"❌ El video es muy grande. Máximo: {MAX_VIDEO_SIZE_MB}MB")
            return
        
        await update.message.reply_text("📥 Descargando video...")
        
        file = await context.bot.get_file(document.file_id)
        video_path = os.path.join(TEMP_DIR, f"{update.message.chat_id}_{document.file_id}.mp4")
        await file.download_to_drive(video_path)
        
        user_videos[update.message.chat_id] = video_path
        
        keyboard = []
        for code, name in SUPPORTED_LANGUAGES.items():
            keyboard.append([InlineKeyboardButton(name, callback_data=f"lang_{code}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🌍 *Paso 1:* Selecciona el idioma de destino:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("languages", languages_command))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(CallbackQueryHandler(handle_language_selection))
    
    logger.info("🤖 Bot iniciado...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
