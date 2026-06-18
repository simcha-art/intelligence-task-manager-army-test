# |Feild              |Type                          | Notes                                                   |
# |-------------------|------------------------------|---------------------------------------------------------|
# |id                 |INT PRIMARY KEY AUTO_INCREMENT|מזהה ייחודי                                             |
# |title              |VARCHAR NOT NULL              |כותרת המשימה                                            |
# |description        |TEXT NOT NULL                 |תיאור מפורט של המשימה                                   |
# |location           |VARCHAR NOT NULL              |מיקום                                                    |       
# |difficulty         |INT NOT NULL                  |1-10 בלבד                                                |
# |importance         |INT NOT NULL                  |1-10 בלבד                                                |
# |status             |ENUM                          | Defualt: NEW, options: [NEW, ASSIGNED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED]|
# |risk_level         |VARCHAR NOT NULL              |מחושב אוטומטית, לא מגיע מהמשתמש                        |
# |assigned_agent_id  |INT                           |default Null, when assigned -> the id number of the agent |



from database.db_connection import DB_conn
from database.agent_db import agent_manager

def calculate_risk_level(difficulty, importance):
    level =  difficulty * 2 + importance
    if level <= 9:
        return "LOW"
    elif level <= 18:
        return "MEDUIM"
    elif level < 24:
        return "HIGH"
    else:
        return "CRITICAL"
    
def valid_updating_status(current_status, new_status)-> bool:
    """
    only mission with status NEW can be assigned. after assignment it becomes ASSIGNED.
    only mission with status ASSIGNED can be started. after starting it becomes IN_PROGRESS.
    only mission with status IN_PROGRESS can be completed. after complete it becomes COMPLETED or FAILED.
    only mission with status NEW or ASSIGNED can be canceled, after cancel it becomes CANCELED.
    """
    if current_status == "NEW" and new_status == "ASSIGNED":
        return True
    elif current_status == "ASSIGNED" and new_status == "IN_PROGRESS":
        return True
    elif current_status == "IN_PROGRESS" and new_status in ["COMPLETED", "FAILED"]:
        return True
    elif current_status in ["NEW", "ASSIGNED"] and new_status == "CANCELLED":
        return True
    else:
        return False
    



class MissionDB:
    def create_mission(self, data: dict):
        title = data.get("title")
        description = data.get("description")
        location = data.get("location")
        difficulty = data.get("difficulty")
        importance = data.get("importance")
        risk_level = calculate_risk_level(difficulty, importance)
        params = (title, description, location, difficulty, importance, risk_level)


        query = """
        INSERT INTO missions
        (title, description, location, difficulty, importance, risk_level)
        VALUES
        (%s, %s, %s, %s, %s, %s)
        """

        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            DB_conn.conn.commit()
            new_id = cursor.lastrowid

        return self.get_mission_by_id(new_id)

    def get_all_missions(self):
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM missions")
            return cursor.fetchall()

    def get_mission_by_id(self, mission_id):
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM missions WHERE id = %s", (mission_id,))
            return cursor.fetchone()

    def assign_mission(self, agent_id: int, mission_id: int):
        query = """
        UPDATE missions
        SET
        assigned_agent_id = %s,
        status = 'ASSIGNED'
        WHERE id = %s
        """
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (agent_id, mission_id))
            DB_conn.conn.commit()
            if cursor.rowcount > 0:
                return f"mission {mission_id} assigned to agent {agent_id} successfully"
            else:
                return "fail to assign"

    def update_mission_status(self, mission_id: int, status: str)->str:
        
        with DB_conn.conn.cursor() as cursor:
            cursor.execute("UPDATE missions SET status = %s WHERE id = %s", (status, mission_id))
            DB_conn.conn.commit()
            return cursor.rowcount > 0


    def get_open_missions_by_agent(self, agent_id):
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM missions WHERE status IN ('ASSIGNED', 'IN_PROGRESS') AND assigned_agent_id = %s", (agent_id,))
            return cursor.fetchall()

    def count_all_missions(self):
        with DB_conn.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM missions")
            return cursor.fetchone()
        
    def count_by_status(self, status: str):
        with DB_conn.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM missions WHERE status = %s", (status,))
            return cursor.fetchone()
        
    def count_open_missions(self):
        with DB_conn.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM missions WHERE status IN ('NEW', 'ASSIGNED', 'IN_PROGRESS')")
            return cursor.fetchone()
        
    def count_critical_missions(self):
        with DB_conn.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM missions WHERE risk_level = 'CRITICAL'")
            return cursor.fetchone()
        
    def get_top_agent(self):
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1")
            return cursor.fetchone()




mission_manager = MissionDB()


# agent_manager.create_agent({"name": "simcha", "specialty": "psychologic", "agent_rank": "Senior"})
# agent_manager.increment_completed(10)
# agent_manager.increment_completed(10)
# agent_manager.increment_completed(10)
# agent_manager.increment_completed(10)
# agent_manager.increment_completed(10)
# agent_manager.increment_completed(10)
# agent_manager.increment_completed(10)
# agent_manager.increment_completed(10)
# agent_manager.increment_completed(10)

# all = mission_manager.count_all_missions()
# open = mission_manager.count_open_missions()
# by_status = mission_manager.count_by_status("CANCELLED")
# criticals = mission_manager.count_critical_missions()
# top = mission_manager.get_top_agent()
# print(all, open, by_status, criticals, top, sep="\n")

















# for agent in agent_manager.get_all_agents():
#     print(agent["id"])

# print(mission_manager.create_mission({"title": "hello", "description": "world", "location": "here", "difficulty": 2, "importance": 2}))

# for mission in mission_manager.get_all_missions():
#     print(mission["id"])

# agent_manager.update_agent(9, {"is_active": True, "agent_rank": "Commander"})
# print(mission_manager.assign_mission(9, 4))
# print(mission_manager.assign_mission(9, 5))
# print(mission_manager.assign_mission(9, 6))
# print(mission_manager.assign_mission(9, 7))
# print(mission_manager.get_open_mission_by_agent(9))
# print(mission_manager.update_mission_status(4, "IN_PROGRESS"))