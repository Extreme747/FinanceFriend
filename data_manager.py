"""
Data manager for persistent storage using JSON files
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class DataManager:
    """Manages persistent data storage for the bot"""
    
    def __init__(self):
        self.data_dir = 'data'
        self.ensure_data_directory()
        self.users_file = os.path.join(self.data_dir, 'users.json')
        self.memories_file = os.path.join(self.data_dir, 'memories.json')
        self.progress_file = os.path.join(self.data_dir, 'progress.json')
        self.group_memories_file = os.path.join(self.data_dir, 'group_memories.json')
        
        # Initialize files if they don't exist
        self.initialize_data_files()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
    
    def initialize_data_files(self):
        """Initialize data files with empty structures"""
        files_to_init = [
            (self.users_file, {}),
            (self.memories_file, {}),
            (self.progress_file, {}),
            (self.group_memories_file, {})
        ]
        
        for file_path, default_data in files_to_init:
            if not os.path.exists(file_path):
                self.save_json_file(file_path, default_data)
                logger.info(f"Initialized data file: {file_path}")
    
    def load_json_file(self, file_path: str) -> Dict:
        """Load data from JSON file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return {}
    
    def save_json_file(self, file_path: str, data: Dict):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")
    
    def get_users_data(self) -> Dict:
        """Get all users data"""
        return self.load_json_file(self.users_file)
    
    def save_users_data(self, data: Dict):
        """Save users data"""
        self.save_json_file(self.users_file, data)
    
    def get_user_data(self, user_id: int) -> Dict:
        """Get specific user data"""
        users_data = self.get_users_data()
        return users_data.get(str(user_id), {})
    
    def save_user_data(self, user_id: int, user_data: Dict):
        """Save specific user data"""
        users_data = self.get_users_data()
        users_data[str(user_id)] = user_data
        self.save_users_data(users_data)
    
    def get_memories_data(self) -> Dict:
        """Get all memories data"""
        return self.load_json_file(self.memories_file)
    
    def save_memories_data(self, data: Dict):
        """Save memories data"""
        self.save_json_file(self.memories_file, data)
    
    def get_user_memories(self, user_id: int) -> List[Dict]:
        """Get conversation memories for a user"""
        memories_data = self.get_memories_data()
        return memories_data.get(str(user_id), [])
    
    def store_conversation(self, user_id: int, conversation_data: Dict):
        """Store a conversation in memories"""
        memories_data = self.get_memories_data()
        user_memories = memories_data.get(str(user_id), [])
        
        # Add timestamp if not present
        if 'timestamp' not in conversation_data:
            conversation_data['timestamp'] = datetime.now().isoformat()
        
        user_memories.append(conversation_data)
        
        # Keep only last 50 conversations to manage memory
        if len(user_memories) > 50:
            user_memories = user_memories[-50:]
        
        memories_data[str(user_id)] = user_memories
        self.save_memories_data(memories_data)
    
    def get_group_memories_data(self) -> Dict:
        """Get all group memories data"""
        return self.load_json_file(self.group_memories_file)
    
    def save_group_memories_data(self, data: Dict):
        """Save group memories data"""
        self.save_json_file(self.group_memories_file, data)
    
    def get_group_memories(self, chat_id: int) -> List[Dict]:
        """Get conversation memories for a group chat"""
        group_memories_data = self.get_group_memories_data()
        return group_memories_data.get(str(chat_id), [])
    
    def store_group_conversation(self, chat_id: int, conversation_data: Dict):
        """Store a group conversation in memories"""
        group_memories_data = self.get_group_memories_data()
        group_memories = group_memories_data.get(str(chat_id), [])
        
        # Add timestamp if not present
        if 'timestamp' not in conversation_data:
            conversation_data['timestamp'] = datetime.now().isoformat()
        
        group_memories.append(conversation_data)
        
        # Keep only last 100 group conversations to manage memory
        if len(group_memories) > 100:
            group_memories = group_memories[-100:]
        
        group_memories_data[str(chat_id)] = group_memories
        self.save_group_memories_data(group_memories_data)
    
    def get_progress_data(self) -> Dict:
        """Get all progress data"""
        return self.load_json_file(self.progress_file)
    
    def save_progress_data(self, data: Dict):
        """Save progress data"""
        self.save_json_file(self.progress_file, data)
    
    def get_user_progress(self, user_id: int) -> Dict:
        """Get user progress data"""
        progress_data = self.get_progress_data()
        return progress_data.get(str(user_id), {})
    
    def save_user_progress(self, user_id: int, progress_data: Dict):
        """Save user progress data"""
        all_progress = self.get_progress_data()
        all_progress[str(user_id)] = progress_data
        self.save_progress_data(all_progress)
    
    def backup_data(self):
        """Create backup of all data files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.data_dir, 'backups')
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        files_to_backup = [
            self.users_file,
            self.memories_file,
            self.progress_file
        ]
        
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                backup_path = os.path.join(backup_dir, f"{timestamp}_{filename}")
                
                try:
                    import shutil
                    shutil.copy2(file_path, backup_path)
                    logger.info(f"Backed up {file_path} to {backup_path}")
                except Exception as e:
                    logger.error(f"Error backing up {file_path}: {e}")
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old conversation data"""
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        memories_data = self.get_memories_data()
        cleaned_data = {}
        
        for user_id, conversations in memories_data.items():
            cleaned_conversations = []
            
            for conversation in conversations:
                try:
                    conv_timestamp = datetime.fromisoformat(conversation['timestamp']).timestamp()
                    if conv_timestamp > cutoff_date:
                        cleaned_conversations.append(conversation)
                except:
                    # Keep conversations without valid timestamps
                    cleaned_conversations.append(conversation)
            
            cleaned_data[user_id] = cleaned_conversations
        
        self.save_memories_data(cleaned_data)
        logger.info(f"Cleaned up conversation data older than {days_to_keep} days")
