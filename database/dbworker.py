from typing import Optional

from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, User


def create_db_engine() -> Engine:
    engine = create_engine('sqlite+pysqlite:///database/database.db')
    Base.metadata.create_all(engine)

    return engine


def create_session(engine: Engine) -> Session:
    Session = sessionmaker(bind=engine)
    return Session()


def get_user(user_id: Optional[int], engine: Engine) -> User:
    session = create_session(engine)
    user = []
    try:
        if user_id != None:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return None

        session.expunge(user)
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return user


def add_user(userdata: list, engine: Engine) -> User:
    session = create_session(engine)
    try:
        user = User(
            id=userdata[0],
            psw_hash=userdata[1],
            pred_count=0,
            is_admin=0 if userdata[0] != 625438726 else 1
        )

        session.add(user)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def get_all_users(engine: Engine) -> list[User]:
    session = create_session(engine)
    users = []
    try:
        all_users = session.execute(select(User).order_by(User.id)).all()
        for user in all_users:
            users += user
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return users


def delete_user(user_id: int, engine: Engine) -> None:
    session = create_session(engine)
    try:
        if user_id != None:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return None

        session.delete(user)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def add_adm_user(user_id: int, engine: Engine) -> None:
    session = create_session(engine)
    try:
        if user_id != None:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return None

        user.is_admin = 1
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def add_user_pred(user_id: int, engine: Engine) -> None:
    session = create_session(engine)
    try:
        if user_id != None:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return None

        user.pred_count += 1
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()