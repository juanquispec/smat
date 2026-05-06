from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definimos la URL de SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./smat.db"

# 2. Creamos el motor
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Clase base
Base = declarative_base()

# 5. Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()