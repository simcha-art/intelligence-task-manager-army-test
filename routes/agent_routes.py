# |method    | endpoint                     | goal                                         |
# |----------|------------------------------|----------------------------------------------|
# |post      |/agents                       | create a new agent                           |
# |get       |/agents                       | get all agents exist                         |
# |get       |/agents/{agent_id}            | get agent by id                              |
# |put       |/agents/{agent_id}            | update agent with id == id                   |
# |put       |/agents/{agent_id}/deactivate | deactivate agent with id == id               |
# |get       |/agents/{agent_id}/preformance| summary of performance of agent with id == id|


from fastapi import APIRouter

router = APIRouter()