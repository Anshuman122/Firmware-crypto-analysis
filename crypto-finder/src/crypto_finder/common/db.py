# Hinglish: Yeh file SQLAlchemy ka use karke hamara database setup karti hai.
# Hum yahan tables ko Python classes ke roop me define karte hain (ise ORM kehte hain).

from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from crypto_finder.common.config import settings
from crypto_finder.common.logging import log

# Database engine banata hai. Yeh project ke liye main connection point hai.
# settings.database_url config file se aata hai.
try:
    engine = create_engine(
        settings.database_url,
        # SQLite ke liye yeh zaroori hai taaki single thread me hi access ho.
        connect_args={"check_same_thread": False}
    )
    log.info("Database engine successfully created.")
except Exception as e:
    log.error(f"Database engine create karne me error: {e}")
    raise

# SessionLocal ek factory hai jo naye database sessions banati hai.
# Har database operation (add, update, delete) ek session ke through hota hai.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class jisse hamare saare ORM models inherit karenge.
Base = declarative_base()


# --- Database Table Models ---

class Binary(Base):
    """'binaries' table ko represent karta hai."""
    __tablename__ = "binaries"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    filepath = Column(String, unique=True, nullable=False)
    filesize = Column(Integer)
    architecture = Column(String, nullable=True)

    # Ek binary ke multiple analysis results ho sakte hain.
    analysis_results = relationship("AnalysisResult", back_populates="binary")

class AnalysisResult(Base):
    """'analysis_results' table ko represent karta hai."""
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    binary_id = Column(Integer, ForeignKey("binaries.id"), nullable=False)
    analysis_type = Column(String, nullable=False) # e.g., "static_scan", "lifter_output"
    
    # JSON type ka use karke hum kisi bhi tarah ka result store kar sakte hain.
    result_data = Column(JSON, nullable=False)

    binary = relationship("Binary", back_populates="analysis_results")


def create_db_and_tables():
    """Database aur uske saare tables create karta hai agar woh exist nahi karte."""
    try:
        log.info("Database tables create ki ja rahi hain...")
        Base.metadata.create_all(bind=engine)
        log.success("Database tables successfully created.")
    except Exception as e:
        log.error(f"Database tables create karne me error: {e}")

# Jab yeh module import hota hai, hum database create kar sakte hain.
# create_db_and_tables()