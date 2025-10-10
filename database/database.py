# cf4/database/database.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date

# Important: We are importing the classes and the SessionLocal from the models.py file
# The '.' before 'models' is crucial because it tells Python to look in the same directory.
from .models import Room, Booking, Customer, SessionLocal, CallSession, ConversationTurn

def get_db():
    """
    This function creates a new database session for each request
    and ensures it's closed afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_available_rooms(db: Session, check_in_date: date, check_out_date: date, num_guests: int):
    """
    Finds rooms that are not booked for the given dates and can accommodate the number of guests.
    """
    # First, find all room IDs that are booked during the requested period.
    # A room is considered booked if its booking period overlaps with the requested dates.
    booked_room_ids = db.query(Booking.room_id).filter(
        and_(
            Booking.check_out_date > check_in_date,
            Booking.check_in_date < check_out_date
        )
    ).all()

    # The result is a list of tuples, so we extract the first element of each tuple.
    booked_room_ids = [r_id for r_id, in booked_room_ids]

    # Now, find all rooms that are NOT in the booked list and have enough capacity.
    available_rooms = db.query(Room).filter(
        and_(
            Room.id.notin_(booked_room_ids),
            Room.capacity >= num_guests
        )
    ).all()

    return available_rooms

def create_booking(db: Session, customer_name: str, phone_number: str, room_id: int, check_in_date: date, check_out_date: date, num_guests: int):
    """
    Creates a booking record in the database.
    It first finds or creates a customer based on the phone number.
    """
    # Check if a customer with this phone number already exists.
    customer = db.query(Customer).filter(Customer.phone_number == phone_number).first()
    if not customer:
        # If not, create a new customer.
        customer = Customer(name=customer_name, phone_number=phone_number)
        db.add(customer)
        db.commit()
        db.refresh(customer) # Refresh to get the new customer's ID

    # Create the new booking record.
    booking = Booking(
        customer_id=customer.id,
        room_id=room_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        number_of_guests=num_guests
    )
    db.add(booking)
    db.commit()
    db.refresh(booking) # Refresh to get the new booking's ID
    return booking

def get_room_by_number(db: Session, room_number: str):
    """A helper function to find a room by its number."""
    return db.query(Room).filter(Room.room_number == room_number).first()

from .models import CallSession, ConversationTurn, Customer # Add to your imports

def create_call_session(db: Session, customer_phone: str = None) -> CallSession:
    """Creates a new record for a call session."""
    session = CallSession(customer_phone=customer_phone)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def log_conversation_turn(db: Session, session_id: int, speaker: str, text: str):
    """Logs a single turn of the conversation."""
    turn = ConversationTurn(session_id=session_id, speaker=speaker, text=text)
    db.add(turn)
    db.commit()

def get_conversation_history(db: Session, session_id: int):
    """Retrieves all turns for a given session ID."""
    return db.query(ConversationTurn).filter(ConversationTurn.session_id == session_id).order_by(ConversationTurn.timestamp).all()

def find_customer_by_phone(db: Session, phone_number: str):
    """Finds a customer by their phone number."""
    return db.query(Customer).filter(Customer.phone_number == phone_number).first()