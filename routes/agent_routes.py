# |method    | endpoint                     | goal                                         |
# |----------|------------------------------|----------------------------------------------|
# |post      |/agents                       | create a new agent                           |
# |get       |/agents                       | get all agents exist                         |
# |get       |/agents/{agent_id}            | get agent by id                              |
# |put       |/agents/{agent_id}            | update agent with id == id                   |
# |put       |/agents/{agent_id}/deactivate | deactivate agent with id == id               |
# |get       |/agents/{agent_id}/performance| summary of performance of agent with id == id|

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from logs.logger_config import logger
from database.agent_db import agent_manager
from mysql.connector import Error as MYSQL_ERROR

router = APIRouter()

def handle_id(agent_id: str)->int:
    try:
        return int(agent_id)
    except ValueError:
        logger.error("agent id must be an integer")
        raise HTTPException(422, "agent_id must be an integer")


@router.post("", status_code=201)
def add_new_agent(data: dict):
    try:
        if len(data) > 3:
            logger.error(f"user entered {list(data.keys())}, but only [name, specialty, agent rank] are valid")
            raise HTTPException(422, "only feilds [name, specialty, agent rank] are valid")
        logger.info("post/agents called")
        logger.info("adding a new agent")
        new_agent = agent_manager.create_agent(data)
        logger.info("agent created successfully")
        return {"data": new_agent}
    except MYSQL_ERROR as e:
        logger.error(f"code: {e.errno}, msg: {e.msg}")
        if e.errno == 1048:
            raise HTTPException(422, "feilds [name, specialty, agent rank] must be filled")
        elif e.errno == 1265:
            raise HTTPException(422, "feild agent_rank must be filled with 'Junior', 'Senior' or 'Commander'")
        raise HTTPException(422, e.msg)


@router.get("") 
def get_all_agents():
    logger.info("get/agents called")
    logger.info("getting list of all agents...")
    agents = agent_manager.get_all_agents()
    if not agents:
        logger.warning("There are no agents in DB")
    logger.info("getting list of all agents completed")
    return {"data": agents}


@router.get("/{agent_id}")
def get_agent_by_id(agent_id):
    logger.info(f"get/agents/{agent_id} called")
    agent_id = handle_id(agent_id)
    logger.info(f"start getting agent {agent_id}...")
    agent = agent_manager.get_agent_by_id(agent_id)
    if not agent:
        logger.error(f"agent {agent_id} not found")
        raise HTTPException(404, f"agent {agent_id} not found")
    logger.info(f"getting agent {agent_id} completed")
    return {"data": agent}


@router.put("/{agent_id}")
def update_agent(agent_id, data: dict):
    logger.info(f"put/agents/{agent_id} called")

    agent_id = handle_id(agent_id)
    agent = agent_manager.get_agent_by_id(agent_id)
    if not agent:
        logger.error(f"agent {agent_id} not found")
        raise HTTPException(404, f"agent {agent_id} not found")
   
    if not data:
        logger.error("user didn't enter any data")
        raise HTTPException(400, "you must enter some data")
    
    elif len(data) > 4:
        raise HTTPException(422, "only feilds [name, specialty, agent rank] can be filled")



    logger.info(f"start updating agent {agent_id}...")
    
    try:
        message = agent_manager.update_agent(agent_id, data)

    except MYSQL_ERROR as e:
        logger.error(f"code: {e.errno}, msg: {e.msg}")
        if e.errno == 1265:
            raise HTTPException(422, "feild agent_rank must be filled with 'Junior', 'Senior' or 'Commander'")
        raise HTTPException(422, e.msg)

    logger.info(f"agent {agent_id} updated successfully")
    return {"msg": message}

@router.put("/{agent_id}/deactivate")
def deactivate_agent(agent_id):
    logger.info(f"put/agents/{agent_id}/deactivate called")

    agent_id = handle_id(agent_id)
    agent = agent_manager.get_agent_by_id(agent_id)
    if not agent:
        logger.error(f"agent {agent_id} not found")
        raise HTTPException(404, f"agent {agent_id} not found")
    
    logger.info(f"start deactivating agent {agent_id}...")
    message = agent_manager.deactivate_agent(agent_id)
    logger.info(message)
    return {"msg": message}    


@router.get("/{agent_id}/performance")
def get_agent_performance(agent_id):
    logger.info(f"get/agents/{agent_id}/performance called")

    agent_id = handle_id(agent_id)
    agent = agent_manager.get_agent_by_id(agent_id)
    if not agent:
        logger.error(f"agent {agent_id} not found")
        raise HTTPException(404, f"agent {agent_id} not found")
    
    logger.info(f"start getting agent {agent_id} performance...")
    summary = agent_manager.get_agent_performance(agent_id)
    logger.info(f"getting agent {agent_id} performance completed")
    return {"data": summary}
    

    
