from fastapi.routing import APIRouter, WebSocket
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from typing import Annotated
from loguru import logger
import asyncio
from celery.result import AsyncResult

from _celery.celery_main import celery_app

router = APIRouter(prefix="/api/job", tags=["job"])

connected_clients = set()  # Track connected clients


@router.websocket("/ws/task-state/{task_id}")
async def handle_task_state_websocket(websocket: WebSocket, task_id: str):
    try:

        async def inner():
            async_result = AsyncResult(task_id, app=celery_app)
            while True:
                state = async_result.state
                await websocket.send_text(state)
                # Prevent excessive updates (adjust as needed)
                await asyncio.sleep(2)

        await websocket.accept()
        connected_clients.add(websocket)
        await inner()
    except Exception as e:
        logger.error(f"Error handling websocket for task {task_id}: {e}")
    finally:
        connected_clients.remove(websocket)


@router.websocket("/ws/task-state/all")
async def handle_all_task_state_websocket(websocket: WebSocket):
    try:

        async def inner():
            while True:
                # Iterate through running tasks and send state updates
                for task_id, async_result in celery_app.control.inspect().active():
                    state = async_result.state
                    await websocket.send_text(f"{task_id}:{state}")
                # Adjust sleep interval as needed
                await asyncio.sleep(5)

        await websocket.accept()
        connected_clients.add(websocket)
        await inner()
    except Exception as e:
        logger.error(f"Error handling websocket for all tasks: {e}")
    finally:
        connected_clients.remove(websocket)


@router.get("/result/{task_id}")
async def get_task_result(task_id: str):
    try:
        result: AsyncResult = AsyncResult(task_id)
        logger.info(
            {
                "task_id": result.id,
                "status": result.status,
                "result": result.result if not result.traceback else str(result),
                "meta": result.info if not result.traceback else str(result.info),
            }
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "task_id": result.id,
                "status": result.status,
                "result": result.result if not result.traceback else str(result),
                "meta": result.info if not result.traceback else str(result.info),
            },
        )
        # return _to_task_out(result)
    except Exception as e:
        logger.error(f"Error retrieving task result: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
