"""
Educational content for crypto and stocks learning
"""

import random
from typing import Dict, List

class EducationalContent:
    """Manages educational content for crypto and stocks"""
    
    def __init__(self):
        self.learning_modules = self._initialize_learning_modules()
        self.quiz_questions = self._initialize_quiz_questions()
    
    def _initialize_learning_modules(self) -> Dict:
        """Initialize learning modules"""
        return {
            'crypto_basics': {
                'title': 'Cryptocurrency Basics',
                'description': 'Learn the fundamentals of cryptocurrency',
                'content': self._get_crypto_basics_content(),
                'difficulty': 'beginner',
                'estimated_time': '15 minutes'
            },
            'blockchain': {
                'title': 'Blockchain Technology',
                'description': 'Understanding how blockchain works',
                'content': self._get_blockchain_content(),
                'difficulty': 'intermediate',
                'estimated_time': '20 minutes'
            },
            'stocks_basics': {
                'title': 'Stock Market Fundamentals',
                'description': 'Learn the basics of stock trading',
                'content': self._get_stocks_basics_content(),
                'difficulty': 'beginner',
                'estimated_time': '15 minutes'
            },
            'technical_analysis': {
                'title': 'Technical Analysis',
                'description': 'Chart reading and technical indicators',
                'content': self._get_technical_analysis_content(),
                'difficulty': 'intermediate',
                'estimated_time': '25 minutes'
            },
            'risk_management': {
                'title': 'Risk Management',
                'description': 'Managing risk in trading and investing',
                'content': self._get_risk_management_content(),
                'difficulty': 'intermediate',
                'estimated_time': '20 minutes'
            }
        }
    
    def _initialize_quiz_questions(self) -> List[Dict]:
        """Initialize quiz questions"""
        return [
            {
                'topic': 'crypto',
                'difficulty': 'easy',
                'question': 'What is Bitcoin?',
                'options': [
                    'A digital currency',
                    'A physical coin',
                    'A bank',
                    'A government program'
                ],
                'correct_answer': 0,
                'explanation': 'Bitcoin is a decentralized digital currency that operates without a central bank.'
            },
            {
                'topic': 'crypto',
                'difficulty': 'medium',
                'question': 'What is a blockchain?',
                'options': [
                    'A type of cryptocurrency',
                    'A distributed ledger technology',
                    'A trading platform',
                    'A wallet app'
                ],
                'correct_answer': 1,
                'explanation': 'Blockchain is a distributed ledger technology that maintains a continuously growing list of records.'
            },
            {
                'topic': 'stocks',
                'difficulty': 'easy',
                'question': 'What does P/E ratio stand for?',
                'options': [
                    'Price to Equity',
                    'Price to Earnings',
                    'Profit to Equity',
                    'Profit to Earnings'
                ],
                'correct_answer': 1,
                'explanation': 'P/E ratio stands for Price-to-Earnings ratio, which compares stock price to earnings per share.'
            },
            {
                'topic': 'stocks',
                'difficulty': 'medium',
                'question': 'What is market capitalization?',
                'options': [
                    'Total debt of a company',
                    'Total value of company shares',
                    'Annual revenue',
                    'Number of employees'
                ],
                'correct_answer': 1,
                'explanation': 'Market cap is the total value of all company shares, calculated as share price × number of shares.'
            }
        ]
    
    def get_learning_modules(self) -> Dict:
        """Get all learning modules"""
        return self.learning_modules
    
    def get_module_content(self, module_id: str) -> str:
        """Get content for a specific module"""
        module = self.learning_modules.get(module_id)
        if module:
            return module['content']
        return "Module not found."
    
    def get_crypto_basics(self) -> str:
        """Get cryptocurrency basics content"""
        return self._get_crypto_basics_content()
    
    def get_stocks_basics(self) -> str:
        """Get stocks basics content"""
        return self._get_stocks_basics_content()
    
    def get_blockchain_content(self) -> str:
        """Get blockchain content"""
        return self._get_blockchain_content()
    
    def get_technical_analysis_content(self) -> str:
        """Get technical analysis content"""  
        return self._get_technical_analysis_content()
    
    def get_risk_management_content(self) -> str:
        """Get risk management content"""
        return self._get_risk_management_content()
    
    def _get_crypto_basics_content(self) -> str:
        """Cryptocurrency basics content"""
        return """
🪙 **Cryptocurrency Basics**

**What is Cryptocurrency?**
Cryptocurrency is a digital or virtual currency secured by cryptography. Unlike traditional currencies, it operates independently of central banks.

**Key Features:**
• 🔒 **Decentralized**: No central authority controls it
• 🔐 **Secure**: Protected by cryptographic techniques
• 🌐 **Global**: Can be sent anywhere in the world
• 💫 **Transparent**: All transactions are recorded on blockchain

**Popular Cryptocurrencies:**
• **Bitcoin (BTC)**: The first and most well-known cryptocurrency
• **Ethereum (ETH)**: Platform for smart contracts and DApps
• **Binance Coin (BNB)**: Native token of Binance exchange

**How to Get Started:**
1. 📚 Learn the basics (you're doing this now!)
2. 🏦 Choose a reputable exchange
3. 💼 Set up a secure wallet
4. 💰 Start with small amounts
5. 📊 Research before investing

**Safety Tips:**
⚠️ Never invest more than you can afford to lose
🔑 Keep your private keys secure
🎯 Do your own research (DYOR)
📈 Start small and learn gradually

Ready to learn more? Ask me about blockchain technology or any crypto concept!
        """
    
    def _get_stocks_basics_content(self) -> str:
        """Stocks basics content"""
        return """
📈 **Stock Market Fundamentals**

**What are Stocks?**
Stocks represent ownership shares in a company. When you buy stock, you become a partial owner of that business.

**Key Concepts:**
• 📊 **Share Price**: Current market value of one share
• 🏢 **Market Cap**: Total value of all company shares
• 💰 **Dividends**: Payments to shareholders from profits
• 📈 **Capital Gains**: Profit from selling shares at higher price

**Types of Stocks:**
• **Common Stock**: Voting rights, dividend potential
• **Preferred Stock**: Fixed dividends, no voting rights
• **Growth Stocks**: Companies expected to grow rapidly
• **Value Stocks**: Undervalued companies with potential

**Stock Market Basics:**
• 🏛️ **Exchanges**: NYSE, NASDAQ where stocks are traded
• ⏰ **Trading Hours**: Generally 9:30 AM - 4:00 PM EST
• 📊 **Orders**: Market orders vs. limit orders
• 💼 **Brokers**: Platforms to buy and sell stocks

**Getting Started:**
1. 📖 Educate yourself about investing
2. 🎯 Define your investment goals
3. 💼 Open a brokerage account
4. 🔍 Research companies thoroughly
5. 📊 Start with index funds or ETFs
6. 💰 Invest regularly and diversify

**Investment Strategies:**
• 📈 **Buy and Hold**: Long-term investing
• 💰 **Dollar-Cost Averaging**: Regular fixed investments
• 🎯 **Diversification**: Don't put all eggs in one basket

Want to learn about technical analysis or risk management? Just ask!
        """
    
    def _get_blockchain_content(self) -> str:
        """Blockchain technology content"""
        return """
⛓️ **Blockchain Technology**

**What is Blockchain?**
A blockchain is a distributed ledger that maintains a continuously growing list of records (blocks) linked and secured using cryptography.

**Key Features:**
• 🔗 **Immutable**: Records cannot be changed once added
• 🌐 **Distributed**: Copies exist across multiple computers
• 🔒 **Secure**: Cryptographically secured
• 👁️ **Transparent**: All transactions are visible

**How It Works:**
1. 📝 Transaction is initiated
2. 📊 Transaction is broadcast to network
3. ✅ Network validates the transaction
4. 📦 Transaction is included in a block
5. 🔗 Block is added to the chain
6. ✨ Transaction is complete

**Applications Beyond Crypto:**
• 📋 Supply chain tracking
• 🏥 Medical records
• 🗳️ Voting systems
• 🏠 Real estate transactions
• 🎨 Digital art (NFTs)

This technology powers all cryptocurrencies and has many other uses!
        """
    
    def _get_technical_analysis_content(self) -> str:
        """Technical analysis content"""
        return """
📊 **Technical Analysis**

**What is Technical Analysis?**
The study of price charts and trading volume to predict future price movements based on historical data.

**Key Concepts:**
• 📈 **Trends**: Upward, downward, or sideways price movements
• 🎯 **Support/Resistance**: Price levels where buying/selling pressure exists
• 📊 **Volume**: Number of shares/coins traded
• 📉 **Chart Patterns**: Recurring formations that may predict price moves

**Popular Indicators:**
• 📈 **Moving Averages**: Average price over specific periods
• 💪 **RSI**: Relative Strength Index (overbought/oversold)
• 📊 **MACD**: Moving Average Convergence Divergence
• 🎯 **Bollinger Bands**: Price volatility indicator

**Chart Types:**
• 📊 **Line Charts**: Simple price progression
• 📈 **Candlestick**: Shows open, high, low, close prices
• 📉 **Bar Charts**: Similar to candlesticks, different format

Remember: Technical analysis is a tool, not a guarantee!
        """
    
    def _get_risk_management_content(self) -> str:
        """Risk management content"""
        return """
🛡️ **Risk Management**

**Why Risk Management Matters:**
Protecting your capital is more important than making profits. Good risk management helps you stay in the game long-term.

**Key Principles:**
• 💰 **Position Sizing**: Never risk more than you can afford to lose
• 🎯 **Stop Losses**: Set predetermined exit points
• 🔄 **Diversification**: Spread risk across different assets
• 📊 **Risk-Reward Ratio**: Ensure potential gains justify risks

**The 1% Rule:**
Never risk more than 1% of your portfolio on a single trade.

**Portfolio Allocation:**
• 🏦 **Emergency Fund**: 3-6 months expenses
• 🔒 **Conservative**: 60-70% in stable investments
• 📈 **Growth**: 20-30% in higher-risk investments
• 🎲 **Speculative**: 5-10% in high-risk assets

**Emotional Control:**
• 😌 **Stay Calm**: Don't make decisions based on fear or greed
• 📋 **Have a Plan**: Stick to your strategy
• 📚 **Keep Learning**: Knowledge reduces risk

Risk management is your financial safety net!
        """
    
    def get_random_quiz(self) -> Dict:
        """Get a random quiz question"""
        return random.choice(self.quiz_questions)
    
    def get_quiz_by_topic(self, topic: str) -> List[Dict]:
        """Get quiz questions for a specific topic"""
        return [q for q in self.quiz_questions if q['topic'] == topic]
    
    def get_daily_tip(self) -> str:
        """Get a daily learning tip"""
        tips = [
            "💡 **Daily Tip**: Always do your own research before making any investment decisions!",
            "💡 **Daily Tip**: Dollar-cost averaging can help reduce the impact of market volatility.",
            "💡 **Daily Tip**: Diversification is your best friend in investing - don't put all eggs in one basket!",
            "💡 **Daily Tip**: The best time to invest was yesterday, the second best time is now - but only after proper research!",
            "💡 **Daily Tip**: Never invest money you can't afford to lose, especially in volatile markets.",
            "💡 **Daily Tip**: Emotional trading is often the enemy of profitable trading. Stay disciplined!",
            "💡 **Daily Tip**: Understanding compound interest is crucial for long-term wealth building.",
            "💡 **Daily Tip**: Keep learning! The markets are always evolving, and so should your knowledge."
        ]
        return random.choice(tips)
