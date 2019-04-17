from datetime import datetime, timedelta
from app import db  # , login
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# by default auto increment is set on the db.Integer primary_key fields


class Person(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True, nullable=False)
    lastname = db.Column(db.String(64), index=True, nullable=False)
    full_name = firstname + ' ' + lastname  # Don't store merely for convienence
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    mobile = db.Column(db.String(12))
    ismember = db.Column(db.Boolean)
    gender = db.Column(db.String(6))
    address1 = db.Column(db.String(100))
    address2 = db.Column(db.String(100))
    suburb = db.Column(db.String(50))
    postcode = db.Column(db.String(6))
    accept_newsletter = db.Column(db.Boolean, default=True)
    accept_social_media = db.Column(db.Boolean, default=True)
    signed_disclaimer = db.Column(db.Boolean, default=True)
    attendance = db.relationship(
        'Attendance', backref='persons', lazy='dynamic')

    def __repr__(self):
        return '<Person: {}, {}>'.format(self.firstname, self.lastname)

    def get_full_name(self):    # Method to return full name
        return self.firstname + ' ' + self.lastname


class EventType(db.Model):
    _tablename = 'eventtype'
    event_type_id = db.Column(db.Integer, primary_key=True)
    event_type_name = db.Column(db.String(64), index=True, nullable=False)
        
    def __repr__(self):
        return '<EventType: {} {}>'.format(self.event_type_id, self.event_type_name)


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(64), index=True, nullable=False)
    event_date = db.Column(db.Date)
    event_type = db.Column(db.Integer, db.ForeignKey('event_type.event_type_id'))
    min_num = db.Column(db.Integer)
    max_num = db.Column(db.Integer)
    booking_required = db.Column(db.Boolean)
    attendees = db.relationship('Attendance', backref='attendees', lazy='dynamic')
    __current_event__ = None
    
    @classmethod
    def get_current_event(cls):
        if cls.__current_event__ is not None:
            return cls.__current_event__
        else:
            return db.session.query(Event).filter(Event.event_date >= (datetime.now() - timedelta(days=1))).order_by(Event.event_date).first()
    
    @classmethod
    def set_current_event(cls, eventid):
        cls.__current_event__ = db.session.query(Event).filter(Event.event_id == eventid).first()
        
    def __repr__(self):
        return '<Event: {}, {}>'.format(self.event_name, self.event_date)

class SalesType(db.Model):
    sales_type_id = db.Column(db.Integer, primary_key=True)
    sale_name = db.Column(db.String(64), index=True, nullable=False)
    member_only = db.Column(db.Boolean)
    end_date = db.Column(db.Date)
    default_price = db.Column(db.Numeric(precision=10, scale=2))     # Decimal
    # Only a default for the sales type
    fk_payment_type = db.Column(db.Integer, db.ForeignKey('pay_method.pay_method_id'))
    is_a_default = db.Column(db.Boolean)

    def __repr__(self):
        return '<SalesType: {}>'.format(self.sales_type_name, self.default_price)


class Attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)
    fk_person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    fk_event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    fk_sales_type_id = db.Column(db.Integer, db.ForeignKey('sales_type.sales_type_id'))
    fk_payment_type = db.Column(db.Integer, db.ForeignKey('pay_method.pay_method_id'))
    amount = db.Column(db.Numeric(precision=10, scale=2))     # Decimal

    def __repr__(self):
        return '<An Attendance object: {}>'.format(self.attendance_id)

class PayMethod(db.Model):
    pay_method_id = db.Column(db.Integer, primary_key=True)
    pay_method_name = db.Column(db.String(10))
