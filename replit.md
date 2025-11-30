# Overview

This is a Telegram bot named "Ayaka" designed for cryptocurrency and stock market education. The bot provides interactive learning experiences with personalized progress tracking, educational content delivery, AI-powered responses through Google's Gemini AI, daily tribute messages, and social media video extraction. Users can learn about trading, blockchain technology, and financial markets through structured modules, quizzes, and conversational interactions.

# User Preferences

Preferred communication style: Simple, everyday language.
Bot display name: User prefers to be called "Extreme" rather than "bot_owner".
Group chat behavior: Bot should only respond when tagged or when someone replies to its messages, not to every message.
Friend recognition: Bot recognizes @Er_Stranger as "Neel", @Nexxxyzz as "Nex", @pr_amod18 as "Pramod".
Group memory: Bot remembers group conversations between friends and maintains context of shared discussions.
Bot name: "Ayaka" - responds when called by this name in group chats.
Typing indicator: Bot shows "typing" animation when generating responses (for better UX).
Daily tributes: Bot sends daily tribute message to Pramod at 12 PM (auto-enabled).
Video extraction: Bot can extract and send videos from Instagram and X (Twitter) posts.

# System Architecture

## Bot Framework
- **Telegram Bot API**: Built using python-telegram-bot v22.5 for handling user interactions, commands, and message processing
- **Asynchronous Processing**: Uses asyncio for handling concurrent user requests and API calls
- **Job Scheduling**: APScheduler for scheduling daily tribute messages

## AI Integration
- **Gemini AI Client**: Integrates Google's Gemini 2.5 Flash model (google-genai library)
- **Educational Persona**: AI configured with expert educator personality
- **General Conversation**: Bot supports both educational and general topics

## Data Management
- **JSON File Storage**: Simple file-based persistence using JSON files
- **Four Data Stores**: 
  - `users.json` for user registration and profile data
  - `progress.json` for learning progress and achievements
  - `memories.json` for individual conversational memory
  - `group_memories.json` for group chat memory

## User Management System
- **User Registration**: Automatic user registration with role-based access (admin, student, regular user)
- **Known Users**: Predefined user list with special roles and display names
- **Progress Tracking**: Individual user progress monitoring with skill levels, completed modules, and learning streaks

## Educational Content System
- **Modular Learning**: Structured learning modules covering crypto basics, blockchain, stocks, technical analysis, and risk management
- **Difficulty Progression**: Content organized by difficulty levels (beginner, intermediate, advanced)
- **Quiz System**: Interactive quizzes with multiple difficulty levels
- **Achievement System**: Progress milestones and achievement tracking

## New Features (Recent Addition)
- **Daily Tribute System**: Sends daily message to @pr_amod18 at 12:00 PM with support for:
  - `/stop_tribute` - Stop daily messages (admin only)
  - `/start_tribute` - Resume daily messages (admin only)
- **Video Extraction**: New `/getvideo <link>` command to extract and send videos from:
  - Instagram posts
  - X/Twitter posts
  - Uses yt-dlp for reliable extraction
  - Handles file size limits (Telegram's 50MB max)

## Configuration Management
- **Centralized Config**: Bot configuration class containing user definitions, tribute settings, learning topics
- **Environment Variables**: Secure API key management (TELEGRAM_BOT_TOKEN, GEMINI_API_KEY)

# External Dependencies

## AI Services
- **Google Gemini 2.5 Flash**: AI model for educational content and conversational responses
- **API Authentication**: Requires GEMINI_API_KEY environment variable

## Telegram Platform
- **Telegram Bot API**: Core platform for user interaction and message delivery
- **Bot Token**: Requires TELEGRAM_BOT_TOKEN environment variable

## Python Libraries
- **python-telegram-bot (v22.5)**: Main framework for Telegram bot functionality
- **google-genai (v1.31.0)**: Official Google Generative AI library for Gemini integration
- **APScheduler (v3.11.1)**: Job scheduling for daily tribute messages
- **yt-dlp (v2025.11.12)**: Video extraction from Instagram and X/Twitter
- **Standard Library**: Uses json, os, logging, datetime, asyncio, re for core functionality

## Data Storage
- **Local File System**: JSON files stored in local `data/` directory for persistence
- **Video Storage**: Downloaded videos temporarily stored in `videos/` directory (auto-cleaned after sending)
- **No External Database**: Self-contained storage solution

# Deployment Info

## Secrets Required (both platforms)
- `TELEGRAM_BOT_TOKEN` - Telegram bot token from BotFather
- `GEMINI_API_KEY` - Google Gemini API key

## Start Command
```
python main.py
```

## Recent Changes (Latest Session)

1. **Upgraded Dependencies**:
   - python-telegram-bot: 20.8 → 22.5
   - Added APScheduler for job scheduling
   - Added yt-dlp for video extraction
   - google-genai: 1.31.0 (kept, most current)
   - httpx: 0.28.1 (compatible with all libraries)

2. **New Features**:
   - Typing indicator when bot generates responses
   - Daily tribute system (12 PM) for @pr_amod18
   - Video extraction from Instagram/X with `/getvideo` command
   - Support for starting/stopping tribute system

3. **Fixed Issues**:
   - Removed deprecated `pass_args` parameter (fixed TypeError)
   - All libraries fully compatible with Python 3.11+
   - Job queue properly initialized

## Files Structure
```
.
├── main.py                 - Main bot logic and command handlers
├── bot_config.py           - Configuration, user definitions, tribute settings
├── gemini_client.py        - AI integration with Gemini 2.5 Flash
├── data_manager.py         - JSON file persistence management
├── video_extractor.py      - Instagram/X video extraction (NEW)
├── educational_content.py  - Learning module content
├── user_manager.py         - User registration and tracking
├── progress_tracker.py     - Learning progress management
├── requirements.txt        - All Python dependencies
├── data/                   - JSON data storage directory
└── videos/                 - Temporary video storage (auto-cleaned)
```

# All Bot Commands

**Learning Commands:**
- `/start` - Start the bot
- `/help` - Show help message
- `/learn` - Browse learning modules
- `/crypto` - Cryptocurrency fundamentals
- `/stocks` - Stock trading basics
- `/quiz` - Test knowledge
- `/progress` - Check learning progress
- `/reset` - Reset progress

**New Commands:**
- `/getvideo <link>` - Extract video from Instagram/X post
- `/start_tribute` - Start daily tribute (admin only)
- `/stop_tribute` - Stop daily tribute (admin only)

**Interactive:**
- Chat naturally and Ayaka will respond with context awareness
- In groups, tag the bot or call "Ayaka" to get responses
