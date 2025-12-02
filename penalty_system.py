"""
Penalty system for tracking daily progress, fines, and recovery
Specifically for Neel (lazy mode 😄)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class PenaltyManager:
    """Manage penalties for missed daily progress"""
    
    PENALTY_FILE = 'data/penalties.json'
    NEEL_USERNAME = 'Er_Stranger'
    PENALTY_AMOUNT = 100  # ₹
    INTEREST_RATE = 0.28  # 28%
    SKIP_THRESHOLD = 2  # Days to skip before donation
    ADMIN_EMAIL = 'theshul747@gmail.com'
    PENALTY_STICKER_ID = 'CAACAgUAAxkBAAEP7BhpLpgG4ODPU-ZAbhjlMkMIebGI_wACyh0AAu7FWFUq0EzTLCmrwzYE'
    
    def __init__(self):
        self._load_penalties()
    
    def _load_penalties(self):
        """Load penalties from file"""
        if not os.path.exists(self.PENALTY_FILE):
            self.penalties = {}
            self._save_penalties()
        else:
            try:
                with open(self.PENALTY_FILE, 'r') as f:
                    self.penalties = json.load(f)
            except:
                self.penalties = {}
    
    def _save_penalties(self):
        """Save penalties to file"""
        os.makedirs('data', exist_ok=True)
        with open(self.PENALTY_FILE, 'w') as f:
            json.dump(self.penalties, f, indent=2)
    
    def record_missed_progress(self, username: str) -> Dict:
        """Record when user misses daily progress"""
        if username != self.NEEL_USERNAME:
            return {'success': False, 'message': 'Only Neel needs penalties 😅'}
        
        if username not in self.penalties:
            self.penalties[username] = {
                'total_penalty': 0,
                'paid_amount': 0,
                'missed_days': 0,
                'consecutive_skips': 0,
                'last_skip_date': None,
                'history': [],
                'paid_history': [],
                'donated_amount': 0,
                'exceptions': []
            }
        
        user_data = self.penalties[username]
        today = datetime.now().date().isoformat()
        
        # Check if it's a new day
        if user_data['last_skip_date'] != today:
            user_data['consecutive_skips'] += 1
        
        user_data['missed_days'] += 1
        user_data['total_penalty'] += self.PENALTY_AMOUNT
        user_data['last_skip_date'] = today
        
        entry = {
            'date': today,
            'penalty': self.PENALTY_AMOUNT,
            'reason': 'Missed daily progress',
            'current_total': user_data['total_penalty']
        }
        user_data['history'].append(entry)
        self._save_penalties()
        
        return {
            'success': True,
            'message': f"❌ ₹{self.PENALTY_AMOUNT} penalty added!\nTotal penalty: ₹{user_data['total_penalty']}",
            'consecutive_skips': user_data['consecutive_skips'],
            'sticker_id': self.PENALTY_STICKER_ID
        }
    
    def add_exception(self, username: str, reason: str, email_notification: bool = True) -> Dict:
        """Add exception for valid reasons (medical, family, etc.)"""
        if username != self.NEEL_USERNAME:
            return {'success': False, 'message': 'Only Neel can request exceptions'}
        
        if username not in self.penalties:
            self.penalties[username] = {
                'total_penalty': 0,
                'paid_amount': 0,
                'missed_days': 0,
                'consecutive_skips': 0,
                'last_skip_date': None,
                'history': [],
                'paid_history': [],
                'donated_amount': 0,
                'exceptions': []
            }
        
        exception_entry = {
            'date': datetime.now().date().isoformat(),
            'reason': reason,
            'status': 'pending_approval'
        }
        
        self.penalties[username]['exceptions'].append(exception_entry)
        self._save_penalties()
        
        if email_notification:
            self._send_exception_email(username, reason)
        
        return {
            'success': True,
            'message': f"📧 Exception request sent to {self.ADMIN_EMAIL}\nReason: {reason}\nWaiting for approval..."
        }
    
    def _send_exception_email(self, username: str, reason: str):
        """Send email notification for exception"""
        try:
            subject = f"Penalty Exception Request - {username}"
            body = f"""
Hello Admin,

{username} has requested an exception for missing daily progress.

Reason: {reason}
Date: {datetime.now().date()}

Please review and approve/reject this exception.

