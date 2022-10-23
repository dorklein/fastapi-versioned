from fastapi import FastAPI
from starlette.websockets import WebSocket

from fastapi_versioned import VersionedFastAPI

app = FastAPI(title="My Online Store")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
        return


app = VersionedFastAPI(app)
