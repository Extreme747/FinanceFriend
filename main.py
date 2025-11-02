#!/usr/bin/env python3
"""
Crypto & Stocks Educational Telegram Bot with Gemini Pro AI
Features: Persistent memory, progress tracking, educational content
"""

import logging
import os
import asyncio
from datetime import datetime
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode, ChatAction

from bot_config import BotConfig
from gemini_client import GeminiClient
from data_manager import DataManager
from educational_content import EducationalContent
from user_manager import UserManager
from progress_tracker import ProgressTracker

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

Hey {user_info['display_name']}! I'm Ayaka, your friendly AI tutor powered by Gemini Pro. I'm here to help you learn about cryptocurrency and stock trading! 

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

💡 **Tip:** You can also just chat with me naturally! Call me Ayaka and I'll remember our conversations and help you learn step by step.
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

        # In group chats, only respond if bot is mentioned, replied to, or called by name "Ayaka"
        if update.message.chat.type in ['group', 'supergroup']:
            bot_username = context.bot.username
            is_mentioned = f"@{bot_username}" in message_text if bot_username else False
            is_reply_to_bot = (
                update.message.reply_to_message
                and update.message.reply_to_message.from_user
                and update.message.reply_to_message.from_user.is_bot)
            is_called_by_name = "ayaka" in message_text.lower(
            ) or "Ayaka" in message_text

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
        """Build context prompt for Gemini AI"""
        chat_context = ""
        if chat_type in ['group', 'supergroup']:
            chat_context = """
IMPORTANT: You are in a group chat with friends. Remember the context of group conversations between:
- Extreme (bot owner/admin)
- Neel (@Er_Stranger) 
- Nex (@Nexxxyzz)
- Pramod (@pr_amod18)

When they reference previous conversations or inside jokes, acknowledge them. Be part of their friend group while maintaining your helpful nature.
"""

        context = f"""
You are Ayaka, a friendly AI assistant with expertise in cryptocurrency, stock trading, and general conversation. Your name is Ayaka and you should introduce yourself as such when appropriate. {chat_context}

Current User Information:
- Name: {user_info.get('display_name', 'Student')}
- Learning Progress: {user_progress.get('overall_score', 0)}% complete
- Completed Modules: {len(user_progress.get('completed_modules', []))}
- Recent Topics: {user_progress.get('recent_topics', [])}

Recent Conversation History:
{self._format_recent_memories(memories)}

Current Message: {current_message}

Guidelines:
1. For crypto/stocks topics: Provide accurate, educational information with safety-focused advice
2. For general conversation: Be helpful, engaging, and supportive on any topic
3. Remember context from previous conversations (both group and individual)
4. Be encouraging and maintain a conversational, friendly tone
5. You can discuss anything - from crypto and stocks to daily life, hobbies, technology, or any other topics
6. In group chats, acknowledge the friend dynamics and shared conversations
7. Always prioritize helpful, accurate responses

Please respond considering the conversation history and context.
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
        ]

        await application.bot.set_my_commands(commands)


def main():
    """Main function to start the bot"""
    # Get bot token from environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return

    # Initialize bot
    bot = CryptoStocksBot()

    # Create application
    application = Application.builder().token(bot_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("learn", bot.learn_command))
    application.add_handler(CommandHandler("crypto", bot.crypto_command))
    application.add_handler(CommandHandler("stocks", bot.stocks_command))
    application.add_handler(CommandHandler("progress", bot.progress_command))
    application.add_handler(CommandHandler("quiz", bot.quiz_command))
    application.add_handler(CommandHandler("reset", bot.reset_command))

    # Add module-specific handlers
    application.add_handler(CommandHandler("crypto_basics",
                                           bot.crypto_command))
    application.add_handler(
        CommandHandler("blockchain", bot.blockchain_command))
    application.add_handler(CommandHandler("stocks_basics",
                                           bot.stocks_command))
    application.add_handler(
        CommandHandler("technical_analysis", bot.technical_analysis_command))
    application.add_handler(
        CommandHandler("risk_management", bot.risk_management_command))

    # Handle all other messages
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))

    # Error handler
    application.add_error_handler(bot.error_handler)

    # Setup commands menu
    async def post_init(app):
        await bot.setup_bot_commands(app)

    application.post_init = post_init

    # Start the bot
    logger.info("Starting Crypto & Stocks Educational Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
# GHOST BUSTED
