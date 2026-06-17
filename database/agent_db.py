
from db_connection import DB_conn


class AgentDB:
    def create_agent(self, data: dict):
        name = data.get("name")
        specialty = data.get('specialty')
        agent_rank = data.get("agent_rank")
        query = """
        INSERT INTO agents
        (name, specialty, agent_rank)
        VALUES
        (%s, %s, %s)
        """
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (name, specialty, agent_rank))
            DB_conn.conn.commit()
            success = cursor.rowcount > 0
            if not success:
                return None
            new_id = cursor.lastrowid
            cursor.execute(f"SELECT * FROM agents WHERE id = {new_id}")
            return cursor.fetchone()


    def get_all_agents(self):
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM agents")
            return cursor.fetchall()
        
    def get_agent_by_id(self, agent_id):
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM agents WHERE id = %s", (agent_id,))
            return cursor.fetchone()
        
    def update_agent(self, agent_id: int, data: dict):
        if "id" in data: 
            raise ValueError ("must not update id")
        set_cluase = ", ".join(f"{feild} = %s " for feild in data.keys())
        values = list(data.values())
        params = values + [agent_id]

        query = f"""
        UPDATE agents
        SET
        {set_cluase}
        WHERE id = %s
        """

        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            DB_conn.conn.commit()
            same = cursor.warning_count == 0
            success = cursor.rowcount > 0
            if same:
                return "agent already up to date"
            if success:
                return "updated successfully"
            else:
                return "update failed"
        
    def deactivate_agent(self, agent_id):
        query = "UPDATE agents SET is_active = FALSE WHERE ID = %s"
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (agent_id,))
            DB_conn.conn.commit()
            success = cursor.rowcount > 0   
            if success:
                return "deactivated successfully"
            else:
                return "deactivate failed" 
        
    def increment_completed(self, agent_id):
        with DB_conn.conn.cursor() as cursor:
            cursor.execute("UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s", (agent_id,))
            DB_conn.conn.commit()
            success = cursor.rowcount > 0
            if success:
                return "feild completed_missions incremented successfully"
            else:
                return "failed to increment"
    
    def increment_failed(self, agent_id):
        with DB_conn.conn.cursor() as cursor:
            cursor.execute("UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s", (agent_id,))
            DB_conn.conn.commit()
            success = cursor.rowcount > 0
            if success:
                return "feild failed_missions incremented successfully"
            else:
                return "failed to increment"
            
    def get_agent_performance(self, agent_id):
        query = "SELECT completed_missions, failed_missions FROM agents WHERE id = %s"
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (agent_id,))
            result = cursor.fetchone()

        if not result:
            return f"agent {agent_id} not found"
        
        completed_missions = result["completed_missions"]
        failed_missions = result["failed_missions"]
        total = completed_missions + failed_missions
        success_rate = None if total == 0 else completed_missions / total * 100

        return {
            "total": total,
            "completed_missions": completed_missions,
            "failed_missions": failed_missions,
            "success_rate": success_rate
                }
    
    def count_active_agents(self):
        query = """
        SELECT COUNT(*) AS active_agents FROM agents
        WHERE is_active = TRUE
        """
        with DB_conn.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return cursor.fetchone()







agent_manager = AgentDB()
