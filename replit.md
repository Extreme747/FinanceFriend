# Overview

This is a Telegram bot designed for cryptocurrency and stock market education. The bot provides interactive learning experiences with personalized progress tracking, educational content delivery, and AI-powered responses through Google's Gemini AI. Users can learn about trading, blockchain technology, and financial markets through structured modules, quizzes, and conversational interactions.

# User Preferences

Preferred communication style: Simple, everyday language.
Bot display name: User prefers to be called "Extreme" rather than "bot_owner".
Group chat behavior: Bot should only respond when tagged or when someone replies to its messages, not to every message.
Friend recognition: Bot recognizes @Er_Stranger as "Neel", @Nexxxyzz as "Nex", @pr_amod18 as "Pramod".

# System Architecture

## Bot Framework
- **Telegram Bot API**: Built using python-telegram-bot library for handling user interactions, commands, and message processing
- **Asynchronous Processing**: Uses asyncio for handling concurrent user requests and API calls

## AI Integration
- **Gemini AI Client**: Integrates Google's Gemini 2.5 Flash model for generating educational responses with specialized system instructions for financial education
- **Educational Persona**: AI configured with expert educator personality, providing supportive and engaging learning experiences

## Data Management
- **JSON File Storage**: Simple file-based persistence using JSON files for storing user data, progress, and memories
- **Three Data Stores**: 
  - `users.json` for user registration and profile data
  - `progress.json` for learning progress and achievements
  - `memories.json` for conversational memory and interactions

## User Management System
- **User Registration**: Automatic user registration with role-based access (admin, student, regular user)
- **Known Users**: Predefined user list with special roles and display names
- **Progress Tracking**: Individual user progress monitoring with skill levels, completed modules, and learning streaks

## Educational Content System
- **Modular Learning**: Structured learning modules covering crypto basics, blockchain, stocks, technical analysis, and risk management
- **Difficulty Progression**: Content organized by difficulty levels (beginner, intermediate, advanced)
- **Quiz System**: Interactive quizzes with multiple difficulty levels for knowledge assessment
- **Achievement System**: Progress milestones and achievement tracking to gamify learning

## Configuration Management
- **Centralized Config**: Bot configuration class containing user definitions, learning topics, progress milestones, and quiz levels
- **Environment Variables**: Secure API key management through environment variables

# External Dependencies

## AI Services
- **Google Gemini AI**: Gemini 2.5 Flash model for generating educational content and conversational responses
- **API Authentication**: Requires GEMINI_API_KEY environment variable

## Telegram Platform
- **Telegram Bot API**: Core platform for user interaction and message delivery
- **Bot Token**: Requires Telegram bot token for authentication

## Python Libraries
- **python-telegram-bot**: Main framework for Telegram bot functionality
- **google-genai**: Official Google Generative AI library for Gemini integration
- **Standard Library**: Uses json, os, logging, datetime, and asyncio for core functionality

## Data Storage
- **Local File System**: JSON files stored in local `data/` directory for persistence
- **No External Database**: Self-contained storage solution without external database dependencies