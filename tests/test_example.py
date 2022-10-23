import pytest
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from example.annotation.app import app as annotation_app
from example.custom_default_version.app import app as default_version_app
from example.router.app import app as router_app
from example.ws_app.app import app as ws_app


def test_annotation_app() -> None:
    test_client = TestClient(annotation_app)
    assert test_client.get("/docs").status_code == 200
    assert test_client.get("/v1_0/docs").status_code == 200
    assert test_client.get("/v1_1/docs").status_code == 200
    assert test_client.get("/v1_2/docs").status_code == 200
    assert test_client.get("/v1_3/docs").status_code == 200
    assert test_client.get("/latest/docs").status_code == 200
    assert test_client.get("/v1_4/docs").status_code == 404

    assert test_client.get("/v1_0/item/1").status_code == 404
    assert test_client.get("/v1_1/item/1").status_code == 200
    assert test_client.get("/v1_1/item/1").json()["quantity"] == 5
    complex_quantity = [{"store_id": "1", "quantity": 5}]

    assert test_client.get("/v1_2/item/1").json()["quantity"] == complex_quantity
    assert test_client.get("/v1_3/item/1").json()["quantity"] == complex_quantity

    assert test_client.get("/latest/item/1").json()["quantity"] == complex_quantity

    item = {
        "id": "1",
        "name": "apple",
        "price": 1.0,
        "quantity": complex_quantity,
    }
    assert (
        test_client.post(
            "/v1_3/item",
            json=item,
        ).json()
        == item
    )
    assert (
        test_client.post(
            "/latest/item",
            json=item,
        ).json()
        == item
    )

    assert test_client.delete("/v1_1/item/1").status_code == 405
    assert test_client.delete("/v1_2/item/1").status_code == 200

    assert test_client.get("/v1_0/store/1").status_code == 200
    assert test_client.get("/v1_0/store/1").json()["status"] is True
    assert test_client.get("/v1_1/store/1").json()["status"] == "open"
    assert test_client.get("/v1_2/store/1").json()["status"] == "open"
    assert test_client.get("/v1_3/store/1").status_code == 404


def test_router_app() -> None:
    test_client = TestClient(router_app)
    assert test_client.get("/docs").status_code == 200
    assert test_client.get("/v1_0/docs").status_code == 200
    assert test_client.get("/v1_1/docs").status_code == 200
    assert test_client.get("/v1_3/docs").status_code == 404

    assert test_client.get("/v1_0/greet").json() == "Hello"
    assert test_client.get("/v1_1/greet").json() == "Hi"

    assert test_client.delete("/v1_0/greet").status_code == 405
    assert test_client.delete("/v1_1/greet").status_code == 200
    assert test_client.delete("/v1_1/greet").json() == "Goodbye"


def test_default_version() -> None:
    test_client = TestClient(default_version_app)
    assert test_client.get("/docs").status_code == 200
    assert test_client.get("/v1_0/docs").status_code == 404
    assert test_client.get("/v2_0/docs").status_code == 200
    assert test_client.get("/v3_0/docs").status_code == 200

    assert test_client.get("/v2_0/").json() == "Hello default version 2.0!"
    assert test_client.get("/v3_0/").json() == "Hello version 3.0!"


def test_websocket_support() -> None:
    with TestClient(ws_app) as test_client:
        assert test_client.get("/docs").status_code == 200
        assert test_client.get("/v1_0/docs").status_code == 200

        with pytest.raises(WebSocketDisconnect):
            test_client.websocket_connect("/ws")

        with test_client.websocket_connect("/v1_0/ws") as websocket:
            websocket.send_json({"msg": "Hello WebSocket"})
            data = websocket.receive_text()
            assert data == 'Message text was: {"msg": "Hello WebSocket"}'
            websocket.close()
