# intelligence-task-manager-army-test

**יחידת מודיעין צריכה מערכת לניהול סוכנים ומשימות. מערכת זו מנהלת בסיס נתונים על מנת לנהל את הסוכנים והמשימות ביעילות.**

<br>
<br>
<br>
<br>
<br>

## File structure

``` text

intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore

```
<br>
<br>
<br>
<br>


## Mission Table

|Feild              |Type                          | Notes                                                   |
|-------------------|------------------------------|---------------------------------------------------------|
|id                 |INT PRIMARY KEY AUTO_INCREMENT|מזהה ייחודי                                             |
|title              |VARCHAR NOT NULL              |כותרת המשימה                                            |
|description        |TEXT NOT NULL                 |תיאור מפורט של המשימה                                   |
|location           |VARCHAR NOT NULL              |מיקום                                                    |       
|difficulty         |INT NOT NULL                  |1-10 בלבד                                                |
|importance         |INT NOT NULL                  |1-10 בלבד                                                |
|status             |ENUM                          | Defualt: NEW, options: [NEW, ASSIGNED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED]|
|risk_level         |VARCHAR NOT NULL              |מחושב אוטומטית, לא מגיע מהמשתמש                        |
|assigned_agent_id  |INT                           |default Null, when assigned -> the id number of the agent |
___

<br>
<br>
<br>

## Agent Table

|Feild              |Type                          | Notes                                                   |
|-------------------|------------------------------|---------------------------------------------------------|
|id	                |INT AUTO_INCREMENT PRIMARY KEY|        	מזהה ייחודי                                 |
|name	            |VARCHAR NOT NULL	           |            שם הסוכן                                    |
|specialty	        |VARCHAR NOR NULL              |                תחום התמחות                             |
|is_active	        |BOOLEAN NOR NULL              |            ברירת מחדל: TRUE                            |
|completed_missions	|INT	                       |                ברירת מחדל: 0                           |
|failed_missions	|INT	                       |                ברירת מחדל: 0                           |
|agent_rank	        |ENUM	                       |            Junior / Senior / Commander בלבד            |
___
<br>
<br>
<br>
<br>
<br>
<br>


## CLASSES
<br>
<br>

### DB_connection
<br>

This class response to connect to docker container and to the DB in it.
<br>

### methods:<br>

**get_connection()** ---> returns an active connection to the database (mysql)<br>
**create_database()** ---> create the database if not exists<br>
**create_tables()** -> create the tablse mission and agent if they are not exists<br>

<br>
<br>
<br>

### AgentDB

|method                         | goal                                             | returns                                                           |
|-------------------------------|--------------------------------------------------|-------------------------------------------------------------------|
|create_agent(data)             |adds a new agent                                  |dictionary of the new agent                                        |
|get_all_agents()               |returns a list of all existing agents             |list of all agents                                                 |
|get_agent_by_id(agent_id)      |returns the agent with id == id                   |dictionary of the agent or None if not exist                       |
|update_agent(agent_id, data)   |updating details of existing agent with id == id  |message of success or failure                                    |
|deactivate_agent(agent_id)     |updating feild "is_active" to False               |message of success or failure                                    |
|increment_completed(agent_id)  |adding 1 to field "comleted_missions"             |message of success or failure                                    |
|increment_failed(agent_id)     |adding 1 to field "failed_missions"               |message of success or failure                                    |
|get_agent_performance(agent_id)|returns a summary of the performance of the agent |dict {total: int, completed: int, failed: int, success_rate: completed / total * 100}
|count_active_agents()          |counts the number of active agents                |int                                                                 |
___
<br>
<br>
<br>
<br>

### MissionDB

|method                              | goal                                                 | returns                                                           |
|------------------------------------|------------------------------------------------------|-------------------------------------------------------------------|
|create_method(data)                 |add a new mission                                     |dictionary of the new mission
|get_all_missions()                  |returns a list of all missions                        |list of dictionaries.
|get_mission_by_id(mission_id)       |returns a specific mission where id == id             |dictionary or None if mission not exists
|assign_mission(agent_id, mission_id)|change feild "assign_agent_id" from Null to agent_id  |message of success or failure
|update_mission_status(m_id, status) |change feild "status"                                 |message of success or failure
|get_open_mission_by_agent(agent_id) |get all mission with status("assigned"\in_progress) witch assinged to agent_id|       list of dict or empty list |
|count_all_missions()                |count all missions                                    | int
|count_by_status(status)             |count all mission with status == status               | int
|count_open_missions()               |count all mission with status (new/assigned/in_progress)| int
|count_critical_missions()           |count all missions with risk_level = CRITICAL         | int
|get_top_agent()                     |find the agent with the higest completed missions     |dictionary of the agent
___
<br>
<br>
<br>
<br>
<br>

## Rules
1. runk must be Junior / Senior / Commander
2. difficulty and importance must by between 1-10.
3. risk_level is not assigned by the user, it is calculated automatically
4. inactive agent cannot accept missions.
5. agent cannot hold more then 3 open missions(ASSIGNED/ IN_PROGRESS) at once.
6. only agent with rank = Commander can accept CRITICAL missions.
7. only mission with status NEW can be assigned. after assignment it becomes ASSIGNED.
8. only mission with status ASSIGNED can be started. after starting it becomes IN_PROGRESS.
9. only mission with status IN_PROGRESS can be completed. after complete it becomes COMPLETED or FAILED.
10. only mission with status NEW or ASSIGNED can be canceled, after cancel it becomes CANCELED.



## How to run

``` text
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
pip install -r requirements.txt

```
