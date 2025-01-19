import dataclasses
import uuid

from collections import defaultdict
from fastapi import FastAPI, Path
from fastapi.websockets import (
    WebSocket,
    WebSocketDisconnect,
)


# Create FastAPI application
application = FastAPI()


@dataclasses.dataclass
class Connection:

    """
    WebSocket connection
    """

    websockets: set[WebSocket] = dataclasses.field(default_factory=set)


# Websocket connection registry
connections: defaultdict[str, defaultdict[uuid.UUID, Connection]] =\
    defaultdict(lambda: defaultdict(Connection))


@application.websocket("/ws/{namespace}/{connection_id}/")
async def onconnect(

    # WebSocket instance
    websocket: WebSocket,

    # WebSocket namespace
    namespace: str = Path(...),

    # WebSocket connection
    connection_id: uuid.UUID = Path(...),
):

    # Check if namespace is permitted
    if namespace not in {"group", "meeting"}:

        # Close WebSocket connection
        await websocket.close()

        # Return
        return

    # Accept WebSocket connection
    await websocket.accept()

    # Get WebSocket connection
    connection = connections[namespace][connection_id]
    connection.websockets.add(websocket)

    try:
        # Receive empty messages for stay connected
        while True:

            # Receive WebSocket message
            await websocket.receive_text()

    except WebSocketDisconnect:

        # Remove WebSocket connection
        connection.websockets.discard(websocket)

        # Remove group from connections
        if not connection.websockets:

            # Pop WebSocket connection
            connections[namespace].pop(connection)

        # Remove namespace from connections
        if not connections[namespace]:

            # Pop WebSocket connection
            connections.pop(namespace)


@application.post("/on/{namespace}/{connection_id}/{command}/")
async def onmessage(

    # WebSocket namespace
    namespace: str = Path(...),

    # WebSocket connection
    connection_id: uuid.UUID = Path(...),

    # WebSocket message
    command: str = Path(...)
):
    # Check if namespace is permitted
    if any([
        namespace not in {"group", "meeting"},
        command not in {"message.create"}
    ]):
        # Close WebSocket connection
        await websocket.close()

        # Return
        return

    # Get WebSocket connection
    connection = connections[namespace].get(connection_id)

    # Check if connection exists
    if connection:

        # Send notification
        for websocket in connection.websockets:

            try:
                # Send notification
                await websocket.send_text(command.upper())

            except Exception:

                # Remove WebSocket connection
                connection.websockets.discard(websocket)

    elif connection is not None:

        # Remove WebSocket connection
        connections[namespace].pop(connection_id)
