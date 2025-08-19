"""
User management system for the bot
"""

import logging
from datetime import datetime
from typing import Dict, Optional, List

from bot_config import BotConfig

logger = logging.getLogger(__name__)

class UserManager:
    """Manages user registration, identification, and information"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.config = BotConfig()
    
    def register_user(self, user_id: int, username: str, first_name: str, chat_id: int) -> Dict:
        """Register or update user information"""
        existing_user = self.data_manager.get_user_data(user_id)
        
        # Check if user is in known users list
        known_user_info = self.config.get_user_by_username(username) if username else None
        
        user_data = {
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'chat_id': chat_id,
            'registration_date': existing_user.get('registration_date', datetime.now().isoformat()),
            'last_seen': datetime.now().isoformat(),
            'is_known_user': bool(known_user_info),
            'role': 'user',
            'display_name': first_name
        }
        
        # Set special properties for known users
        if known_user_info:
            user_data['role'] = known_user_info.get('role', 'user')
            user_data['display_name'] = known_user_info.get('name', first_name)
            user_data['known_as'] = known_user_info.get('name')
            
            logger.info(f"Registered known user: {username} ({known_user_info.get('name')})")
        
        # Update user data
        self.data_manager.save_user_data(user_id, user_data)
        
        return user_data
    
    def get_user_info(self, user_id: int) -> Dict:
        """Get user information"""
        user_data = self.data_manager.get_user_data(user_id)
        
        if not user_data:
            # Return default user info if not found
            return {
                'user_id': user_id,
                'username': None,
                'first_name': 'Unknown User',
                'display_name': 'Unknown User',
                'is_known_user': False,
                'role': 'user'
            }
        
        return user_data
    
    def update_last_seen(self, user_id: int):
        """Update user's last seen timestamp"""
        user_data = self.data_manager.get_user_data(user_id)
        if user_data:
            user_data['last_seen'] = datetime.now().isoformat()
            self.data_manager.save_user_data(user_id, user_data)
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is an admin"""
        user_data = self.get_user_info(user_id)
        return user_data.get('role') == 'admin'
    
    def is_known_user(self, user_id: int) -> bool:
        """Check if user is in the known users list"""
        user_data = self.get_user_info(user_id)
        return user_data.get('is_known_user', False)
    
    def get_all_users(self) -> Dict:
        """Get all registered users"""
        return self.data_manager.get_users_data()
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        user_data = self.get_user_info(user_id)
        memories = self.data_manager.get_user_memories(user_id)
        progress = self.data_manager.get_user_progress(user_id)
        
        if user_data.get('registration_date'):
            try:
                reg_date = datetime.fromisoformat(user_data['registration_date'])
                days_since_registration = (datetime.now() - reg_date).days
            except:
                days_since_registration = 0
        else:
            days_since_registration = 0
        
        return {
            'display_name': user_data.get('display_name', 'Unknown'),
            'username': user_data.get('username'),
            'is_known_user': user_data.get('is_known_user', False),
            'role': user_data.get('role', 'user'),
            'days_since_registration': days_since_registration,
            'total_conversations': len(memories),
            'learning_progress': progress.get('overall_score', 0),
            'completed_modules': len(progress.get('completed_modules', [])),
            'quizzes_completed': progress.get('quizzes_completed', 0)
        }
    
    def search_users(self, query: str) -> List[Dict]:
        """Search users by username or display name"""
        all_users = self.get_all_users()
        results = []
        
        query_lower = query.lower()
        
        for user_id, user_data in all_users.items():
            username = user_data.get('username', '').lower()
            display_name = user_data.get('display_name', '').lower()
            first_name = user_data.get('first_name', '').lower()
            
            if (query_lower in username or 
                query_lower in display_name or 
                query_lower in first_name):
                results.append({
                    'user_id': user_id,
                    'username': user_data.get('username'),
                    'display_name': user_data.get('display_name'),
                    'is_known_user': user_data.get('is_known_user', False)
                })
        
        return results
    
    def get_known_users_summary(self) -> str:
        """Get a summary of all known users"""
        all_users = self.get_all_users()
        known_users = []
        
        for user_id, user_data in all_users.items():
            if user_data.get('is_known_user'):
                stats = self.get_user_stats(int(user_id))
                known_users.append({
                    'display_name': user_data.get('display_name'),
                    'username': user_data.get('username'),
                    'role': user_data.get('role'),
                    'progress': stats['learning_progress']
                })
        
        if not known_users:
            return "No known users have interacted with the bot yet."
        
        summary = "👥 **Known Users Summary:**\n\n"
        for user in known_users:
            role_emoji = "👑" if user['role'] == 'admin' else "📚"
            summary += f"{role_emoji} **{user['display_name']}** (@{user['username']})\n"
            summary += f"   └ Progress: {user['progress']}%\n\n"
        
        return summary
