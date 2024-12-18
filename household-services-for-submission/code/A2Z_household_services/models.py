from datetime import datetime, timezone;  # type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship # type: ignore
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

class Service_requests_central(db.Model):

    service_id: Mapped['int'] = mapped_column(primary_key=True); # auto-generated
    
    service_category: Mapped['str'] = mapped_column(db.String(30),nullable=False); # will be decided by the professional at the time of making their professional portfolio

    service_price: Mapped['int'] = mapped_column(nullable=False); # will be decided by the professional at the time of making their professional portfolio

    service_status: Mapped['str'] = mapped_column(db.String(20), nullable=False); # both customers and professionals can change this

    customer_id: Mapped['int'] = mapped_column(db.ForeignKey('service_requests_customer.customer_id'), nullable=False);
    # single customer asking for single service

    professional_id: Mapped['int'] = mapped_column(db.ForeignKey('service_requests_professional.professional_id'), nullable=False);
    # single professional a single service to a single customer

    customer_pincode: Mapped['int'] = mapped_column(nullable=False);

    professional_pincode: Mapped['int'] = mapped_column(nullable=False);

    service_review: Mapped['str'] = mapped_column(db.Text, nullable=False);
    # will be added by the customer at the time of closing the service

class Service_requests_customer(db.Model):
    customer_id: Mapped['int'] = mapped_column(primary_key=True);

    services_requested: Mapped[list['Service_requests_central']] = relationship(lazy=True);

class Service_requests_professional(db.Model):

    professional_id: Mapped['int'] = mapped_column(primary_key=True);

    services_served: Mapped[list['Service_requests_central']] = relationship(lazy=True);

class Professional_portfolio(db.Model):

    professional_id: Mapped['int'] = mapped_column(primary_key=True);

    professional_portfolio: Mapped['str'] = mapped_column(db.Text, nullable=False);