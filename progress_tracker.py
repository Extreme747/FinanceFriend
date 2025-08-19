"""
Progress tracking system for user learning
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Tracks user learning progress and achievements"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def get_user_progress(self, user_id: int) -> Dict:
        """Get user's learning progress"""
        progress = self.data_manager.get_user_progress(user_id)
        
        # Initialize progress if not exists
        if not progress:
            progress = self._initialize_user_progress(user_id)
            self.data_manager.save_user_progress(user_id, progress)
        
        return progress
    
    def _initialize_user_progress(self, user_id: int) -> Dict:
        """Initialize progress structure for new user"""
        return {
            'user_id': user_id,
            'overall_score': 0,
            'completed_modules': [],
            'current_modules': [],
            'quizzes_completed': 0,
            'correct_answers': 0,
            'total_questions': 0,
            'learning_streak': 0,
            'last_activity': None,
            'days_active': 0,
            'achievements': [],
            'recent_topics': [],
            'skill_levels': {
                'crypto': 'beginner',
                'stocks': 'beginner',
                'trading': 'beginner'
            },
            'learning_goals': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
    
    def update_progress(self, user_id: int, topic: str, action: str, score: int = 0):
        """Update user progress for a specific topic and action"""
        progress = self.get_user_progress(user_id)
        
        current_time = datetime.now().isoformat()
        progress['updated_at'] = current_time
        
        # Update based on action
        if action == 'started':
            if topic not in progress['current_modules']:
                progress['current_modules'].append(topic)
        
        elif action == 'completed':
            if topic not in progress['completed_modules']:
                progress['completed_modules'].append(topic)
            
            if topic in progress['current_modules']:
                progress['current_modules'].remove(topic)
            
            # Award points for completion
            progress['overall_score'] += 10
        
        elif action == 'quiz_completed':
            progress['quizzes_completed'] += 1
            progress['total_questions'] += 1
            
            if score > 0:
                progress['correct_answers'] += score
                progress['overall_score'] += score * 5
        
        # Update recent topics
        if topic not in progress['recent_topics']:
            progress['recent_topics'].append(topic)
        
        # Keep only last 10 recent topics
        if len(progress['recent_topics']) > 10:
            progress['recent_topics'] = progress['recent_topics'][-10:]
        
        # Update overall score (cap at 100)
        progress['overall_score'] = min(progress['overall_score'], 100)
        
        # Check for achievements
        self._check_achievements(progress)
        
        # Update skill levels
        self._update_skill_levels(progress)
        
        self.data_manager.save_user_progress(user_id, progress)
    
    def update_user_activity(self, user_id: int, message: str):
        """Update user activity tracking"""
        progress = self.get_user_progress(user_id)
        
        current_date = datetime.now().date()
        last_activity_date = None
        
        if progress.get('last_activity'):
            try:
                last_activity_date = datetime.fromisoformat(progress['last_activity']).date()
            except:
                pass
        
        # Update activity tracking
        if last_activity_date != current_date:
            progress['days_active'] += 1
            
            # Update learning streak
            if last_activity_date and (current_date - last_activity_date).days == 1:
                progress['learning_streak'] += 1
            elif last_activity_date and (current_date - last_activity_date).days > 1:
                progress['learning_streak'] = 1
            else:
                progress['learning_streak'] = 1
        
        progress['last_activity'] = datetime.now().isoformat()
        progress['updated_at'] = datetime.now().isoformat()
        
        self.data_manager.save_user_progress(user_id, progress)
    
    def _check_achievements(self, progress: Dict):
        """Check and award achievements"""
        achievements = progress.get('achievements', [])
        
        # First steps achievement
        if len(progress['completed_modules']) >= 1 and 'First Steps' not in achievements:
            achievements.append('First Steps')
        
        # Knowledge seeker achievement
        if len(progress['completed_modules']) >= 3 and 'Knowledge Seeker' not in achievements:
            achievements.append('Knowledge Seeker')
        
        # Quiz master achievement
        if progress['quizzes_completed'] >= 5 and 'Quiz Master' not in achievements:
            achievements.append('Quiz Master')
        
        # Consistent learner achievement
        if progress['learning_streak'] >= 7 and 'Consistent Learner' not in achievements:
            achievements.append('Consistent Learner')
        
        # High achiever achievement
        if progress['overall_score'] >= 80 and 'High Achiever' not in achievements:
            achievements.append('High Achiever')
        
        # Perfect score achievement
        if (progress['total_questions'] > 0 and 
            progress['correct_answers'] == progress['total_questions'] and
            progress['total_questions'] >= 5 and
            'Perfect Score' not in achievements):
            achievements.append('Perfect Score')
        
        progress['achievements'] = achievements
    
    def _update_skill_levels(self, progress: Dict):
        """Update skill levels based on progress"""
        skill_levels = progress.get('skill_levels', {})
        completed_modules = progress.get('completed_modules', [])
        overall_score = progress.get('overall_score', 0)
        
        # Crypto skill level
        crypto_modules = [m for m in completed_modules if 'crypto' in m.lower() or 'blockchain' in m.lower()]
        if len(crypto_modules) >= 3 or overall_score >= 60:
            skill_levels['crypto'] = 'intermediate'
        if len(crypto_modules) >= 5 or overall_score >= 80:
            skill_levels['crypto'] = 'advanced'
        
        # Stocks skill level
        stocks_modules = [m for m in completed_modules if 'stock' in m.lower() or 'trading' in m.lower()]
        if len(stocks_modules) >= 3 or overall_score >= 60:
            skill_levels['stocks'] = 'intermediate'
        if len(stocks_modules) >= 5 or overall_score >= 80:
            skill_levels['stocks'] = 'advanced'
        
        # Trading skill level
        trading_modules = [m for m in completed_modules if any(term in m.lower() for term in ['trading', 'analysis', 'risk'])]
        if len(trading_modules) >= 2 or overall_score >= 50:
            skill_levels['trading'] = 'intermediate'
        if len(trading_modules) >= 4 or overall_score >= 75:
            skill_levels['trading'] = 'advanced'
        
        progress['skill_levels'] = skill_levels
    
    def get_progress_summary(self, user_id: int) -> str:
        """Get formatted progress summary"""
        progress = self.get_user_progress(user_id)
        
        summary = f"📊 **Your Learning Progress**\n\n"
        summary += f"🎯 **Overall Score:** {progress['overall_score']}%\n"
        summary += f"📚 **Completed Modules:** {len(progress['completed_modules'])}\n"
        summary += f"🔥 **Learning Streak:** {progress['learning_streak']} days\n"
        summary += f"📅 **Days Active:** {progress['days_active']}\n"
        summary += f"❓ **Quizzes Completed:** {progress['quizzes_completed']}\n"
        
        if progress['total_questions'] > 0:
            accuracy = (progress['correct_answers'] / progress['total_questions']) * 100
            summary += f"🎯 **Quiz Accuracy:** {accuracy:.1f}%\n"
        
        summary += f"\n**📈 Skill Levels:**\n"
        for skill, level in progress['skill_levels'].items():
            emoji = "🌟" if level == "advanced" else "📈" if level == "intermediate" else "🌱"
            summary += f"{emoji} {skill.title()}: {level.title()}\n"
        
        if progress['achievements']:
            summary += f"\n🏆 **Achievements:**\n"
            for achievement in progress['achievements']:
                summary += f"🏅 {achievement}\n"
        
        return summary
    
    def reset_user_progress(self, user_id: int):
        """Reset user's progress"""
        fresh_progress = self._initialize_user_progress(user_id)
        self.data_manager.save_user_progress(user_id, fresh_progress)
        logger.info(f"Reset progress for user {user_id}")
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users by progress"""
        all_progress = self.data_manager.get_progress_data()
        
        leaderboard = []
        for user_id, progress in all_progress.items():
            user_info = self.data_manager.get_user_data(int(user_id))
            if user_info:
                leaderboard.append({
                    'user_id': user_id,
                    'display_name': user_info.get('display_name', 'Unknown'),
                    'overall_score': progress.get('overall_score', 0),
                    'completed_modules': len(progress.get('completed_modules', [])),
                    'achievements': len(progress.get('achievements', []))
                })
        
        # Sort by overall score
        leaderboard.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return leaderboard[:limit]
    
    def get_learning_recommendations(self, user_id: int) -> List[str]:
        """Get personalized learning recommendations"""
        progress = self.get_user_progress(user_id)
        completed = progress.get('completed_modules', [])
        skill_levels = progress.get('skill_levels', {})
        
        recommendations = []
        
        # Recommend based on completion
        if 'crypto_basics' not in completed:
            recommendations.append("Start with Cryptocurrency Basics - perfect for beginners!")
        
        if 'stocks_basics' not in completed:
            recommendations.append("Learn Stock Market Fundamentals - build your foundation!")
        
        if len(completed) >= 2 and 'risk_management' not in completed:
            recommendations.append("Study Risk Management - essential for any trader!")
        
        # Recommend based on skill level
        if skill_levels.get('crypto') == 'beginner' and 'blockchain' not in completed:
            recommendations.append("Dive deeper with Blockchain Technology module!")
        
        if skill_levels.get('stocks') == 'beginner' and 'technical_analysis' not in completed:
            recommendations.append("Learn Technical Analysis to read charts like a pro!")
        
        # Always recommend practice
        if progress.get('quizzes_completed', 0) < 3:
            recommendations.append("Take more quizzes to test your knowledge!")
        
        return recommendations[:3]  # Return top 3 recommendations
