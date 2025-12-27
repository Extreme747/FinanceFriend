"""
Simple penalty system for Neel
Commands: /penalty_initial (start) and /penalty_done (complete)
Interest: 18% if not done within 24 hours
"""

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

class PenaltyManager:
    PENALTY_FILE = 'data/neel_penalties.json'
    NEEL_USERNAME = 'Er_Stranger'
    TEAM_LEADER_ID = 5587821011
    INITIAL_AMOUNT = 100
    INTEREST_RATE = 0.18
    STICKER_ID = 'CAACAgUAAxkBAAEP7BhpLpgG4ODPU-ZAbhjlMkMIebGI_wACyh0AAu7FWFUq0EzTLCmrwzYE'

    def __init__(self):
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.PENALTY_FILE):
            try:
                with open(self.PENALTY_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_data(self):
        os.makedirs('data', exist_ok=True)
        with open(self.PENALTY_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def is_authorized(self, user_id: int) -> bool:
        return user_id == self.TEAM_LEADER_ID

    def start_penalty(self) -> Dict:
        ist_offset = timedelta(hours=5, minutes=30)
        now_ist = datetime.now(timezone.utc) + ist_offset
        
        self.data['current'] = {
            'start_time': now_ist.isoformat(),
            'amount': self.INITIAL_AMOUNT,
            'status': 'pending'
        }
        self._save_data()
        return {
            'amount': self.INITIAL_AMOUNT,
            'sticker': self.STICKER_ID,
            'time': now_ist.strftime("%Y-%m-%d %H:%M:%S")
        }

    def complete_penalty(self) -> Dict:
        if 'current' not in self.data or self.data['current']['status'] != 'pending':
            return {'success': False, 'message': "Koi active penalty nahi hai! 🤷‍♂️"}

        ist_offset = timedelta(hours=5, minutes=30)
        curr = self.data['current']
        start_time = datetime.fromisoformat(curr['start_time'])
        now_ist = datetime.now(timezone.utc) + ist_offset
        
        elapsed = now_ist - start_time
        final_amount = curr['amount']
        interest_added = 0
        
        if elapsed > timedelta(hours=24):
            interest_added = final_amount * self.INTEREST_RATE
            final_amount += interest_added

        curr['status'] = 'completed'
        curr['end_time'] = now_ist.isoformat()
        curr['final_amount'] = final_amount
        
        if 'history' not in self.data:
            self.data['history'] = []
        self.data['history'].append(curr)
        del self.data['current']
        
        self._save_data()
        
        msg = f"✅ Penalty Done!\n\nStart (IST): {start_time.strftime('%Y-%m-%d %H:%M:%S')}\nEnd (IST): {now_ist.strftime('%Y-%m-%d %H:%M:%S')}"
        if interest_added > 0:
            msg += f"\n\n⚠️ 24h se zyada ho gaye! 18% interest lag gaya.\nFinal Amount: ₹{final_amount:.2f}"
        else:
            msg += f"\nFinal Amount: ₹{final_amount}"
            
        return {'success': True, 'message': msg}
