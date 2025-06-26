from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict

@dataclass
class TrackedWallet:
    address: str
    name: Optional[str] = None

@dataclass
class User:
    id: str
    session_data: Dict = field(default_factory=dict)
    
    def clear_session(self) -> None:
        """Clear session data - for privacy"""
        self.session_data.clear() 