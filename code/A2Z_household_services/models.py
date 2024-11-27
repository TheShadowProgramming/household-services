from datetime import datetime, timezone;  # type: ignore
from sqlalchemy.orm import Mapped, mapped_column # type: ignore
from A2Z_household_services import db;
from flask_login import UserMixin; # type: ignore


class User(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(db.String(20), nullable=False)

    category: Mapped[str] = mapped_column(nullable=False)

    user_blocked: Mapped[bool] = mapped_column(nullable=False,default=False)

    email: Mapped[str] = mapped_column(db.String(120), nullable=False, unique=True)

    hashed_password: Mapped[str] = mapped_column(db.String(20), nullable=False)

    password: Mapped[str] = mapped_column(db.String(20), nullable=False)

    address: Mapped[str] = mapped_column(db.Text, nullable=False, default='Admin Address Anonymous Place')

    pincode: Mapped[int] = mapped_column(nullable=False, default=000000)

    date_joined: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), nullable=False)

    service_offered: Mapped[str] = mapped_column(nullable=False, default='Customer')

    description: Mapped[str] = mapped_column(db.Text, default='Household Customer Seeker')

    experience: Mapped[int] = mapped_column(nullable=False, default=0)

class ServiceTypes(db.Model):
    
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(db.String(20), nullable=False, unique=True)

    description: Mapped[str] = mapped_column(db.Text, nullable=False)

    base_price: Mapped[int] = mapped_column(nullable=False)