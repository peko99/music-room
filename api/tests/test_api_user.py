# Copyright 2021 Group 21 @ PI (120)


import pytest
from typing import Dict, List
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient


_BASE_URL = '/user'


@pytest.fixture
def user_data():
    return [
        {"username": "example_user", "room_code": "NZVTKX"},
        {"username": "user_2", "room_code": "NZVTKX"},
        {"username": "user_3", "room_code": "NZVTKX"}
    ]


def test_create_user(client: TestClient, user_data: List[Dict]) -> None:
    client.post('/room', json={"host_id": 1, "code": "NZVTKX", "number_of_votes": 4, "guests_can_pause": True})
    created_response = client.post(f'{_BASE_URL}', json=user_data[0])
    assert created_response.status_code == 200
    created_user = created_response.json()

    assert created_user['username'] == user_data[0]['username']
    assert created_user['room_code'] == user_data[0]['room_code']


def test_get_all_users(client: TestClient, user_data: List[Dict]) -> None:
    client.post('/room', json={"host_id": 1, "code": "NZVTKX", "number_of_votes": 4, "guests_can_pause": True})
    first_created_response = client.post(f'{_BASE_URL}', json=user_data[0])
    assert first_created_response.status_code == 200
    first_created_user = first_created_response.json()
    second_created_response = client.post(f'{_BASE_URL}', json=user_data[1])
    assert second_created_response.status_code == 200
    second_created_user = second_created_response.json()
    third_created_response = client.post(f'{_BASE_URL}', json=user_data[2])
    assert third_created_response.status_code == 200
    third_created_user = third_created_response.json()

    stored_response = client.get(f'{_BASE_URL}')
    assert stored_response.status_code == 200
    stored_users = stored_response.json()

    assert stored_users[0] == first_created_user
    assert stored_users[1] == second_created_user
    assert stored_users[2] == third_created_user


def test_get_user_by_id(client: TestClient, user_data: List[Dict]) -> None:
    client.post('/room', json={"host_id": 1, "code": "NZVTKX", "number_of_votes": 4, "guests_can_pause": True})
    created_response = client.post(f'{_BASE_URL}', json=user_data[0])
    assert created_response.status_code == 200
    created_user = created_response.json()

    stored_user_response = client.get(f'{_BASE_URL}/id/{created_user["id"]}')
    assert stored_user_response.status_code == 200
    stored_user = stored_user_response.json()

    assert stored_user == created_user


def test_get_user_by_username(client: TestClient, user_data: List[Dict]) -> None:
    client.post('/room', json={"host_id": 1, "code": "NZVTKX", "number_of_votes": 4, "guests_can_pause": True})
    created_response = client.post(f'{_BASE_URL}', json=user_data[0])
    assert created_response.status_code == 200
    created_user = created_response.json()

    stored_user_response = client.get(f'{_BASE_URL}/username/{created_user["username"]}')
    assert stored_user_response.status_code == 200
    stored_user = stored_user_response.json()

    assert stored_user == created_user


def test_update_user(client: TestClient, user_data: List[Dict]) -> None:
    client.post('/room', json={"host_id": 1, "code": "NZVTKX", "number_of_votes": 4, "guests_can_pause": True})
    created_response = client.post(f'{_BASE_URL}', json=user_data[0])
    assert created_response.status_code == 200
    created_user = created_response.json()

    update_user_json = {"username": "user_3"}
    update_response = client.put(f'{_BASE_URL}/{created_user["id"]}', json=update_user_json)
    assert update_response.status_code == 200
    updated_user = update_response.json()

    assert updated_user['username'] == update_user_json['username']


def test_delete_user(client: TestClient, user_data: List[Dict]) -> None:
    client.post('/room', json={"host_id": 1, "code": "NZVTKX", "number_of_votes": 4, "guests_can_pause": True})   
    created_response = client.post(f'{_BASE_URL}', json=user_data[0])
    assert created_response.status_code == 200
    created_user = created_response.json()

    delete_user_response = client.delete(f'{_BASE_URL}/{created_user["id"]}')
    assert delete_user_response.status_code == 200
    deleted_user = delete_user_response.json()

    assert deleted_user == created_user

    fetch_user_response = client.get(f'{_BASE_URL}')
    assert fetch_user_response.status_code == 200
    assert fetch_user_response.json() == []


def test_user_join_room(client: TestClient) -> None:
    create_room_response = client.post('/room', json={"host_id": 1, "code": "NZVTKX", "number_of_votes": 4, "guests_can_pause": True})   
    create_user_response = client.post(f'{_BASE_URL}', json={"username": "example_user"})

    room = create_room_response.json()
    user = create_user_response.json()

    user_join_room_response = client.put(f'{_BASE_URL}/{user["id"]}/room-code/{room["code"]}')
    assert user_join_room_response.status_code == 200
    user_joined_room = user_join_room_response.json()

    assert user_joined_room['room_code'] == room['code']


def test_user_leave_room(client: TestClient, user_data: List[Dict]) -> None:
    client.post('/room', json={"host_id": 1, "code": "NZVTKX", "number_of_votes": 4, "guests_can_pause": True})
    created_response = client.post(f'{_BASE_URL}', json=user_data[0])
    user = created_response.json()

    user_leave_room_response = client.put(f'{_BASE_URL}/{user["id"]}/leave-room')
    assert user_leave_room_response.status_code == 200
    user_no_room = user_leave_room_response.json()

    assert user_no_room['room_code'] == None
