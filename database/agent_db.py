"""
AgentDB

|method                         | goal                                             | returns                                                           |
|-------------------------------|--------------------------------------------------|-------------------------------------------------------------------|
|create_agent(data)             |adds a new agent                                  |dictionary of the new agent                                        |
|get_all_agents()               |returns a list of all existing agents             |list of all agents                                                 |
|get_agent_by_id(agent_id)      |returns the agent with id == id                   |dictionary of the agent or None if not exist                       |
|update_agent(agent_id, data)   |updating details of existing agent with id == id  |True(success) or False (failed)                                    |
|deactivate_agent(agent_id)     |updating feild "is_active" to False               |True(success) or False (failed)                                    |
|increment_completed(agent_id)  |adding 1 to field "comleted_missions"             |True(success) or False (failed)                                    |
|increment_completed(agent_id)  |adding 1 to field "comleted_missions"             |True(success) or False (failed)                                    |
|increment_failed(agent_id)     |adding 1 to field "failed_missions"               |True(success) or False (failed)                                    |
|get_agent_performance(agent_id)|returns a summary of the performance of the agent |dict {total: int, completed: int, failed: int, success_rate: completed / total * 100}
|count_active_agents()          |counts the number of active agents                |int                                                                 |
"""

from database.db_connection import DB_conn
import mysql.connector

            # name VARCHAR(100) NOT NULL,
            # specialty VARCHAR(150) NOT NULL,
            # is_active BOOLEAN DEFAULT TRUE,
            # completed_missions INT DEFAULT 0,
            # failed_missions INT DEFAULT 0,
            # agent_rank ENUM('Junior', 'Senior', 'Commander')
            # )

class AgentDB:
    def create_agent(self, data: dict):
        name = data.get("name")