"""
Utility features: prices, news, jokes, quotes, etc.
"""

import aiohttp
import json
import random
from datetime import datetime
from typing import Optional, Dict, Any

class PriceTracker:
    """Fetch crypto and stock prices"""
    
    @staticmethod
    async def get_crypto_price(symbol: str) -> Optional[str]:
        """Get crypto price from CoinGecko (free, no key needed)"""
        try:
            symbol = symbol.upper()
            async with aiohttp.ClientSession() as session:
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if symbol.lower() in data:
                            coin_data = data[symbol.lower()]
                            price = coin_data.get('usd', 'N/A')
                            change = coin_data.get('usd_24h_change', 0)
                            change_emoji = "🔴" if change < 0 else "🟢"
                            return f"`{symbol}`: ${price:,.2f} {change_emoji} {change:.2f}%"
                    return f"Couldn't find price for {symbol}"
        except Exception as e:
            return f"Error fetching price: {str(e)}"

class NewsDigest:
    """Daily news digest"""
    
    @staticmethod
    async def get_crypto_news() -> str:
        """Get crypto news (mock for now, can integrate with real API)"""
        news_snippets = [
            "🔴 Bitcoin volatility remains high amid market uncertainty",
            "🟢 Ethereum upgrade improves network efficiency by 30%",
            "📊 DeFi TVL reaches new milestone of $100B",
            "🚀 Altseason indicators showing bullish signals",
            "⚠️ Regulatory news: New crypto bill under discussion",
            "💎 NFT market shows signs of recovery",
            "🔐 Security tip: Always use hardware wallets for large holdings",
        ]
        return f"📰 **Crypto News Digest**\n\n" + "\n".join(random.sample(news_snippets, 3))

class ReminderManager:
    """Manage reminders"""
    
    reminders = {}
    
    @classmethod
    def add_reminder(cls, user_id: int, text: str, minutes: int) -> str:
        """Add a reminder"""
        if user_id not in cls.reminders:
            cls.reminders[user_id] = []
        
        reminder = {
            'text': text,
            'time': minutes,
            'created': datetime.now().isoformat()
        }
        cls.reminders[user_id].append(reminder)
        return f"⏰ Reminder set: '{text}' in {minutes} minutes"
    
    @classmethod
    def get_reminders(cls, user_id: int) -> str:
        """Get user's reminders"""
        if user_id not in cls.reminders or not cls.reminders[user_id]:
            return "No reminders set"
        
        text = "📝 **Your Reminders:**\n"
        for i, r in enumerate(cls.reminders[user_id], 1):
            text += f"{i}. {r['text']} ({r['time']} min)\n"
        return text

class PollManager:
    """Simple poll system"""
    
    polls = {}
    
    @classmethod
    def create_poll(cls, poll_id: str, question: str, options: list) -> str:
        """Create a new poll"""
        cls.polls[poll_id] = {
            'question': question,
            'options': {opt: [] for opt in options},
            'voters': set()
        }
        return f"📊 Poll created: {question}\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
    
    @classmethod
    def vote(cls, poll_id: str, user_id: int, option_idx: int) -> str:
        """Vote on a poll"""
        if poll_id not in cls.polls:
            return "Poll not found"
        
        poll = cls.polls[poll_id]
        if user_id in poll['voters']:
            return "You already voted!"
        
        options = list(poll['options'].keys())
        if option_idx < 0 or option_idx >= len(options):
            return "Invalid option"
        
        poll['voters'].add(user_id)
        poll['options'][options[option_idx]].append(user_id)
        return f"✅ Vote registered for: {options[option_idx]}"

class Watchlist:
    """Track favorite coins/stocks"""
    
    watchlists = {}
    
    @classmethod
    def add_to_watchlist(cls, user_id: int, symbol: str) -> str:
        """Add to watchlist"""
        if user_id not in cls.watchlists:
            cls.watchlists[user_id] = []
        
        symbol = symbol.upper()
        if symbol not in cls.watchlists[user_id]:
            cls.watchlists[user_id].append(symbol)
            return f"✅ Added {symbol} to watchlist"
        return f"{symbol} already in watchlist"
    
    @classmethod
    def get_watchlist(cls, user_id: int) -> str:
        """Get user's watchlist"""
        if user_id not in cls.watchlists or not cls.watchlists[user_id]:
            return "📋 Your watchlist is empty"
        
        return "📋 **Your Watchlist:**\n" + "\n".join(cls.watchlists[user_id])
    
    @classmethod
    def remove_from_watchlist(cls, user_id: int, symbol: str) -> str:
        """Remove from watchlist"""
        symbol = symbol.upper()
        if user_id in cls.watchlists and symbol in cls.watchlists[user_id]:
            cls.watchlists[user_id].remove(symbol)
            return f"✅ Removed {symbol} from watchlist"
        return f"{symbol} not in watchlist"

