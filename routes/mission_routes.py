# |method    | endpoint                               | goal                                           |
# |----------|----------------------------------------|------------------------------------------------|
# |post      |/missions                               | create a new mission                           |
# |get       |/missions                               | get all missions exist                         |
# |get       |/missions/{mission_id}                  | get mission by id                              |
# |put       |/missions/{mission_id}/assign/{agent_id}| assign mission to agent + 6 validations        |
# |put       |/missions/{mission_id}/start            | start mission (assigned -> in_progress)        |
# |put       |/missions/{mission_id}/complete         | complete mission (in_progress -> completed)    |
# |put       |/missions/{mission_id}/fail             | mission faile (in_progress -> failed)          |
# |put       |/missions/{mission_id}/cancel           | start mission (new/assigned -> cancelled)      |

from fastapi import APIRouter

router = APIRouter()