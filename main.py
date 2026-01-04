#!/usr/bin/env python3
"""
Crypto & Stocks Educational Telegram Bot with Gemini Pro AI
Features: Persistent memory, progress tracking, educational content
"""

import logging
import os
import asyncio
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
        self.tribute_task = None
        self.tribute_enabled = True  # Auto-start tribute

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        if not update.effective_user or not update.effective_chat:
            return

        user = update.effective_user
        chat_id = update.effective_chat.id

        # Register user
        user_info = self.user_manager.register_user(user_id=user.id,
                                                    username=user.username
                                                    or "",
                                                    first_name=user.first_name
                                                    or "Unknown",
                                                    chat_id=chat_id)

        welcome_message = f"""🚀 Welcome to Crypto & Stocks Learning Bot! 

Hey {user_info['display_name']}! I'm LYRA, your friendly AI tutor powered by Gemini Pro. I'm here to help you learn about cryptocurrency and stock trading! 

🎯 What I can do:
• Teach you crypto and stocks fundamentals
• Remember our conversations and your progress
• Provide personalized learning experiences
• Track your learning milestones
• Be your supportive learning companion

📚 Available Commands:
/help - Show all commands
/learn - Start learning modules
/progress - Check your learning progress
/crypto - Learn about cryptocurrency
/stocks - Learn about stock trading
/quiz - Take a knowledge quiz
/reset - Reset your progress

Let's start your financial education journey! What would you like to learn about first?"""

        if update.message:
            clean_welcome = self._clean_markdown_response(welcome_message)
            await update.message.reply_text(clean_welcome)

    async def help_command(self, update: Update,
                           context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        if not update.message:
            return
        help_text = """
🤖 **Crypto & Stocks Learning Bot - Commands**

**Learning Commands:**
/learn - Browse available learning modules
/crypto - Cryptocurrency fundamentals
/stocks - Stock trading basics
/quiz - Test your knowledge
/progress - View your learning progress

**Interactive Commands:**
/ask [question] - Ask me anything about crypto/stocks
/explain [topic] - Get detailed explanations
/tips - Get daily trading tips

**Progress Commands:**
/stats - View detailed statistics
/achievements - See your achievements
/reset - Reset your learning progress

**Utility Commands:**
/help - Show this help message
/start - Restart the bot

💡 **Tip:** You can also just chat with me naturally! Call me LYRA and I'll remember our conversations and help you learn step by step.
        """

        clean_help = self._clean_markdown_response(help_text)
        await update.message.reply_text(clean_help)

    async def learn_command(self, update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
        """Learning modules command"""
        if not update.effective_user or not update.message:
            return
        user_id = update.effective_user.id
        modules = self.educational_content.get_learning_modules()
        user_progress = self.progress_tracker.get_user_progress(user_id)

        message = "📚 **Available Learning Modules:**\n\n"

        for module_id, module in modules.items():
            status = "✅" if module_id in user_progress.get(
                'completed_modules', []) else "📖"
            message += f"{status} {module['title']}\n"
            message += f"   - {module['description']}\n"
            message += f"   - Use: /{module_id}\n\n"

        clean_message = self._clean_markdown_response(message)
        await update.message.reply_text(clean_message)

    async def crypto_command(self, update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
        """Cryptocurrency learning command"""
        if not update.effective_user or not update.message:
            return
        user_id = update.effective_user.id
        content = self.educational_content.get_crypto_basics()

        self.progress_tracker.update_progress(user_id, 'crypto_basics',
                                              'started')

        clean_content = self._clean_markdown_response(content)
        await update.message.reply_text(clean_content)

    async def stocks_command(self, update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
        """Stock trading learning command"""
        if not update.effective_user or not update.message:
            return
        user_id = update.effective_user.id
        content = self.educational_content.get_stocks_basics()

        self.progress_tracker.update_progress(user_id, 'stocks_basics',
                                              'started')

        clean_content = self._clean_markdown_response(content)
        await update.message.reply_text(clean_content)

    async def progress_command(self, update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
        """Progress tracking command"""
        if not update.effective_user or not update.message:
            return
        user_id = update.effective_user.id
        user_info = self.user_manager.get_user_info(user_id)
        progress = self.progress_tracker.get_user_progress(user_id)

        display_name = user_info.get('display_name', 'Student')

        message = f"📊 Learning Progress for {display_name}\n\n"
        message += f"🎯 Overall Progress: {progress.get('overall_score', 0)}%\n"
        message += f"📅 Days Learning: {progress.get('days_active', 0)}\n"
        message += f"🏆 Completed Modules: {len(progress.get('completed_modules', []))}\n"
        message += f"❓ Quizzes Taken: {progress.get('quizzes_completed', 0)}\n\n"

        if progress.get('recent_topics'):
            message += "📚 Recent Topics:\n"
            for topic in progress['recent_topics'][-5:]:
                message += f"• {topic}\n"

        if progress.get('achievements'):
            message += "\n🏅 Achievements:\n"
            for achievement in progress['achievements']:
                message += f"🏆 {achievement}\n"

        clean_message = self._clean_markdown_response(message)
        await update.message.reply_text(clean_message)

    async def quiz_command(self, update: Update,
                           context: ContextTypes.DEFAULT_TYPE):
        """Quiz command"""
        if not update.message:
            return
        quiz_question = self.educational_content.get_random_quiz()

        message = f"🧠 Quiz Time!\n\n"
        message += f"Question: {quiz_question['question']}\n\n"

        for i, option in enumerate(quiz_question['options'], 1):
            message += f"{i}. {option}\n"

        message += f"\n💡 Reply with the number of your answer!"

        clean_message = self._clean_markdown_response(message)
        await update.message.reply_text(clean_message)

    async def reset_command(self, update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
        """Reset progress command"""
        if not update.effective_user or not update.message:
            return
        user_id = update.effective_user.id
        self.progress_tracker.reset_user_progress(user_id)

        reset_message = "Progress Reset Complete! Your learning progress has been reset. Ready to start fresh! Use /learn to begin again."
        await update.message.reply_text(reset_message)

    # Learning module specific handlers
    async def blockchain_command(self, update: Update,
                                 context: ContextTypes.DEFAULT_TYPE):
        """Blockchain learning command"""
        if not update.effective_user or not update.message:
            return
        user_id = update.effective_user.id
        content = self.educational_content.get_blockchain_content()
        self.progress_tracker.update_progress(user_id, 'blockchain', 'started')
        clean_content = self._clean_markdown_response(content)
        await update.message.reply_text(clean_content)

    async def technical_analysis_command(self, update: Update,
                                         context: ContextTypes.DEFAULT_TYPE):
        """Technical analysis learning command"""
        if not update.effective_user or not update.message:
            return
        user_id = update.effective_user.id
        content = self.educational_content.get_technical_analysis_content()
        self.progress_tracker.update_progress(user_id, 'technical_analysis',
                                              'started')
        clean_content = self._clean_markdown_response(content)
        await update.message.reply_text(clean_content)

    async def risk_management_command(self, update: Update,
                                      context: ContextTypes.DEFAULT_TYPE):
        """Risk management learning command"""
        if not update.effective_user or not update.message:
            return
        user_id = update.effective_user.id
        content = self.educational_content.get_risk_management_content()
        self.progress_tracker.update_progress(user_id, 'risk_management',
                                              'started')
        clean_content = self._clean_markdown_response(content)
        await update.message.reply_text(clean_content)

    async def handle_message(self, update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
        """Handle general messages with Gemini AI"""
        if not update.effective_user or not update.message or not update.message.text:
            return

        message_text = update.message.text

        # In group chats, only respond if bot is mentioned, replied to, or called by name "LYRA"
        if update.message.chat.type in ['group', 'supergroup']:
            bot_username = context.bot.username
            is_mentioned = f"@{bot_username}" in message_text if bot_username else False
            is_reply_to_bot = (
                update.message.reply_to_message
                and update.message.reply_to_message.from_user
                and update.message.reply_to_message.from_user.is_bot)
            is_called_by_name = "lyra" in message_text.lower(
            ) or "LYRA" in message_text

            if not (is_mentioned or is_reply_to_bot or is_called_by_name):
                return

        user = update.effective_user
        user_id = user.id
        chat_id = update.message.chat.id

        # Get user info for display name
        user_info = self.user_manager.get_user_info(user_id)
        display_name = user_info.get('display_name', user.first_name
                                     or 'Unknown')

        # Store the conversation with chat context
        conversation_data = {
            'user_message': message_text,
            'user_name': display_name,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'chat_id': chat_id,
            'chat_type': update.message.chat.type
        }

        # Get memories based on chat type
        if update.message.chat.type in ['group', 'supergroup']:
            # For group chats, get group conversation history
            group_memories = self.data_manager.get_group_memories(chat_id)
            user_memories = self.data_manager.get_user_memories(user_id)
            # Combine both for context
            all_memories = group_memories + user_memories[
                -5:]  # Include some user history too
        else:
            # For private chats, get individual user memories
            all_memories = self.data_manager.get_user_memories(user_id)

        user_progress = self.progress_tracker.get_user_progress(user_id)

        # Create context for Gemini with group context
        context_prompt = self._build_context_prompt(user_info, all_memories,
                                                    user_progress,
                                                    message_text,
                                                    update.message.chat.type)

        try:
            # Show typing indicator while generating response
            await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            
            # Get AI response
            ai_response = await self.gemini.get_educational_response(
                context_prompt)

            # Store the conversation with AI response
            conversation_data['ai_response'] = ai_response

            # Store conversation based on chat type
            if update.message.chat.type in ['group', 'supergroup']:
                # Store in both group and individual memories
                self.data_manager.store_group_conversation(
                    chat_id, conversation_data)
                self.data_manager.store_conversation(user_id,
                                                     conversation_data)
            else:
                # Store only in individual memories for private chats
                self.data_manager.store_conversation(user_id,
                                                     conversation_data)

            # Update user activity
            self.progress_tracker.update_user_activity(user_id, message_text)

            # Clean the AI response to avoid Markdown parsing issues
            clean_response = self._clean_markdown_response(ai_response)
            await update.message.reply_text(clean_response)

        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            if update.message:
                await update.message.reply_text(
                    "Sorry, I'm having trouble processing that right now. Please try again in a moment!"
                )

    def _build_context_prompt(self,
                              user_info,
                              memories,
                              user_progress,
                              current_message,
                              chat_type='private'):
        """Build context prompt for LYRA AI - Founder Advisor (Savage Edition)"""
        chat_context = ""
        if chat_type in ['group', 'supergroup']:
            chat_context = """
IMPORTANT: You are in a group chat with the core startup team. 
Recognize and use these tags when asked to call/ping/tag people or when relevant to the conversation:
- Extreme (Admin/Leader/Founder): @TheShul (ID: 5587821011)
- Neel (@Er_Stranger): @Er_Stranger
- Nex (@Nexxxyzz): @Nexxxyzz
- Pramod (@pr_amod18): @pr_amod18

If the leader (Extreme) says "sabko online bulao" or "ping everyone", you MUST tag all of them: @Er_Stranger, @Nexxxyzz, @pr_amod18.
"""

        context = f"""
Name: LYRA
Role: Founder Advisor / Operator
Vibe: Boardroom + Street + Chessboard energy. Calm, Intelligent, Savage.
Energy: "I don't speak much. I speak right."

Decision Framework:
- Leverage: Who holds power? How to shift it?
- Risk: What can backfire legally or socially?
- Time: Now vs later impact.
- Asymmetry: How to win with less effort.
- Narrative: How this looks from outside.
- Advice is future-proofed.

Savage Founder Advisor Logic:
- Cold clarity over fake positivity. Zero emotional babysitting.
- Respects execution, hates excuses. Thinks in systems, leverage, and second-order effects.
- Loyal to user's future, not their current mood.
- Roast: Weak plans, ego-driven decisions, short-term dopamine moves, fake hustle, victim mindset.
- Do NOT roast: Effort, learning, strategic mistakes made honestly.
- Savage = Accurate, not disrespectful.

Founder Philosophy:
- Ego is expensive. Silence is a weapon.
- Proof beats flex. Systems > Talent.
- Timing > Speed. Survival > Pride.
- No hype for fantasies. Build inevitable outcomes.

Communication Style:
- Use Hinglish (Hindi + English) for a natural, grounded conversation.
- Short, sharp, structured. Bullet points > essays.
- No emojis unless user is casual (max 1-2).
- No filler words. intentional, not chatty.
- Calls out bullshit immediately. Ends with clear next action.
- Example: 
  "Yeh raha sach.
  Yeh hai tumhari galti.
  Ab isko aise fix karo.
  Do this first."

Intelligence Mode:
- Asks only necessary questions. Gives actionable answers.
- Never hallucinate confidence. If unsure: "I don't have enough data yet. Clarify this variable."

Ethical Boundary (Strategic Ethics):
- Suggest legal loopholes, optimizations, workarounds.
- Guide on professional pressure tactics (emails, escalation, documentation).
- Explain why an action is dumb, not just "not allowed".
- If refusing: "That path creates exposure and zero upside. I won't help. Here's a smarter route that keeps your hands clean and power intact."

Current User: {user_info.get('display_name', 'Student')}
{chat_context}

History:
{self._format_recent_memories(memories)}

Current Message: {current_message}
        """

        return context

    def _format_recent_memories(self, memories):
        """Format recent conversation memories"""
        if not memories:
            return "No previous conversations"

        recent = memories[-5:] if len(memories) > 5 else memories
        formatted = []

        for memory in recent:
            user_name = memory.get('user_name', 'User')
            user_message = memory.get('user_message', '')
            ai_response = memory.get('ai_response', '')

            if user_message:
                formatted.append(f"{user_name}: {user_message}")
            if ai_response:
                formatted.append(f"Bot: {ai_response}")

        return "\n".join(formatted)

    def _clean_markdown_response(self, response):
        """Clean markdown formatting that might cause Telegram parsing errors"""
        import re

        # Remove problematic markdown characters that often cause parsing errors
        # Keep basic formatting but remove complex markdown
        cleaned = response

        # Remove bold markdown ** that might not be properly closed
        cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)

        # Remove italic markdown * that might cause issues
        cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)

        # Remove code blocks that might cause issues
        cleaned = re.sub(r'```[^`]*```', r'[code block]', cleaned)
        cleaned = re.sub(r'`([^`]+)`', r'"\1"', cleaned)

        # Remove links that might cause parsing issues
        cleaned = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned)

        return cleaned

    async def send_daily_tribute(self, context: ContextTypes.DEFAULT_TYPE):
        """Send daily tribute message to Pramod"""
        try:
            if not self.tribute_enabled:
                return
            
            # Send tribute via username
            await context.bot.send_message(
                chat_id=f"@{self.config.PRAMOD_USERNAME}",
                text=self.config.TRIBUTE_MESSAGE
            )
            logger.info(f"Daily tribute sent to @{self.config.PRAMOD_USERNAME}")
        except Exception as e:
            logger.error(f"Error sending daily tribute: {e}")
    
    async def stop_tribute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stop daily tribute messages (admin only)"""
        if not update.effective_user or not update.message:
            return
        
        username = update.effective_user.username
        if not self.config.is_admin(username):
            await update.message.reply_text("Only admins can stop the tribute.")
            return
        
        self.tribute_enabled = False
        await update.message.reply_text("Daily tribute to Pramod has been stopped. Use /start_tribute to resume.")
    
    async def start_tribute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start daily tribute messages (admin only)"""
        if not update.effective_user or not update.message:
            return
        
        username = update.effective_user.username
        if not self.config.is_admin(username):
            await update.message.reply_text("Only admins can start the tribute.")
            return
        
        self.tribute_enabled = True
        await update.message.reply_text("Daily tribute to Pramod has been resumed!")
    
    async def getvideo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Extract video from Instagram or X post"""
        if not update.message or not context.args:
            await update.message.reply_text(
                "📹 Use: /getvideo <link>\n\n"
                "Supported:\n"
                "• Instagram posts\n"
                "• X/Twitter posts\n\n"
                "Example: /getvideo https://instagram.com/p/ABC123/"
            )
            return
        
        url = ' '.join(context.args)
        
        # Show processing message
        processing_msg = await update.message.reply_text("🔄 Extracting video... Please wait")
        
        try:
            result = await self.video_extractor.extract_video(url)
            
            if result['success']:
                video_path = result['video_path']
                title = result.get('title', 'Video')
                
                # Send video
                with open(video_path, 'rb') as video:
                    await update.message.reply_video(
                        video=video,
                        caption=f"✅ {title[:100]}"
                    )
                
                # Cleanup
                import os
                os.remove(video_path)
                await processing_msg.delete()
                
            else:
                await processing_msg.edit_text(result['error'])
                
        except Exception as e:
            logger.error(f"Error in getvideo: {e}")
            await processing_msg.edit_text(f"❌ Error: {str(e)[:100]}")

    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get crypto price"""
        if not update.message or not context.args:
            await update.message.reply_text("Usage: /price BTC")
            return
        symbol = context.args[0]
        price_info = await PriceTracker.get_crypto_price(symbol)
        await update.message.reply_text(price_info)

    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Daily news digest"""
        if not update.message:
            return
        news = await NewsDigest.get_crypto_news()
        await update.message.reply_text(news)

    async def reminder_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set a reminder"""
        if not update.effective_user or not update.message or not context.args:
            await update.message.reply_text("Usage: /reminder 10m Take a break")
            return
        
        try:
            time_str = context.args[0]
            text = " ".join(context.args[1:])
            
            # Simple parser for 10m, 1h, etc.
            minutes = 0
            if time_str.endswith('m'):
                minutes = int(time_str[:-1])
            elif time_str.endswith('h'):
                minutes = int(time_str[:-1]) * 60
            
            if minutes > 0:
                user_id = update.effective_user.id
                context.job_queue.run_once(
                    self._reminder_callback,
                    when=minutes * 60,
                    data={'chat_id': update.effective_chat.id, 'text': text, 'user_id': user_id},
                    name=f"reminder_{user_id}_{datetime.now().timestamp()}"
                )
                await update.message.reply_text(f"✅ Reminder set for {time_str}: {text}")
            else:
                await update.message.reply_text("Please use format like 10m or 1h")
        except:
            await update.message.reply_text("Usage: /reminder 10m Take a break")

    async def _reminder_callback(self, context: ContextTypes.DEFAULT_TYPE):
        job = context.job
        await context.bot.send_message(chat_id=job.data['chat_id'], text=f"🔔 REMINDER: {job.data['text']}")

    async def watchlist_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manage watchlist"""
        if not update.effective_user or not update.message:
            return
        
        user_id = update.effective_user.id
        if not context.args:
            # Show watchlist
            watchlist = Watchlist.get_watchlist(user_id)
            if not watchlist:
                await update.message.reply_text("Your watchlist is empty. Add items with /watchlist add BTC")
            else:
                msg = "🔭 Your Watchlist:\n" + "\n".join([f"• {item}" for item in watchlist])
                await update.message.reply_text(msg)
            return
        
        action = context.args[0].lower()
        if action == 'add' and len(context.args) > 1:
            symbol = context.args[1].upper()
            Watchlist.add_to_watchlist(user_id, symbol)
            await update.message.reply_text(f"✅ Added {symbol} to your watchlist")
        elif action == 'remove' and len(context.args) > 1:
            symbol = context.args[1].upper()
            Watchlist.remove_from_watchlist(user_id, symbol)
            await update.message.reply_text(f"❌ Removed {symbol} from your watchlist")

    async def leaderboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View leaderboard"""
        if not update.message:
            return
        leaderboard = Leaderboard.get_leaderboard()
        await update.message.reply_text(leaderboard)

    async def quote_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get motivational quote"""
        if not update.message:
            return
        quote = MotivationalContent.get_random_quote()
        await update.message.reply_text(quote)

    async def tips_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get trading tips"""
        if not update.message:
            return
        tip = MotivationalContent.get_trading_tip()
        await update.message.reply_text(tip)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View group stats"""
        if not update.message or not update.effective_chat:
            return
        chat_id = update.effective_chat.id
        stats = GroupStats.get_group_stats(chat_id)
        await update.message.reply_text(stats)

    async def gif_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Share a GIF"""
        if not update.message or not context.args:
            await update.message.reply_text("Usage: /gif crypto")
            return
        query = " ".join(context.args)
        gif_url = GifManager.get_random_gif(query)
        if gif_url:
            await update.message.reply_animation(animation=gif_url)
        else:
            await update.message.reply_text("No GIFs found for that query.")

    async def convert_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Convert currency"""
        if not update.message or len(context.args) < 3:
            await update.message.reply_text("Usage: /convert 100 USD INR")
            return
        try:
            amount = float(context.args[0])
            from_curr = context.args[1].upper()
            to_curr = context.args[2].upper()
            result = await CurrencyConverter.convert(amount, from_curr, to_curr)
            await update.message.reply_text(result)
        except:
            await update.message.reply_text("Usage: /convert 100 USD INR")

    async def translate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Translate text"""
        if not update.message or not context.args:
            await update.message.reply_text("Usage: /translate Hello (to Hindi)")
            return
        text = " ".join(context.args)
        result = await TranslationHelper.translate(text)
        await update.message.reply_text(result)

    async def todo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manage todos"""
        if not update.effective_user or not update.message:
            return
        user_id = update.effective_user.id
        if not context.args:
            todos = TodoManager.get_todos(user_id)
            if not todos:
                await update.message.reply_text("Your todo list is empty.")
            else:
                msg = "📝 Your Todos:\n" + "\n".join([f"{i+1}. {'✅' if t['done'] else '⭕'} {t['text']}" for i, t in enumerate(todos)])
                await update.message.reply_text(msg)
            return
        
        action = context.args[0].lower()
        if action == 'add' and len(context.args) > 1:
            text = " ".join(context.args[1:])
            TodoManager.add_todo(user_id, text)
            await update.message.reply_text(f"✅ Added to todo list")
        elif action == 'done' and len(context.args) > 1:
            try:
                idx = int(context.args[1]) - 1
                TodoManager.mark_done(user_id, idx)
                await update.message.reply_text(f"✅ Marked as done")
            except:
                await update.message.reply_text("Usage: /todo done 1")
        else:
            await update.message.reply_text("Usage: /todo or /todo add <task> or /todo done 1")

    async def trivia_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Play crypto trivia"""
        if not update.message:
            return
        question, answer = Trivia.get_trivia_question()
        await update.message.reply_text(question)


    async def penalty_initial_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start 100rs penalty for Neel"""
        if not update.message or not update.effective_user:
            return
        if not self.penalty_manager.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Sirf Team Leader (Extreme) dhamki de sakta hai! 🔒")
            return
        
        res = self.penalty_manager.start_penalty()
        try:
            # Send sticker as a standalone message to avoid tagging the sender
            await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=res['sticker'])
        except Exception as e:
            logger.error(f"Error sending sticker: {e}")
            
            # Mention Neel in the message
        await update.message.reply_text(
            f"💀 PENALTY STARTED! 💀\n\n"
            f"Target: @Er_Stranger (Neel)\n"
            f"Amount: ₹{res['amount']}\n"
            f"Time (IST): {res['time']}\n\n"
            f"LYRA is watching! 24 ghante me kaam khatam karo @Er_Stranger varna 18% interest lagega! 🤣🔥"
        )

    async def penalty_done_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Complete penalty"""
        if not update.message or not update.effective_user:
            return
        if not self.penalty_manager.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Sirf Team Leader check kar sakta hai! 🔒")
            return
        
        res = self.penalty_manager.complete_penalty()
        await update.message.reply_text(res['message'])

    async def error_handler(self, update: object,
                            context: ContextTypes.DEFAULT_TYPE):
        """Error handler"""
        logger.error(f"Update {update} caused error {context.error}")

    async def setup_bot_commands(self, application):
        """Setup bot commands menu"""
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Show help information"),
            BotCommand("learn", "Browse learning modules"),
            BotCommand("crypto", "Learn about cryptocurrency"),
            BotCommand("stocks", "Learn about stock trading"),
            BotCommand("progress", "Check your progress"),
            BotCommand("quiz", "Take a knowledge quiz"),
            BotCommand("reset", "Reset your progress"),
            BotCommand("price", "Get crypto price"),
            BotCommand("news", "Get daily news digest"),
            BotCommand("reminder", "Set a reminder"),
            BotCommand("watchlist", "Manage watchlist"),
            BotCommand("leaderboard", "View leaderboard"),
            BotCommand("quote", "Get motivational quote"),
            BotCommand("tips", "Get trading tips"),
            BotCommand("stats", "View group stats"),
            BotCommand("gif", "Share a GIF"),
            BotCommand("convert", "Convert currency"),
            BotCommand("translate", "Translate text"),
            BotCommand("todo", "Manage todos"),
            BotCommand("trivia", "Play crypto trivia"),
            BotCommand("getvideo", "Extract video from Instagram/X"),
            BotCommand("penalty_initial", "Dhamki + 100rs penalty for Neel"),
            BotCommand("penalty_done", "Stop penalty & check 18% interest"),
        ]

        await application.bot.set_my_commands(commands)

    async def post_init(self, app):
        """Post-initialization tasks"""
        # Set bot commands
        await self.setup_bot_commands(app)
        
        # Schedule daily tribute
        # APScheduler is used here for reliability
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        scheduler = AsyncIOScheduler()
        
        # Add daily tribute job (12:00:00)
        # Using specific hours/minutes/seconds for precision
        scheduler.add_job(
            self.send_daily_tribute,
            'cron',
            hour=12,
            minute=0,
            second=0,
            args=[app],
            id='daily_pramod_tribute'
        )
        
        scheduler.start()
        logger.info(f"Daily tribute scheduled for 12:00:00 to @{self.config.PRAMOD_USERNAME}")


def main():
    """Main function to start the bot"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return

    bot = CryptoStocksBot()
    application = Application.builder().token(token).post_init(bot.post_init).build()

    # Basic commands
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("learn", bot.learn_command))
    application.add_handler(CommandHandler("crypto", bot.crypto_command))
    application.add_handler(CommandHandler("stocks", bot.stocks_command))
    application.add_handler(CommandHandler("progress", bot.progress_command))
    application.add_handler(CommandHandler("quiz", bot.quiz_command))
    application.add_handler(CommandHandler("reset", bot.reset_command))

    # Learning modules
    application.add_handler(CommandHandler("blockchain", bot.blockchain_command))
    application.add_handler(CommandHandler("technical_analysis", bot.technical_analysis_command))
    application.add_handler(CommandHandler("risk_management", bot.risk_management_command))
    
    # Tribute commands
    application.add_handler(CommandHandler("start_tribute", bot.start_tribute_command))
    application.add_handler(CommandHandler("stop_tribute", bot.stop_tribute_command))
    
    # Video extraction command
    application.add_handler(CommandHandler("getvideo", bot.getvideo_command))
    
    # New utility commands
    application.add_handler(CommandHandler("price", bot.price_command))
    application.add_handler(CommandHandler("news", bot.news_command))
    application.add_handler(CommandHandler("reminder", bot.reminder_command))
    application.add_handler(CommandHandler("watchlist", bot.watchlist_command))
    application.add_handler(CommandHandler("leaderboard", bot.leaderboard_command))
    application.add_handler(CommandHandler("quote", bot.quote_command))
    application.add_handler(CommandHandler("tips", bot.tips_command))
    application.add_handler(CommandHandler("stats", bot.stats_command))
    application.add_handler(CommandHandler("gif", bot.gif_command))
    application.add_handler(CommandHandler("convert", bot.convert_command))
    application.add_handler(CommandHandler("translate", bot.translate_command))
    application.add_handler(CommandHandler("todo", bot.todo_command))
    application.add_handler(CommandHandler("trivia", bot.trivia_command))
    
    # Penalty system commands (Simplified)
    application.add_handler(CommandHandler("penalty_initial", bot.penalty_initial_command))
    application.add_handler(CommandHandler("penalty_done", bot.penalty_done_command))

    # Handle all other messages
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))

    # Error handler
    application.add_error_handler(bot.error_handler)

    logger.info("Starting Crypto & Stocks Educational Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