class MotivationalContent:
    """Daily motivation and quotes"""
    
    QUOTES = [
        "The best time to buy is when there's blood in the streets. - Warren Buffett",
        "Success is not about money. It's about discipline. - Noah Kagan",
        "The goal of a successful trader is to make the best trades. Not the most trades.",
        "Money is not the goal. Money is a tool. - Tony Robbins",
        "The only thing that matters in the market is price action. - Jesse Livermore",
        "Trading is 90% psychology and 10% mechanics.",
        "Compound interest is the 8th wonder of the world.",
        "Time in the market beats timing the market.",
        "Risk management is everything in trading.",
        "Learn from losses, celebrate wins, but never get emotional.",
    ]
    
    TIPS = [
        "💡 Always set a stop loss before entering a trade",
        "💡 Never risk more than 2% of your capital on a single trade",
        "💡 Diversification reduces risk - don't put all eggs in one basket",
        "💡 Keep a trading journal to track your progress",
        "💡 Technical analysis + Fundamentals = Better decisions",
        "💡 Patience is a virtue in trading - wait for the right setup",
        "💡 FOMO (Fear of Missing Out) is the biggest enemy of traders",
        "💡 Always have an exit strategy before entering",
        "💡 Practice with paper trading before using real money",
        "💡 The trend is your friend - trade with the trend",
    ]
    
    @staticmethod
    def get_daily_quote() -> str:
        """Get random motivational quote"""
        quote = random.choice(MotivationalContent.QUOTES)
        return f"💭 **Quote of the Day:**\n\n{quote}"
    
    @staticmethod
    def get_trading_tip() -> str:
        """Get trading tip"""
        tip = random.choice(MotivationalContent.TIPS)
        return f"🎯 **Trading Tip:**\n\n{tip}"

class Leaderboard:
    """Group leaderboard for quiz scores"""
    
    scores = {}
    
    @classmethod
    def add_score(cls, user_name: str, points: int) -> None:
        """Add points to user score"""
        if user_name not in cls.scores:
            cls.scores[user_name] = 0
        cls.scores[user_name] += points
    
    @classmethod
    def get_leaderboard(cls) -> str:
        """Get top scores"""
        if not cls.scores:
            return "🏆 Leaderboard is empty. Start taking quizzes!"
        
        sorted_scores = sorted(cls.scores.items(), key=lambda x: x[1], reverse=True)
        text = "🏆 **Leaderboard** 🏆\n\n"
        medals = ["🥇", "🥈", "🥉"]
        
        for i, (name, score) in enumerate(sorted_scores[:10]):
            medal = medals[i] if i < 3 else f"{i+1}."
            text += f"{medal} {name}: {score} points\n"
        
        return text

class GroupStats:
    """Group statistics"""
    
    stats = {
        'messages': {},
        'videos': {},
        'commands': {}
    }
    
    @classmethod
    def track_message(cls, user_name: str) -> None:
        """Track message count"""
        if user_name not in cls.stats['messages']:
            cls.stats['messages'][user_name] = 0
        cls.stats['messages'][user_name] += 1
    
    @classmethod
    def track_video(cls, user_name: str) -> None:
        """Track video shares"""
        if user_name not in cls.stats['videos']:
            cls.stats['videos'][user_name] = 0
        cls.stats['videos'][user_name] += 1
    
    @classmethod
    def get_stats(cls) -> str:
        """Get group statistics"""
        text = "📊 **Group Stats**\n\n"
        
        if cls.stats['messages']:
            text += "💬 **Most Active:**\n"
            top_msg = sorted(cls.stats['messages'].items(), key=lambda x: x[1], reverse=True)[:3]
            for i, (name, count) in enumerate(top_msg, 1):
                text += f"{i}. {name}: {count} messages\n"
        
        if cls.stats['videos']:
            text += "\n📹 **Most Videos Shared:**\n"
            top_vid = sorted(cls.stats['videos'].items(), key=lambda x: x[1], reverse=True)[:3]
            for i, (name, count) in enumerate(top_vid, 1):
                text += f"{i}. {name}: {count} videos\n"
        
        return text

