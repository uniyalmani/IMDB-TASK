
import pytest
import os
import sqlalchemy
from sqlmodel import Session, create_engine as sqlmodel_engine, SQLModel
from app.models import database_models
from sqlalchemy import create_engine
print(os.getcwd(), "hhfhehfkkdfkkkdfk", os.listdir())
import os



@pytest.fixture
def database_session():
    mysql_host_test = os.environ.get("MYSQL_ROOT_HOST", "172.17.0.5")

    mysql_root_password = os.environ.get("MYSQL_ROOT_PASSWORD", "")

    mysql_port_test = 3306

    mysql_username = os.environ.get("MYSQL_USER", "root2")

    mysql_password = os.environ.get("MYSQL_PASSWORD", "pass123")
    print(os.environ.get("MYSQL_USER"), mysql_host_test, mysql_root_password)

    mysql_test_database = os.environ.get("MYSQL_TEST_DATABASE", "imbd_test")



    TESTURL = f"mysql://{mysql_username}:{mysql_password}@{mysql_host_test}:{mysql_port_test}"


    engine = sqlalchemy.create_engine(TESTURL).connect()


    engine.execute(f"DROP DATABASE IF EXISTS {mysql_test_database}")
 
    engine.execute(f"CREATE DATABASE {mysql_test_database}")


    engine.close()

    TESTURL = f"mysql://{mysql_username}:{mysql_password}@{mysql_host_test}:{mysql_port_test}/{mysql_test_database}"

    engine = sqlmodel_engine(TESTURL, echo = True)


    SQLModel.metadata.create_all(engine)

    
    session = Session(engine)

    yield session

    session.close()

    print("database operation completed")




