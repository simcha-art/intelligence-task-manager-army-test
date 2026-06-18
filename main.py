from fastapi import FastAPI, exception_handlers, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from logs.logger_config import logger
from database.db_connection import DB_conn
from routes.agent_routes import router as agents_router
from routes.mission_routes import router as missions_router
from routes.report_routes import router as reports_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    DB_conn.get_connection()
    DB_conn.create_database()
    DB_conn.create_tables()

    yield

    DB_conn.conn.close()


app = FastAPI(lifespan=lifespan)


app.include_router(agents_router, prefix="/agents", tags=["agents"])
app.include_router(missions_router, prefix="/missions", tags=["missions"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])