Regards,
Ayaka Bot
            """
            
            # In production, configure actual email
            # For now, just log it
            print(f"📧 Exception email would be sent to {self.ADMIN_EMAIL}: {reason}")
            
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def mark_progress_done(self, username: str) -> Dict:
        """Mark user's progress as completed"""
        if username != self.NEEL_USERNAME:
            return {'success': False, 'message': 'Only Neel uses this system'}
        
        if username not in self.penalties:
            return {'success': True, 'message': '✅ No penalty for you today!'}
        
        user_data = self.penalties[username]
        today = datetime.now().date().isoformat()
        
        # Reset consecutive skips
        if user_data['last_skip_date'] != today:
            user_data['consecutive_skips'] = 0
        
        # Recovery: if maintaining progress, reduce penalty
        if user_data['total_penalty'] > 0 and user_data['consecutive_skips'] == 0:
            user_data['consecutive_skips'] = 0
            return {
                'success': True,
                'message': '✅ Great work! You maintained progress today.\nKeep it up to recover penalties!'
            }
        
        self._save_penalties()
        return {'success': True, 'message': '✅ Progress recorded!'}
    
    def pay_penalty(self, username: str, amount: float) -> Dict:
        """Record penalty payment"""
        if username != self.NEEL_USERNAME:
            return {'success': False, 'message': 'Only Neel needs to pay penalties'}
        
        if username not in self.penalties:
            return {'success': False, 'message': 'No penalties found'}
        
        user_data = self.penalties[username]
        pending_penalty = user_data['total_penalty'] - user_data['paid_amount']
        
        if amount <= 0:
            return {'success': False, 'message': 'Amount must be positive'}
        
        if amount > pending_penalty:
            return {
                'success': False,
                'message': f'Amount exceeds pending penalty!\nPending: ₹{pending_penalty}'
            }
        
        user_data['paid_amount'] += amount
        
        payment_entry = {
            'date': datetime.now().date().isoformat(),
            'amount': amount,
            'remaining': pending_penalty - amount
        }
        user_data['paid_history'].append(payment_entry)
        
        # Check if fully paid
        if user_data['paid_amount'] >= user_data['total_penalty']:
            message = f"✅ Penalty fully paid! ₹{amount} received.\nYou're free to go! 🎉"
        else:
            remaining = pending_penalty - amount
            message = f"✅ Payment of ₹{amount} recorded!\nRemaining: ₹{remaining}"
        
        self._save_penalties()
        return {'success': True, 'message': message}
    
    def check_donation_trigger(self, username: str) -> Dict:
        """Check if penalty should be donated"""
        if username != self.NEEL_USERNAME:
            return {'success': False, 'message': 'N/A'}
        
        if username not in self.penalties:
            return {'success': False, 'message': 'No penalties'}
        
        user_data = self.penalties[username]
        
        # If skipped >2 days AND not paid, donate
        if user_data['consecutive_skips'] > self.SKIP_THRESHOLD:
            pending = user_data['total_penalty'] - user_data['paid_amount']
            if pending > 0:
                user_data['donated_amount'] += pending
                user_data['total_penalty'] = 0
                user_data['paid_amount'] = 0
                self._save_penalties()
                
                return {
                    'success': True,
                    'message': f"🫀 Penalty of ₹{pending} donated to local foundation with your name!\nLet's get back on track!",
                    'donated': pending
                }
        
        return {'success': False, 'message': 'No donation trigger'}
    
    def get_status(self, username: str) -> str:
        """Get user's penalty status"""
        if username != self.NEEL_USERNAME:
            return "✅ You're doing great, no penalties needed!"
        
        if username not in self.penalties:
            return "📊 No penalties recorded yet. Keep doing the work!"
        
        user_data = self.penalties[username]
        pending = user_data['total_penalty'] - user_data['paid_amount']
        
        status = f"""
📊 **{username.replace('@', '')} - Penalty Status**

💰 Total Penalty: ₹{user_data['total_penalty']}
✅ Paid Amount: ₹{user_data['paid_amount']}
⏳ Pending: ₹{pending}

📅 Missed Days: {user_data['missed_days']}
🔄 Consecutive Skips: {user_data['consecutive_skips']}
🫀 Donated to Foundation: ₹{user_data['donated_amount']}

⚠️ Interest (28%): ₹{int(pending * 0.28)} if not paid soon!

📧 Have a valid reason? Email: {self.ADMIN_EMAIL}
Accepted: Medical emergency, health issues, family functions, holidays, college work, etc.
        """
        
        return status.strip()
    
    def get_recovery_tips(self) -> str:
        """Get tips to recover from penalties"""
        tips = """
🎯 **How to Recover from Penalties (For Neel)** 🎯

1. ✅ **Maintain Daily Progress**: Complete your tasks on time
2. 🔄 **Consistent Work**: Don't skip more than allowed days
3. 💳 **Pay Penalties**: Settle pending amounts to avoid interest
4. 📧 **Report Issues**: Email admin for valid exceptions
5. 🏃 **Speed Recovery**: More consistent days = faster penalty reduction

💡 Pro Tip: Better to work daily than pay penalties! 😄

Remember: After 2 skips without payment, penalty gets donated to local foundation with your name!
        """
        return tips.strip()

class PenaltyNotifier:
    """Send penalty notifications"""
    
    @staticmethod
    def get_daily_reminder(username: str, manager: PenaltyManager) -> str:
        """Get daily reminder for Neel"""
        if username != manager.NEEL_USERNAME:
            return ""
        
        if username not in manager.penalties:
            return "💪 New day, fresh start! Show me your progress today!"
        
        user_data = manager.penalties[username]
        pending = user_data['total_penalty'] - user_data['paid_amount']
        
        if pending > 0:
            return f"⚠️ Daily Reminder: You have ₹{pending} pending penalty.\nDo your work today to recover! 💪"
        else:
            return "✅ You're all clear! Keep up the good work!"
