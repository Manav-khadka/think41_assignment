from typing import List, Dict, Optional
from pydantic import BaseModel

class PollOption(BaseModel):
    id: str
    text: str
    poll_id: str
    votes: List[str] = []  # user_ids who voted
    count: int = 0  # number of votes

class Poll(BaseModel):
    id: str
    question: str
    options: List[PollOption]
    voted_users: List[str] = []  # user_ids who have voted in this poll
    status: str = "active"  # poll status, default to active

# In-memory DB
polls_db: Dict[str, Poll] = {}
