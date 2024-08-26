import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from database.engine import connect_with_connector
from typing import Optional

from utils.exceptions import NOT_FOUND_USER_EXCEPTION

db_name = os.environ["USERS_DATABASE_NAME"]

async def get_all_users():
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(text("SELECT * FROM profile"))
        rows = result.fetchall()

        users = []
        for row in rows:
            row_dict = {column: value for column, value in zip(result.keys(), row)}
            users.append(row_dict)

        return users
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def get_user_by_username(username: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(
            text("SELECT * FROM profile WHERE username = :username"),
            {"username": username}
        )

        row = result.fetchone()

        if row is None:
            raise NOT_FOUND_USER_EXCEPTION

        return {column: value for column, value in zip(result.keys(), row)}
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def update_user_status(username: str, disabled: bool):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(
            text("UPDATE profile SET disabled = :disabled WHERE username = :username"),
            {"username": username, "disabled": disabled}
        )

        session.commit()

        if result.rowcount == 0:
            raise NOT_FOUND_USER_EXCEPTION

        return {"username": username, "disabled": disabled}
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def update_user_role(username: str, role: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(
            text("UPDATE profile SET role = :role WHERE username = :username"),
            {"username": username, "role": role}
        )

        session.commit()

        if result.rowcount == 0:
            raise NOT_FOUND_USER_EXCEPTION

        return {"username": username, "role": role}
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def update_user(username: str, new_hashed_password: str, email: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        update_data = {
            "username": username,
            "new_hashed_password": new_hashed_password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }

        result = session.execute(
            text(
                "UPDATE profile SET hashed_password = :new_hashed_password, email = :email, first_name = :first_name, last_name = :last_name WHERE username = :username"
            ),
            update_data
        )

        session.commit()

        if result.rowcount == 0:
            raise NOT_FOUND_USER_EXCEPTION

        return {"username": username, "email": email, "first_name": first_name, "last_name": last_name}
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def user_already_exists(username: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(
            text("SELECT * FROM profile WHERE username = :username"),
            {"username": username}
        )

        return result.fetchone() is not None
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def create_user(username: str, hashed_password: str, email: Optional[str] = None, role: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, disabled: Optional[bool] = None):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.execute(
            text(
                "INSERT INTO profile (username, hashed_password, email, role, first_name, last_name, disabled) VALUES (:username, :hashed_password, :email, :role, :first_name, :last_name, :disabled)"
            ),
            {"username": username, "hashed_password": hashed_password, "email": email, "role": role, "first_name": first_name, "last_name": last_name, "disabled": disabled}
        )

        session.commit()

        return {"username": username, "email": email, "role": role, "first_name": first_name, "last_name": last_name, "disabled": disabled}
    except Exception as exception:
        raise exception
    finally:
        session.close()