class GifManager:
    """GIF search using emoji reactions"""
    
    @staticmethod
    def get_gif_emoji() -> str:
        """Get random fun GIF"""
        gifs = [
            "📈 *GIF: Bull market celebration!*",
            "🎉 *GIF: Trading victory!*",
            "🚀 *GIF: Moon mission!*",
            "💰 *GIF: Money falling!*",
            "🔥 *GIF: On fire!*",
            "😂 *GIF: Laughing at losses!*",
            "💎 *GIF: Diamond hands!*",
            "🤦 *GIF: Face palm moment!*",
        ]
        return random.choice(gifs)

class CurrencyConverter:
    """Convert between currencies"""
    
    RATES = {
        'USD': 1.0,
        'INR': 84.5,
        'EUR': 0.95,
        'GBP': 0.79,
        'JPY': 150.0,
        'BTC': 0.000022,  # Example rate
    }
    
    @classmethod
    def convert(cls, amount: float, from_currency: str, to_currency: str) -> str:
        """Convert currency"""
        from_c = from_currency.upper()
        to_c = to_currency.upper()
        
        if from_c not in cls.RATES or to_c not in cls.RATES:
            return f"❌ Currency not supported. Available: {', '.join(cls.RATES.keys())}"
        
        result = (amount / cls.RATES[from_c]) * cls.RATES[to_c]
        return f"💱 {amount} {from_c} = {result:.2f} {to_c}"

class TranslationHelper:
    """Simple translation (mock - can integrate with real API)"""
    
    COMMON_PHRASES = {
        'hello': 'नमस्ते',
        'thanks': 'धन्यवाद',
        'please': 'कृपया',
        'ok': 'ठीक है',
        'yes': 'हाँ',
        'no': 'नहीं',
    }
    
    @staticmethod
    def translate(text: str, to_lang: str = 'hindi') -> str:
        """Translate text"""
        if to_lang.lower() == 'hindi':
            translated = TranslationHelper.COMMON_PHRASES.get(text.lower(), f"'{text}' (not in database)")
            return f"🌐 Hindi: {translated}"
        return "Only Hindi translation available for now"

class TodoManager:
    """Simple todo/task manager"""
    
    todos = {}
    
    @classmethod
    def add_todo(cls, user_id: int, task: str) -> str:
        """Add a todo"""
        if user_id not in cls.todos:
            cls.todos[user_id] = []
        
        cls.todos[user_id].append({
            'task': task,
            'done': False,
            'created': datetime.now().isoformat()
        })
        return f"✅ Added todo: '{task}'"
    
    @classmethod
    def get_todos(cls, user_id: int) -> str:
        """Get user's todos"""
        if user_id not in cls.todos or not cls.todos[user_id]:
            return "📝 No todos yet!"
        
        text = "📝 **Your Todos:**\n"
        for i, t in enumerate(cls.todos[user_id], 1):
            status = "✅" if t['done'] else "⬜"
            text += f"{i}. {status} {t['task']}\n"
        return text
    
    @classmethod
    def complete_todo(cls, user_id: int, task_num: int) -> str:
        """Mark todo as done"""
        if user_id not in cls.todos or task_num < 1 or task_num > len(cls.todos[user_id]):
            return "❌ Todo not found"
        
        cls.todos[user_id][task_num - 1]['done'] = True
        return f"✅ Completed: '{cls.todos[user_id][task_num - 1]['task']}'"

class Trivia:
    """Crypto/Trading trivia"""
    
    QUESTIONS = [
        {
            'q': 'What year was Bitcoin created?',
            'opts': ['2008', '2009', '2010', '2011'],
            'ans': 1
        },
        {
            'q': 'What is the maximum supply of Bitcoin?',
            'opts': ['10M', '21M', '100M', 'Unlimited'],
            'ans': 1
        },
        {
            'q': 'Who is the founder of Ethereum?',
            'opts': ['Vitalik Buterin', 'Satoshi Nakamoto', 'Charlie Lee', 'Brian Armstrong'],
            'ans': 0
        },
        {
            'q': 'What does DeFi stand for?',
            'opts': ['Digital Finance', 'Decentralized Finance', 'Digital Fund', 'None'],
            'ans': 1
        },
        {
            'q': 'What is a blockchain?',
            'opts': ['A type of database', 'A chain of encrypted blocks', 'A cryptocurrency', 'All of above'],
            'ans': 1
        },
    ]
    
    @staticmethod
    def get_trivia_question() -> tuple:
        """Get random trivia question"""
        q_data = random.choice(Trivia.QUESTIONS)
        question = f"❓ {q_data['q']}\n\n"
        for i, opt in enumerate(q_data['opts'], 1):
            question += f"{i}. {opt}\n"
        return (question, q_data['ans'])
