from app.utilities.decorators import auth_required
from app.utilities.helper import create_jwt_token, decode_token, hash_password, is_valid_token, validate_token_expiry, verify_password
import pytest
import json
from json import JSONEncoder




def test_token():
    data = {"email":"ashu123@gmail.com", "is_verified":True,"role":"admin"}
    expire_time = 50
    token = create_jwt_token(data, expire_time)

    print(f"******************{token}*********************")
    print("token created")

    returned_data = decode_token(token)


    print(f"******************{returned_data}*********************")
    print("token decoded")

    assert not decode_token(token+"1")

    assert returned_data["email"] == data["email"]

    assert data["is_verified"] == returned_data["is_verified"]

    assert data["role"] == returned_data["role"]


def test_password_hashing():
    password = "9410197255"

    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password)

    assert not verify_password(password + "1", hashed_password)


def test_is_valid_token():

    data = {"email":"ashu123@gmail.com", "is_verified":True,"role":"admin"}
    expire_time = 50
    token = create_jwt_token(data, expire_time)

    print(f"******************{token}*********************")
    print("token created")

    retured_data = is_valid_token(token)

    assert retured_data["valid_token"]

    assert retured_data["email"] == data["email"]

    assert data["is_verified"] == retured_data["is_verified"]

    assert data["role"] == retured_data["role"]


def test_validate_token_expiry():
    data = {"email":"ashu123@gmail.com", "is_verified":True,"role":"admin"}
    expire_time = 50
    token = create_jwt_token(data, expire_time)

    print(f"******************{token}*********************")
    print("token created")
    decoded_data = decode_token(token)

    expire_at = json.loads(decoded_data["expire_at"])["to_encode"]

    assert validate_token_expiry(expire_at)




