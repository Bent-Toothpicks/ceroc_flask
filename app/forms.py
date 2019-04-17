from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, DataRequired, ValidationError, Email, EqualTo, Length, AnyOf
from app.models import Person, Event, EventType, SalesType, PayMethod, Attendance
from datetime import datetime, timedelta
from sqlalchemy import and_, inspect
from app import app, db

class PersonForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(min=2, max=64)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=2, max=64)])
    gender = SelectField('Gender', choices=[('F', "Female"), ('M', "Male")], coerce=str)
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=2, max=120)])
    is_member = BooleanField('Is a member', validators=[], default=False)
    mobile = StringField('Mobile Phone', validators=[])
    address1 = StringField('Address Line 1', validators=[Length(max=100)])
    address2 = StringField('Address Line 2', validators=[Length(max=100)])
    suburb = StringField('Suburb', validators=[Length(max=50)])
    postcode = StringField('Postcode', validators=[Length(max=4)])
    accept_newsletter = BooleanField('Accepts email news leter?', default=True)
    accept_social_media = BooleanField('Accepts social media links?', default=True)
    has_signed_disclaimer = BooleanField('Has signed disclaimer?', validators=[InputRequired()], default=True)    
    submit = SubmitField('Add Person')
  
    def validate_email(self, email):
        user = Person.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Already have that email address. Please use a different email address.')


class EventForm(FlaskForm):
    event_name = StringField('Event name', validators=[InputRequired(), Length(min=0, max=140)]) 
    event_date = DateField('Event Date', validators=[InputRequired()])
    e_type = SelectField('Event type', coerce=int)
    min_num = IntegerField('Minium Numbers', default=1)
    max_num = IntegerField('Maximum numbers', default=999)
    booking_required = SelectField('Bookings required?', choices=[(1, 'Yes'), (2, 'No')], coerce=int, default=2)
    submit = SubmitField('Add Event')

    def __init__(self, event_id, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.event_id = event_id
        self.e_type.choices = [(event_type.event_type_id, event_type.event_type_name) for event_type in EventType.query.all()]

    def validate_event_date(self, eventdate):
        event = Event.query.filter_by(event_date=eventdate.data).all()

        if (len(event) > 1):  # This captures 1 or 0
            raise ValidationError('Currently can only have one event per date')


class SalesTypeForm(FlaskForm):
    sale_name = StringField('Entry Type', description='A short description of sales type', validators=[InputRequired(), Length(min=0, max=60)])
    member_only = SelectField('For Members Only?', choices=[(1, 'Yes'), (0, 'Everybody')], coerce=int)
    end_date = DateField('End date of this entry type')
    default_price = DecimalField('Default price', places=2)
    payment_type = SelectField('Payment type', choices=[(pm.pay_method_id, pm.pay_method_name) for pm in PayMethod.query.all()], coerce=int)
    is_a_default = SelectField('Should this be a default field', choices=[(1, 'Yes'), (0, 'No')], coerce=int)
    submit = SubmitField('Add Sales Type')


class RegistrationForm(FlaskForm):
    """ The Form to use to add people to the event on screen """
    person = StringField('Find a Person', id="person", validators=[InputRequired()])
    sales_types = SelectField('Select Entry Method', coerce=int, id="sales_type", validators=[InputRequired()])
    payment_method = SelectField('Enter Payment Method', coerce=int, id="pay_method", default=0)
    payment_amount = DecimalField('Enter Payment Amount', id="amount", default=0)
    submit = SubmitField('Register this Person')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
#        self.person.choices = [(person.person_id, person.firstname + ' ' + person.lastname) for person in Person.query.order_by(Person.firstname).all()] 
        self.sales_types.choices = [(st.sales_type_id, st.sale_name) for st in SalesType.query.filter_by(is_a_default=True).all()]
        self.payment_method.choices = [(pm.pay_method_id, pm.pay_method_name) for pm in PayMethod.query.all()]
        self.payment_amount.default = SalesType.query.filter_by(default_price=self.payment_method.data).first()
    
    def validate_payment_method(self, payment_method):
        if self.payment_method.data == 0:
            raise ValidationError('Please select a valid payment method')

    def validate_person(self, person):
        """
            Validate person is really used to validate that this person has not already been registed for this event
        """
        # Check to see if this person has already been registered for this event.
        person_id = Person.query.filter(Person.full_name == person.data).first().person_id
        event_id = Event.get_current_event().event_id
        already_registered = db.session.query(Attendance, Person, Event).join(Person).join(Event) \
            .filter(and_(Person.person_id == person_id, Event.event_id == event_id)).first()
        if already_registered is not None:
            app.logger.info("Person {} has already been registered for {}".format(person.data, Event.get_current_event().event_name))
            raise ValidationError("Person {} has already been registered for {}".format(person.data, Event.get_current_event().event_name))


class EventSelectForm(FlaskForm):
    """ Form to select and set the event that registrations refer to"""
    event = SelectField('Select the event', id='event_id', validators=[DataRequired()], coerce=int)

    def __init__(self, *args, **kwargs):
        super(EventSelectForm, self).__init__(*args, **kwargs)
        filter_date = datetime.now() - timedelta(days=1) 
        self.event.choices = [(e.event_id, e.event_name) for e in Event.query.filter(Event.event_date >= filter_date).all()]



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# 
# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired()])
#     email = StringField('Email', validators=[InputRequired(), Email()])
#     password = PasswordField('Password', validators=[InputRequired()])
#     password2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
#     submit = SubmitField('Register')
    
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different username.')
            
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different email address.')
            
#             