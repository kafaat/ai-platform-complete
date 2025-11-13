"""
Agents Orchestrator Service
Manages and orchestrates AI agents for various tasks
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum
import os
import logging
from datetime import datetime
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agents Orchestrator",
    description="AI Agents orchestration and management API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class AgentType(str, Enum):
    SUPPORT = "support"
    FRAUD_DETECTION = "fraud_detection"
    RECOMMENDATION = "recommendation"
    CONTENT_MODERATION = "content_moderation"
    CODE_REVIEW = "code_review"
    DATA_ANALYSIS = "data_analysis"

class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

# Models
class AgentTask(BaseModel):
    agent_type: AgentType
    task_data: Dict[str, Any]
    priority: Optional[int] = 1
    timeout_seconds: Optional[int] = 300

class AgentTaskResponse(BaseModel):
    task_id: str
    agent_type: AgentType
    status: AgentStatus
    result: Optional[Dict[str, Any]] = None
    created_at: str
    completed_at: Optional[str] = None

class AgentInfo(BaseModel):
    agent_type: AgentType
    name: str
    description: str
    capabilities: List[str]
    status: str
    active_tasks: int

# Agent registry
AGENT_REGISTRY = {
    AgentType.SUPPORT: {
        "name": "Customer Support Agent",
        "description": "Handles customer support inquiries and tickets",
        "capabilities": ["ticket_analysis", "response_generation", "sentiment_analysis"],
        "status": "active",
        "active_tasks": 0
    },
    AgentType.FRAUD_DETECTION: {
        "name": "Fraud Detection Agent",
        "description": "Detects fraudulent activities and anomalies",
        "capabilities": ["transaction_analysis", "pattern_detection", "risk_scoring"],
        "status": "active",
        "active_tasks": 0
    },
    AgentType.RECOMMENDATION: {
        "name": "Recommendation Agent",
        "description": "Provides personalized recommendations",
        "capabilities": ["collaborative_filtering", "content_based", "hybrid_recommendations"],
        "status": "active",
        "active_tasks": 0
    },
    AgentType.CONTENT_MODERATION: {
        "name": "Content Moderation Agent",
        "description": "Moderates user-generated content",
        "capabilities": ["text_moderation", "image_moderation", "toxicity_detection"],
        "status": "active",
        "active_tasks": 0
    },
    AgentType.CODE_REVIEW: {
        "name": "Code Review Agent",
        "description": "Reviews code for quality and security",
        "capabilities": ["static_analysis", "security_scan", "best_practices"],
        "status": "active",
        "active_tasks": 0
    },
    AgentType.DATA_ANALYSIS: {
        "name": "Data Analysis Agent",
        "description": "Analyzes data and generates insights",
        "capabilities": ["statistical_analysis", "visualization", "reporting"],
        "status": "active",
        "active_tasks": 0
    }
}

# Task storage (in-memory for demo)
tasks_db = {}

@app.get("/")
async def root():
    return {
        "service": "Agents Orchestrator",
        "version": "1.0.0",
        "status": "operational",
        "agents_available": len(AGENT_REGISTRY)
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "agents-orchestrator"
    }

@app.get("/agents", response_model=List[AgentInfo])
async def list_agents():
    """List all available agents"""
    return [
        AgentInfo(agent_type=agent_type, **agent_data)
        for agent_type, agent_data in AGENT_REGISTRY.items()
    ]

@app.get("/agents/{agent_type}", response_model=AgentInfo)
async def get_agent_info(agent_type: AgentType):
    """Get information about a specific agent"""
    if agent_type not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return AgentInfo(agent_type=agent_type, **AGENT_REGISTRY[agent_type])

@app.post("/tasks", response_model=AgentTaskResponse)
async def create_task(task: AgentTask):
    """Create a new agent task"""
    task_id = str(uuid.uuid4())
    
    # Simulate task execution
    result = {
        "status": "processed",
        "agent": task.agent_type.value,
        "data": task.task_data,
        "confidence": 0.95
    }
    
    task_response = AgentTaskResponse(
        task_id=task_id,
        agent_type=task.agent_type,
        status=AgentStatus.COMPLETED,
        result=result,
        created_at=datetime.utcnow().isoformat(),
        completed_at=datetime.utcnow().isoformat()
    )
    
    tasks_db[task_id] = task_response
    
    logger.info(f"Task created: {task_id} for agent {task.agent_type}")
    
    return task_response

@app.get("/tasks/{task_id}", response_model=AgentTaskResponse)
async def get_task(task_id: str):
    """Get task status and result"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks_db[task_id]

@app.get("/tasks")
async def list_tasks(agent_type: Optional[AgentType] = None, limit: int = 100):
    """List all tasks, optionally filtered by agent type"""
    tasks = list(tasks_db.values())
    
    if agent_type:
        tasks = [t for t in tasks if t.agent_type == agent_type]
    
    return {
        "total": len(tasks),
        "tasks": tasks[:limit]
    }

@app.get("/metrics")
async def get_metrics():
    """Get orchestrator metrics"""
    return {
        "total_agents": len(AGENT_REGISTRY),
        "active_agents": len([a for a in AGENT_REGISTRY.values() if a["status"] == "active"]),
        "total_tasks": len(tasks_db),
        "completed_tasks": len([t for t in tasks_db.values() if t.status == AgentStatus.COMPLETED]),
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
