from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

@dataclass
class ConversationState:
    """Represents the state of a conversation"""
    state: str
    data: Dict[str, Any]
    started_at: datetime
    expires_at: datetime

class StateManager:
    def __init__(self, expiry_minutes: int = 30):
        self.states: Dict[str, ConversationState] = {}
        self.expiry_minutes = expiry_minutes
        
    def set_state(self, user_id: str, state: str, data: Dict[str, Any] = None) -> None:
        """Set state for a user"""
        now = datetime.now()
        self.states[user_id] = ConversationState(
            state=state,
            data=data or {},
            started_at=now,
            expires_at=now + timedelta(minutes=self.expiry_minutes)
        )
        
    def get_state(self, user_id: str) -> Optional[ConversationState]:
        """Get current state for a user"""
        state = self.states.get(user_id)
        if not state:
            return None
            
        # Check expiry
        if datetime.now() > state.expires_at:
            self.clear_state(user_id)
            return None
            
        return state
        
    def clear_state(self, user_id: str) -> None:
        """Clear state for a user"""
        if user_id in self.states:
            del self.states[user_id]
            
    def update_data(self, user_id: str, data: Dict[str, Any]) -> None:
        """Update state data for a user"""
        if state := self.get_state(user_id):
            state.data.update(data) 