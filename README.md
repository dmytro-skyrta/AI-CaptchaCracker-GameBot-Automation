This project is for educational purposes only. 
Using may violate the terms of service of the game. 
Any use, copying, modification, or distribution of this code
without the author's written permission is strictly prohibited.

Copyright (c) [2025] [Dmytro Skyrta]

# AI-CaptchaCracker-GameBot-Automation
An automated bot for one online game that uses AI-powered CAPTCHA recognition to handle authentication challenges while automatically managing battles and collecting in-game bonuses.

# Features

Automatic login with CAPTCHA solving capabilities
Navigates to battle sections autonomously
Submits battle requests and handles confirmation challenges
Manages the complete battle cycle with attack timing
Collects daily bonuses and rewards
Supports multiple AI models for CAPTCHA recognition

# Technical Components

Selenium-based navigation: Automates browser interactions
AI-powered CAPTCHA solving: Uses both cloud-based (OpenRouter) and local AI models
Multi-model testing: Tests various AI models to find the most effective CAPTCHA solvers
Error recovery: Robust error handling and recovery mechanisms

# Requirements

Python 3.8+
Selenium WebDriver
Chrome browser
OpenAI API key (for cloud-based CAPTCHA solving)
Optional: Local AI models for offline CAPTCHA recognition

# Configuration

Configure your credentials in main_v2_1.py:
pythonLOGIN = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"
For OpenRouter API, set your key in capt_recog_with_AI.py or AI_Modelslist_Tester.py.

# Usage

Run the main bot:
bashpython main_v2_1.py
To test AI models for CAPTCHA recognition:
bashpython AI_Modelslist_Tester.py

# CAPTCHA Recognition

The system uses multiple approaches for CAPTCHA recognition:
- Cloud-based AI models through OpenRouter API
- Local AI models (DeepSeek, Qwen)
- OCR with pytesseract as fallback
