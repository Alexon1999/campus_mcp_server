from fastapi import FastAPI
from app.database import Base, engine
from app.routers import classes, schedules
from app.mcp.server import router as mcp_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="School API + MCP Server")

# REST API
app.include_router(classes.router, prefix="/api")
app.include_router(schedules.router, prefix="/api")

# MCP Server
app.include_router(mcp_router, prefix="/mcp")

@app.get("/api/health")
def api_health():
    return {"status": "ok"}
