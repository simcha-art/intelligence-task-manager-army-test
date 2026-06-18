# |method    | endpoint                               | goal                                           |
# |----------|----------------------------------------|------------------------------------------------|
# |post      |/missions                               | create a new mission                           |
# |get       |/missions                               | get all missions exist                         |
# |get       |/missions/{mission_id}                  | get mission by id                              |
# |put       |/missions/{mission_id}/assign/{agent_id}| assign mission to agent + 6 validations        |
# |put       |/missions/{mission_id}/start            | start mission (assigned -> in_progress)        |
# |put       |/missions/{mission_id}/complete         | complete mission (in_progress -> completed)    |
# |put       |/missions/{mission_id}/fail             | mission faile (in_progress -> failed)          |
# |put       |/missions/{mission_id}/cancel           | cancel mission (new/assigned -> cancelled)      |

from fastapi import APIRouter, HTTPException
from database.mission_db import mission_manager, valid_updating_status
from database.agent_db import agent_manager
from mysql.connector import Error as MYSQL_ERROR
from logs.logger_config import logger

FEILDS = ["title", "description", "location", "difficulty", "importance"]


def handle_id(mission_id: str):
    try:
        return int(mission_id)
    except ValueError:
        raise HTTPException(422, "id must be integer")


router = APIRouter()


@router.post("", status_code=201)
def add_new_mission(data: dict):
    if len(data) > 5:
        raise HTTPException(422, f"feilds must be only {FEILDS}")
    if sorted(data.keys()) != sorted(FEILDS):
        raise HTTPException(422, f'feilds {FEILDS} must be filled')
    
    try:
        mission = mission_manager.create_mission(data)
        return {"data": mission}
    
    except MYSQL_ERROR as e:
        logger.error(f"database_error: code: {e.errno}, msg: {e.msg}")
        if e.errno == 3819:
            raise HTTPException(400, "importance and difficulty must be integers from 1 to 10")
        raise HTTPException(422, f"database error, {e.errno}, {e.msg}")
    
    except TypeError:
        raise HTTPException(400, "importance and difficulty must be integers")


@router.get("")
def get_all_missions():
    missions = mission_manager.get_all_missions()
    if not missions:
        logger.warning("There are no mission in DB")
    return {"data": missions}


@router.get("/{mission_id}")
def get_mission_by_id(mission_id):
    mission_id = handle_id(mission_id)
    mission = mission_manager.get_mission_by_id(mission_id)
    if not mission:
        raise HTTPException(404, f"mission {mission_id} not found")
    return {"data": mission}


@router.get("/{mission_id}/assign/{agent_id}")
def assign_mission_to_agent(mission_id, agent_id):
    mission_id = handle_id(mission_id)
    agent_id = handle_id(agent_id)

    mission = mission_manager.get_mission_by_id(mission_id)
    if not mission:
        raise HTTPException(404, f"mission {mission_id} not found")
    
    agent = agent_manager.get_agent_by_id(agent_id)
    if not agent:
        raise HTTPException(404, f"agent {agent_id} not found")
   
    #rule number 7, only new mission can be assigned
    status = mission["status"]
    if status != "NEW":
        raise HTTPException(400, "Only new missions can be assigned")
    
    #rule number 4 only active agent can accept missions
    if not agent['is_active']:
        raise HTTPException(400, f"agent {agent_id} is inactive")
    
    #rule number 6, only agent with rank = Commander can accept CRITICAL missions.
    if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
        raise HTTPException(400, "mission with risk_level of 'critical' can be assigned only to commander")
    
    #rule number 5, agent cannot hold more then 3 open missions(ASSIGNED/ IN_PROGRESS) at once.
    num_of_open_missions_of_agent = len(mission_manager.get_open_missions_by_agent(agent_id))
    if num_of_open_missions_of_agent >= 3:
        raise HTTPException(400, f"agent {agent_id} has reached maximum open missions: 3")
    
    msg = mission_manager.assign_mission(agent_id, mission_id)
    return {"msg": msg}


@router.put("/{mission_id}/start")
def start_mission(mission_id):
    mission_id = handle_id(mission_id)
    mission = mission_manager.get_mission_by_id(mission_id)
    if not mission:
        raise HTTPException(404, f"mission {mission_id} not found")
    
    current_status = mission["status"]
    new_status = "IN_PROGRESS"
    if not valid_updating_status(current_status, new_status):
        raise HTTPException(400, "Only mission with status 'ASSIGNED' can be started")

    
    mission_manager.update_mission_status(mission_id, "IN_PROGRESS")
    return {"msg": f"mission {mission_id} has started"}



@router.put("/{mission_id}/complete")
def complete_mission(mission_id):
    mission_id = handle_id(mission_id)
    mission = mission_manager.get_mission_by_id(mission_id)
    if not mission:
        raise HTTPException(404, f"mission {mission_id} not found")
    
    current_status = mission["status"]
    new_status = "COMPLETED"
    if not valid_updating_status(current_status, new_status):
        raise HTTPException(400, "Only mission with status 'IN_PROGRESS' can be completed")

    
    mission_manager.update_mission_status(mission_id, "COMPLETED")
    agent_manager.increment_completed(mission["assigned_agent_id"])
    return {"msg": f"mission {mission_id} has completed"}


@router.put("/{mission_id}/fail")
def fail_mission(mission_id):
    mission_id = handle_id(mission_id)
    mission = mission_manager.get_mission_by_id(mission_id)
    if not mission:
        raise HTTPException(404, f"mission {mission_id} not found")
    
    current_status = mission["status"]
    new_status = "FAILED"
    if not valid_updating_status(current_status, new_status):
        raise HTTPException(400, "Only mission with status 'IN_PROGRESS' can be failed")

    
    mission_manager.update_mission_status(mission_id, "FAILED")
    agent_manager.increment_failed(mission["assigned_agent_id"])
    return {"msg": f"mission {mission_id} has failed"}


@router.put("/{mission_id}/cancel")
def cancel_mission(mission_id):
    mission_id = handle_id(mission_id)
    mission = mission_manager.get_mission_by_id(mission_id)
    if not mission:
        raise HTTPException(404, f"mission {mission_id} not found")
    
    current_status = mission["status"]
    new_status = "CANCELLED"
    if not valid_updating_status(current_status, new_status):
        raise HTTPException(400, "Only mission with status 'NEW' or 'ASSIGNED' can be cancelled")

    
    mission_manager.update_mission_status(mission_id, "CANCELLED")
    return {"msg": f"mission {mission_id} has canceled"}

        
    

