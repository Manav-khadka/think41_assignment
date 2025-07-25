from fastapi import APIRouter, Body
from poll_controller import (
    CreatePollRequest, VoteRequest,
    create_poll_controller, vote_poll_controller,
    get_poll_results_controller, update_poll_status_controller, get_active_polls_controller
)

router = APIRouter()

@router.post("/polls/")
def create_poll(req: CreatePollRequest):
    return create_poll_controller(req)

@router.post("/polls/{poll_id}/vote")
def vote_poll(poll_id: str, req: VoteRequest):
    return vote_poll_controller(poll_id, req)

@router.get("/polls/{poll_id}/results")
def get_poll_results(poll_id: str):
    return get_poll_results_controller(poll_id)

@router.put("/polls/{poll_id}/status")
def update_poll_status(poll_id: str, status: dict = Body(...)):
    return update_poll_status_controller(poll_id, status.get("status"))

@router.get("/polls/active")
def get_active_polls():
    return get_active_polls_controller()
