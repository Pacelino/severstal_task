import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


@pytest.fixture(scope="session")
def create_table():
    
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        def get_session_override():
            return session
    yield get_session_override
    
    SQLModel.metadata.drop_all(engine)
    
    
@pytest.fixture(scope="function", autouse=True)
def truncate_data(create_table):
    # Получаем сессию из фикстуры create_table
    session = create_table()
    
    # Чистим данные во всех таблицах
    for table in reversed(SQLModel.metadata.sorted_tables):
        session.execute(table.delete())
    
    session.commit()
    session.close()
    
# @pytest.fixture
# def client(session):
#     def get_session_override():
#         return session
    
#     app.dependency_overrides[get_session] = get_session_override
#     yield TestClient(app)
#     app.dependency_overrides.clear()