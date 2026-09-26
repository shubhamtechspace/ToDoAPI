from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings


database_url = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    database=settings.DB_NAME,
)


engine = create_engine(database_url)

Base = declarative_base()
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
