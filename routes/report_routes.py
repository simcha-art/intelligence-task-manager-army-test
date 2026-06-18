# |method | endpoint                  | goal                                                                        |
# |-------|---------------------------|-----------------------------------------------------------------------------|
# |get    |/reports/summary           |general report {active_agents_count, total_missions, open_missions, completed_missions, failed_missions, cancelled_missions}|
# |get    |/reports/mission-by-status | report { "open": , "in_progress": , "completed": , "failed": , "cancelled": }|
# |get    |/reports/top-agent         | report - the agent with most completed missions                              |

from fastapi import APIRouter, HTTPException
from database.agent_db import agent_manager
from database.mission_db import mission_manager
from logs.logger_config import logger

router = APIRouter()

@router.get("/summary")
def get_general_summary():
    active_agents_count = agent_manager.count_active_agents()["active_agents"]
    total_missions = mission_manager.count_all_missions()["total_missions"]
    open_missions = mission_manager.count_open_missions()["open_missions"]
    completed_missions = mission_manager.count_by_status("COMPLETED")["total"]
    failed_missions = mission_manager.count_by_status("FAILED")["total"]
    cancelled_missions = mission_manager.count_by_status("CANCELLED")["total"]
    return {"data":{
        "active_agents_count": active_agents_count,
        "total_missions": total_missions,
        "open_missions": open_missions,
        "completed_missions": completed_missions,
        "failed_missions": failed_missions,
        "cancelled_missions": cancelled_missions
    }}


@router.get("/mission-by-status")
def get_mission_by_status():
    new = mission_manager.count_by_status("NEW")["total"]
    assigned = mission_manager.count_by_status("ASSIGNED")["total"]
    open = new + assigned

    in_progress = mission_manager.count_by_status("IN_PROGRESS")["total"]
    completed = mission_manager.count_by_status("COMPLETED")["total"]
    failed = mission_manager.count_by_status("FAILED")["total"]
    cancelled = mission_manager.count_by_status("CANCELLED")["total"]
    return {"data": {
        "open": open,
        "in_progress": in_progress,
        "completed": completed,
        "failed": failed,
        "cancelled": cancelled
    }}


@router.get("/top-agent")
def get_top_agent():
    return {"data": mission_manager.get_top_agent()}