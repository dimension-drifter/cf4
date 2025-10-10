# cf4/database/models.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# --- All your table classes (Customer, Room, Booking, etc.) go here ---
# (The following classes are unchanged)
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String, unique=True, nullable=False)
    bookings = relationship("Booking", back_populates="customer")

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True, nullable=False)
    room_type = Column(String)
    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    bookings = relationship("Booking", back_populates="room")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    call_session_id = Column(Integer, ForeignKey('call_sessions.id'))
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    customer = relationship("Customer", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")

class CallSession(Base):
    __tablename__ = 'call_sessions'
    id = Column(Integer, primary_key=True)
    customer_phone = Column(String, nullable=True)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    turns = relationship("ConversationTurn", back_populates="session")

class ConversationTurn(Base):
    __tablename__ = 'conversation_turns'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('call_sessions.id'), nullable=False)
    speaker = Column(String)
    text = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    session = relationship("CallSession", back_populates="turns")

# --- NEW AND IMPROVED DATABASE CONNECTION ---

# Get the absolute path to the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path for the database file within that directory
db_path = os.path.join(BASE_DIR, "hotel_agent.db")

# The new, robust DATABASE_URL
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Creates all the tables in the database."""
    print(f"Initializing database at: {db_path}")
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()