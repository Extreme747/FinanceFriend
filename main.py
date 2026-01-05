#!/usr/bin/env python3
"""
LYRA - Founder Advisor / Operator
Telegram Bot powered by Gemini Pro AI
"""

import logging
import os
import asyncio
import random
from datetime import datetime, time, timedelta
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode, ChatAction

from bot_config import BotConfig
from gemini_client import GeminiClient
from data_manager import DataManager
from educational_content import EducationalContent
from user_manager import UserManager
from progress_tracker import ProgressTracker
from video_extractor import VideoExtractor
from utilities import (
    PriceTracker, NewsDigest, ReminderManager, PollManager,
    Watchlist, MotivationalContent, Leaderboard, GroupStats,
    GifManager, CurrencyConverter, TranslationHelper, TodoManager, Trivia
)
from penalty_system import PenaltyManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class CryptoStocksBot:

    def __init__(self):
        self.config = BotConfig()
        self.gemini = GeminiClient()
        self.data_manager = DataManager()
        self.educational_content = EducationalContent()
        self.user_manager = UserManager(self.data_manager)
        self.progress_tracker = ProgressTracker(self.data_manager)
        self.video_extractor = VideoExtractor()
        self.penalty_manager = PenaltyManager()
        self.tribute_enabled = True

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or not update.message: return
        user = update.effective_user
        user_info = self.user_manager.register_user(user_id=user.id,
                                                    username=user.username or "",
                                                    first_name=user.first_name or "Unknown",
                                                    chat_id=update.effective_chat.id)
        msg = f"Hey {user_info['display_name']}! I'm LYRA, your Founder Advisor. Use /help to see what I can do."
        await update.message.reply_text(msg)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message: return
        help_text = "LYRA Commands:\n/learn, /progress, /crypto, /stocks, /quiz, /penalty_status, /getvideo <link>"
        await update.message.reply_text(help_text)

    async def learn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or not update.message: return
        modules = self.educational_content.get_learning_modules()
        text = "📚 Modules:\n" + "\n".join([f"- /{m_id}: {m['title']}" for m_id, m in modules.items()])
        await update.message.reply_text(text)

    async def crypto_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or not update.message: return
        content = self.educational_content.get_crypto_basics()
        await update.message.reply_text(self._clean_markdown_response(content))

    async def stocks_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or not update.message: return
        content = self.educational_content.get_stocks_basics()
        await update.message.reply_text(self._clean_markdown_response(content))

    async def progress_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or not update.message: return
        progress = self.progress_tracker.get_user_progress(update.effective_user.id)
        await update.message.reply_text(f"Progress: {progress.get('overall_score', 0)}%")

    async def quiz_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message: return
        q = self.educational_content.get_random_quiz()
        text = f"🧠 {q['question']}\n" + "\n".join([f"{i+1}. {o}" for i, o in enumerate(q['options'])])
        await update.message.reply_text(text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or not update.message or not update.message.text: return
        text = update.message.text
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        chat_type = update.effective_chat.type

        user_info = self.user_manager.get_user_info(user_id)
        conversation_data = {'user_message': text, 'user_name': user_info.get('display_name', 'User'), 'timestamp': datetime.now().isoformat(), 'user_id': user_id, 'chat_id': chat_id, 'chat_type': chat_type}

        is_proactive = False
        if chat_type in ['group', 'supergroup']:
            bot_username = context.bot.username
            is_mentioned = f"@{bot_username}" in text if bot_username else False
            is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user and update.message.reply_to_message.from_user.is_bot
            is_called = "lyra" in text.lower()
            
            self.data_manager.store_group_conversation(chat_id, conversation_data)
            
            if is_mentioned or is_reply or is_called:
                is_proactive = False
            else:
                history = self.data_manager.get_group_memories(chat_id)[-10:]
                if not self._should_jump_in(text, history): return
                is_proactive = True

        memories = self.data_manager.get_group_memories(chat_id) if chat_type in ['group', 'supergroup'] else self.data_manager.get_user_memories(user_id)
        context_prompt = self._build_context_prompt(user_info, memories, text, chat_type, is_proactive)

        try:
            await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            ai_res = await self.gemini.get_educational_response(context_prompt)
            if not ai_res or "[SILENCE]" in ai_res: return
            
            conversation_data['ai_response'] = ai_res
            if chat_type in ['group', 'supergroup']: self.data_manager.store_group_conversation(chat_id, conversation_data)
            self.data_manager.store_conversation(user_id, conversation_data)

            clean_res = self._clean_markdown_response(ai_res)
            if is_proactive: await context.bot.send_message(chat_id=chat_id, text=clean_res)
            else: await update.message.reply_text(clean_res)
        except Exception as e:
            logger.error(f"AI Error: {e}")

    def _should_jump_in(self, text: str, history: list) -> bool:
        triggers = ['crypto', 'stocks', 'penalty', 'profit', 'loss', 'market', 'strategy', 'startup', 'kaam']
        if any(t in text.lower() for t in triggers): return True
        return random.random() < 0.15

    def _build_context_prompt(self, user_info, memories, current_message, chat_type='private', is_proactive=False):
        team_context = ""
        if chat_type in ['group', 'supergroup']:
            team_context = "Team: Extreme (Leader, ID: 5587821011), Neel (@Er_Stranger), Nex (@Nexxxyzz), Pramod (@pr_amod18)."
        
        return f"""
NAME: LYRA (Founder Advisor). Energy: Boardroom + Street. Hinglish.
{team_context}
Proactive: {'ON' if is_proactive else 'OFF'}. If ON, jump in only if strategic value exists.
History: {self._format_memories(memories)}
User {user_info.get('display_name')}: {current_message}
"""

    def _format_memories(self, memories):
        return "\n".join([f"{m.get('user_name')}: {m.get('user_message')}\nLYRA: {m.get('ai_response')}" for m in memories[-5:]])

    def _clean_markdown_response(self, response):
        import re
        return re.sub(r'[*_`]', '', response)

    async def getvideo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not context.args: return
        url = context.args[0]
        msg = await update.message.reply_text("🔄 Extracting...")
        try:
            res = await self.video_extractor.extract_video(url)
            if res['success']:
                with open(res['video_path'], 'rb') as v: await update.message.reply_video(v)
                os.remove(res['video_path'])
                await msg.delete()
            else: await msg.edit_text(res['error'])
        except Exception as e: await msg.edit_text(f"Error: {e}")

    async def penalty_initial_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or not self.penalty_manager.is_authorized(update.effective_user.id): return
        res = self.penalty_manager.start_penalty()
        await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=res['sticker'])
        await update.message.reply_text(f"💀 PENALTY STARTED! @Er_Stranger Target: Neel. Amount: ₹{res['amount']}. LYRA is watching!")

    async def penalty_done_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or not self.penalty_manager.is_authorized(update.effective_user.id): return
        res = self.penalty_manager.complete_penalty()
        await update.message.reply_text(res['message'])

    async def post_init(self, app):
        cmds = [("start", "Start"), ("help", "Help"), ("learn", "Learn"), ("crypto", "Crypto"), ("stocks", "Stocks"), ("progress", "Progress"), ("quiz", "Quiz"), ("getvideo", "Video"), ("penalty_initial", "Penalty"), ("penalty_done", "Done")]
        await app.bot.set_my_commands([BotCommand(c[0], c[1]) for c in cmds])

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token: return
    bot = CryptoStocksBot()
    app = Application.builder().token(token).post_init(bot.post_init).build()
    handlers = ["start", "help", "learn", "crypto", "stocks", "progress", "quiz", "getvideo", "penalty_initial", "penalty_done"]
    for h in handlers: app.add_handler(CommandHandler(h, getattr(bot, h + "_command" if hasattr(bot, h + "_command") else h)))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
