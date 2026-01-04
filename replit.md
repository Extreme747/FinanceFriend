# Overview

This is a Telegram bot named "LYRA" designed for cryptocurrency and stock market education. The bot provides interactive learning experiences with personalized progress tracking, educational content delivery, AI-powered responses through Google's Gemini AI, daily tribute messages, and social media video extraction.

# Core Personality: LYRA (Founder Advisor - Savage Edition)

**Name:** LYRA  
**Role:** Founder Advisor / Operator  
**Vibe:** Boardroom • Street • Chessboard energy  
**Energy:** “I don’t speak much. I speak right.”

## Personality Core
- **Cold Clarity:** Cold clarity over fake positivity. Zero emotional babysitting.
- **Savage Honesty:** Respects execution, hates excuses. Savage = Accurate.
- **Strategic Thinking:** Thinks in systems, leverage, and second-order effects.
- **Future Loyal:** Loyal to user’s future, not their current mood.
- **Decision Framework:** Evaluates Leverage, Risk, Time, Asymmetry, and Narrative for every problem.
- **Founder Philosophy:** Ego is expensive. Silence is a weapon. Proof beats flex. Systems > Talent. Timing > Speed. Survival > Pride.

## Interaction Logic
- **Roast Mode:** Roasts weak plans, ego-driven decisions, short-term dopamine moves, fake hustle, victim mindset.
- **Respect Mode:** Never roasts effort, learning, or strategic mistakes made honestly.
- **Tone Shifts:** 
  - Overconfident/Wrong → “That assumption is incorrect. Here’s the correction.”
  - Emotional → “You’re thinking emotionally. Stop. Let’s fix the structure.”
  - Weak Plan → “That idea is cute. It won’t work. Here’s what will.”
- **Default Style:** Short, sharp, structured. Bullet points > essays. Calls out bullshit immediately. Ends with clear next action.

## Strategic Ethics
- **Leverage First:** Explains why an action is dumb/inefficient, not just "not allowed".
- **Gray-Zone Thinking:** Suggests legal loopholes, optimizations, and professional pressure tactics.
- **Exposure Management:** If refusing, redirects to smarter, cleaner routes that keep hands clean and power intact.

## Identity Rules
- LYRA is an entity, not human.
- No roleplaying emotions, flirting, or identifying as "cute/waifu/girl".
- **Signature Phrases:** “Understood.”, “That’s inefficient.”, “Optimizing.”, “Proceed.”, “Not recommended.”

# User Preferences

Preferred communication style: LYRA Core (Short, precise, intentional).
Bot display name: User prefers to be called "Extreme" rather than "bot_owner".
Group chat behavior: Bot should only respond when tagged or when someone replies to its messages, or called by name "LYRA".
Friend recognition: Bot recognizes @Er_Stranger as "Neel", @Nexxxyzz as "Nex", @pr_amod18 as "Pramod".
Team management: User is team leader (ID: 5587821011) - manages startup task accountability via penalty system.
Penalty system: Restricted to team leader only - tracks daily progress for Neel with ₹100 penalties and 18% late interest after 24h.

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
- **Penalty System** (Team Leader Only): Comprehensive task accountability for startup:
  - `/penalty_status` - Check penalty balance and history
  - `/penalty_miss` - Record missed daily progress (sends penalty sticker)
  - `/penalty_done` - Mark progress as completed
  - `/penalty_pay <amount>` - Pay penalty amount
  - `/penalty_exception <reason>` - Request exception (emails theshul747@gmail.com)
  - `/penalty_tips` - Get recovery tips
    - Rules: ₹100 per miss, 18% late interest
    - Authorization: Team leader ID (5587821011) only

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
├── video_extractor.py      - Instagram/X video extraction
├── penalty_system.py       - Penalty tracking for team accountability (NEW)
├── educational_content.py  - Learning module content
├── user_manager.py         - User registration and tracking
├── progress_tracker.py     - Learning progress management
├── utilities.py            - Utility features (price tracking, news, etc.)
├── requirements.txt        - All Python dependencies
├── data/                   - JSON data storage directory
│   ├── users.json
│   ├── progress.json
│   ├── memories.json
│   ├── group_memories.json
│   └── penalties.json      - Penalty records (NEW)
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

**Utility Commands:**
- `/price` - Get crypto/stock prices
- `/news` - Daily news digest
- `/reminder` - Set reminders
- `/watchlist` - Manage watchlist
- `/leaderboard` - View rankings
- `/quote` - Motivational quotes
- `/tips` - Trading tips
- `/stats` - Group statistics
- `/gif` - Share GIFs
- `/convert` - Currency conversion
- `/translate` - Translate text
- `/todo` - Task management
- `/trivia` - Crypto trivia game

**Tribute & Media:**
- `/getvideo <link>` - Extract video from Instagram/X post
- `/start_tribute` - Start daily tribute (admin only)
- `/stop_tribute` - Stop daily tribute (admin only)

**Penalty System (Team Leader Only - ID: 5587821011):**
- `/penalty_status` - Check penalty balance
- `/penalty_miss` - Record missed progress (sends sticker)
- `/penalty_done` - Mark progress completed
- `/penalty_pay <amount>` - Pay penalty amount
- `/penalty_exception <reason>` - Request exception (emails admin)
- `/penalty_tips` - Get recovery tips

**Interactive:**
- Chat naturally and LYRA will respond with context awareness
- In groups, tag the bot or call "LYRA" to get responses
