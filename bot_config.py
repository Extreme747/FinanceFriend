"""
Bot configuration and constants
"""

class BotConfig:
    """Configuration class for the bot"""
    
    # Known users with their telegram handles and names
    KNOWN_USERS = {
        '@Er_Stranger': {
            'name': 'neel',
            'role': 'student'
        },
        '@Nexxxyzz': {
            'name': 'nex',
            'role': 'student'
        },
        '@pr_amod18': {
            'name': 'pramod',
            'role': 'student'
        },
        '@Extreme747': {
            'name': 'Extreme',
            'role': 'admin'
        }
    }
    
    # Educational topics
    LEARNING_TOPICS = [
        'cryptocurrency_basics',
        'blockchain_technology',
        'stock_market_fundamentals',
        'trading_strategies',
        'risk_management',
        'technical_analysis',
        'fundamental_analysis',
        'portfolio_management'
    ]
    
    # Progress milestones
    PROGRESS_MILESTONES = {
        'beginner': 0,
        'novice': 25,
        'intermediate': 50,
        'advanced': 75,
        'expert': 90
    }
    
    # Quiz difficulty levels
    QUIZ_LEVELS = ['easy', 'medium', 'hard']
    
    # Data file paths
    DATA_PATHS = {
        'users': 'data/users.json',
        'memories': 'data/memories.json',
        'progress': 'data/progress.json'
    }
    
    @classmethod
    def get_user_by_username(cls, username):
        """Get user info by username"""
        for handle, info in cls.KNOWN_USERS.items():
            if handle.lower() == f"@{username}".lower():
                return info
        return None
    
    @classmethod
    def is_admin(cls, username):
        """Check if user is admin"""
        user_info = cls.get_user_by_username(username)
        return user_info and user_info.get('role') == 'admin'
