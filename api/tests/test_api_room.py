# Copyright 2021 Group 21 @ PI (120)


import pytest
from typing import Dict, List
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient


_BASE_URL = '/room'


@pytest.fixture
def room_data():
    return [
        {"host_id": 1, "code": "NZVTKX", "number_of_votes": 4, "guests_can_pause": True},
        {"host_id": 2, "code": "JA7Y91", "number_of_votes": 5, "guests_can_pause": False},
        {"host_id": 3, "code": "0EQMJL", "number_of_votes": 6, "guests_can_pause": True}
    ]


def test_create_room(client: TestClient, room_data: List[Dict]) -> None:
    created_response = client.post(f'{_BASE_URL}', json=room_data[0])
    assert created_response.status_code == 200
    created_room = created_response.json()

    assert created_room['host_id'] == room_data[0]['host_id']
    assert created_room['number_of_votes'] == room_data[0]['number_of_votes']
    assert created_room['guests_can_pause'] == room_data[0]['guests_can_pause']


def test_get_all_rooms(client: TestClient, room_data: List[Dict]) -> None:
    first_created_response = client.post(f'{_BASE_URL}', json=room_data[0])
    assert first_created_response.status_code == 200
    first_created_room = first_created_response.json()
    second_created_response = client.post(f'{_BASE_URL}', json=room_data[1])
    assert second_created_response.status_code == 200
    second_created_room = second_created_response.json()
    third_created_response = client.post(f'{_BASE_URL}', json=room_data[2])
    assert third_created_response.status_code == 200
    third_created_room = third_created_response.json()

    stored_response = client.get(f'{_BASE_URL}')
    assert stored_response.status_code == 200
    stored_rooms = stored_response.json()

    assert stored_rooms[0] == first_created_room
    assert stored_rooms[1] == second_created_room
    assert stored_rooms[2] == third_created_room


def test_get_room_by_code(client: TestClient, room_data: List[Dict]) -> None:
    created_response = client.post(f'{_BASE_URL}', json=room_data[0])
    assert created_response.status_code == 200
    created_room = created_response.json()

    stored_room_response = client.get(f'{_BASE_URL}/code/{created_room["code"]}')
    assert stored_room_response.status_code == 200
    stored_room = stored_room_response.json()

    assert stored_room == created_room


def test_get_room_by_host_id(client: TestClient, room_data: List[Dict]) -> None:
    created_response = client.post(f'{_BASE_URL}', json=room_data[0])
    assert created_response.status_code == 200
    created_room = created_response.json()

    stored_room_response = client.get(f'{_BASE_URL}/host-id/{created_room["host_id"]}')
    assert stored_room_response.status_code == 200
    stored_room = stored_room_response.json()

    assert stored_room == created_room


def test_update_room(client: TestClient, room_data: List[Dict]) -> None:
    created_response = client.post(f'{_BASE_URL}', json=room_data[0])
    assert created_response.status_code == 200
    created_room = created_response.json()

    update_room_json = {"host_id": 2, "code": "0EQMJL", "number_of_votes": 5, "guests_can_pause": False}
    update_response = client.put(f'{_BASE_URL}/{created_room["code"]}', json=update_room_json)
    assert update_response.status_code == 200
    updated_room = update_response.json()

    assert updated_room == update_room_json


def test_delete_room(client: TestClient, room_data: List[Dict]) -> None:
    created_response = client.post(f'{_BASE_URL}', json=room_data[0])
    assert created_response.status_code == 200
    created_room = created_response.json()

    delete_room_response = client.delete(f'{_BASE_URL}/{created_room["code"]}')
    assert delete_room_response.status_code == 200
    deleted_room = delete_room_response.json()

    assert deleted_room == created_room

    fetch_room_response = client.get(f'{_BASE_URL}')
    assert fetch_room_response.status_code == 200
    assert fetch_room_response.json() == []
