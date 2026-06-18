# |method | endpoint                  | goal                                                                        |
# |-------|---------------------------|-----------------------------------------------------------------------------|
# |get    |/reports/summary           |general report {active_agents_count, total_missions, open_missions, completed_missions, failed_missions, cancelled_missions}|
# |get    |/reports/mission-by-status | report { "open": , "in_progress": , "completed": , "failed": , "cancelled": }|
# |get    |/reports/top-agent         | report - the agent with most completed missions                              |

from fastapi import APIRouter

router = APIRouter()