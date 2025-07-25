from fastapi import Body
from fastapi import APIRouter, HTTPException
from models import Poll, PollOption, polls_db
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()

# Endpoint to update poll status
@router.put("/polls/{poll_id}/status")
def update_poll_status(poll_id: str, status: dict = Body(...)):
    poll = polls_db.get(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found.")
    new_status = status.get("status")
    if new_status not in ["active", "closed"]:
        raise HTTPException(status_code=400, detail="Invalid status value.")
    poll.status = new_status
    return {"message": f"Poll status updated to {new_status}", "poll": poll}


from fastapi import APIRouter, HTTPException
from models import Poll, PollOption, polls_db
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()

# Endpoint to get all active polls
@router.get("/polls/active")
def get_active_polls():
    active_polls = [poll for poll in polls_db.values() if poll.status == "active"]
    return active_polls

class CreatePollRequest(BaseModel):
    id: str
    question: str
    options: List[str]

@router.post("/polls/")
def create_poll(req: CreatePollRequest):
    if req.id in polls_db:
        raise HTTPException(status_code=400, detail="Poll ID already exists.")
    options = [PollOption(id=str(uuid.uuid4()), text=opt, poll_id=req.id) for opt in req.options]
    poll = Poll(id=req.id, question=req.question, options=options)
    polls_db[req.id] = poll
    return {"message": "Poll created", "poll": poll}


from fastapi import HTTPException
from models import Poll, PollOption, polls_db
from pydantic import BaseModel
from typing import List
import uuid

class CreatePollRequest(BaseModel):
    id: str
    question: str
    options: List[str]

class VoteRequest(BaseModel):
    option_id: str
    user_id: str

def create_poll_controller(req: CreatePollRequest):
    if req.id in polls_db:
        raise HTTPException(status_code=400, detail="Poll ID already exists.")
    options = [PollOption(id=str(uuid.uuid4()), text=opt, poll_id=req.id) for opt in req.options]
    poll = Poll(id=req.id, question=req.question, options=options)
    polls_db[req.id] = poll
    return {"message": "Poll created", "poll": poll}

def vote_poll_controller(poll_id: str, req: VoteRequest):
    poll = polls_db.get(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found.")
    if poll.status == "closed":
        raise HTTPException(status_code=403, detail="Poll is closed. Voting is not allowed.")
    option = next((opt for opt in poll.options if opt.id == req.option_id), None)
    if not option:
        raise HTTPException(status_code=404, detail="Option not found.")
    if req.user_id in poll.voted_users:
        raise HTTPException(status_code=400, detail="User already voted.")
    option.votes.append(req.user_id)
    option.count += 1
    poll.voted_users.append(req.user_id)
    return {"message": "Vote recorded", "option": option}

def get_poll_results_controller(poll_id: str):
    poll = polls_db.get(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found.")
    return {
        "id": poll.id,
        "question": poll.question,
        "options": [
            {"id": opt.id, "text": opt.text, "count": opt.count} for opt in poll.options
        ]
    }

def update_poll_status_controller(poll_id: str, status: str):
    poll = polls_db.get(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found.")
    if status not in ["active", "closed"]:
        raise HTTPException(status_code=400, detail="Invalid status value.")
    poll.status = status
    return {"message": f"Poll status updated to {status}", "poll": poll}

def get_active_polls_controller():
    return [poll for poll in polls_db.values() if poll.status == "active"]