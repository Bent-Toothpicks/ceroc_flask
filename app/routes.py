from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.models import Person, Event, SalesType, Attendance, EventType, PayMethod
from app.forms import LoginForm, PersonForm, EventForm, SalesTypeForm, EventSelectForm, RegistrationForm   # EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.tables import RegistrationTable, EventsTable

event = None

@app.route('/dummyroute')
def dummyroute():  # A place holder to do nothing
    return render_template('base.html', title='Ceroc Management System')

@app.route('/')
@app.route('/index')
# @login_required
def index():
    app.logger.info("Route /index called")
    return render_template('index.html', title='Ceroc Management System')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    app.logger.info("Route /registration called")
    form = RegistrationForm()
    event = Event.get_current_event()
    evtform = EventSelectForm()
    if form.validate_on_submit():
        flash('{} has been registered {}'.format(form.person.data, Event.query.filter_by(event_id=event.event_id).first().event_name))
        attendee = Attendance(fk_person_id=Person.query.filter_by(full_name=form.person.data).first().person_id,
                              fk_event_id=event.event_id,  # form.event.data,
                              fk_sales_type_id=form.sales_types.data,
                              fk_payment_type=form.payment_method.data,
                              amount=form.payment_amount.data)
        db.session.add(attendee)
        db.session.commit()
    rt = None
    if event is not None: 
        atts = get_attendees(event.event_id)
        rt = RegistrationTable(atts, table_id="regotable")
    return render_template('registration.html', title='Home', form=form, evtform=evtform, table=rt)


@app.route('/person', methods=['GET', 'POST'])
def add_person():
    app.logger.info("Route /person called - Adding a new person")
    form = PersonForm()
    if form.validate_on_submit():
        flash('{} {} has been added to the database'.format(form.first_name.data, form.last_name.data))
        app.logger.info("New person {} {} added to database".format(form.first_name.data, form.last_name.data))
        person = Person(firstname=form.first_name.data,
                        lastname=form.last_name.data,
                        email=form.email.data,
                        mobile=form.mobile.data,
                        ismember=form.is_member.data,
                        gender=form.gender.data,
                        address1=form.address1.data,
                        address2=form.address2.data,
                        suburb=form.suburb.data,
                        postcode=form.postcode.data,
                        accept_newsletter=form.accept_newsletter.data,
                        accept_social_media=form.accept_social_media.data,
                        signed_disclaimer=form.has_signed_disclaimer.data)
        db.session.add(person)
        db.session.commit()
    return render_template('add_person.html', title='Add Person', form=form, pagetitle='Add Person')


@app.route('/event', methods=["GET", "POST"])
def add_event():
    app.logger.info("Route /event called - Adding a new event")
    form = EventForm(None)
    if form.validate_on_submit():
        flash('{} on {} was added to the database'.format(form.event_name.data, form.event_date.data))
        app.logger.info('Event {} on date {} added to the database'.format(form.event_name.data, form.event_date.data))
        event = Event(event_name=form.event_name.data,
                      event_date=form.event_date.data,
                      event_type=form.e_type.data)
        db.session.add(event)
        db.session.commit()
    # Always include the events table
    rt = EventsTable(get_events(), table_id="eventstable")
    return render_template('event.html', title='Manage Events', form=form, table=rt, pagetitle='Manage Events')

@app.route('/new_sales_type', methods=['GET', 'POST'])
def add_salestype():
    app.logger.info('Route /new_sales_type called')
    form = SalesTypeForm()
    if form.validate_on_submit():
        flash('New Sales type {} with default price of {} added {}'.format(form.sale_name.data, form.default_price.data, datetime.now()))
        app.logger.info('New Sales type {} with default price of {} added {}'.format(form.sale_name.data, form.default_price.data, datetime.now()))
        sales_type = SalesType(sale_name=form.sale_name.data,
                               fk_payment_type=form.payment_type.data,
                               end_date=form.end_date.data,
                               default_price=form.default_price.data,
                               member_only=form.member_only.data,
                               is_a_default=form.is_a_default.data)
        db.session.add(sales_type)
        db.session.commit()
    return render_template('add_salestype.html', title='Add Sales Type', form=form, pagetitle='Add Sales Type')


@app.route('/person/<email>')
def edit_person(email):
    print (email)
    person = Person.query.filter_by(email=email).first()
    if person is not None:
        print (person.firstname + person.lastname)
    return redirect(url_for('registration'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # app.logger.info("Route /login called")
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     next_page = request.args.get('next')
    #     if not next_page or url_parse(next_page).netloc != '':
    #         next_page = url_for('index')
    #     return redirect(next_page)
    # flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
    # return render_template('login.html', title='Sign In', form=form)
    return render_template('index.html')


# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now registered!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
# @login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


"""
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
"""


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/update_event/<int:id>', methods=['GET', 'POST'])
def update_event(id):
    form = EventForm(id)
    event = Event.query.filter(Event.event_id == id).first_or_404()
    if form.validate_on_submit():
        flash('{} on {} was amended in  the database'.format(form.event_name.data, form.event_date.data))
        app.logger.info('Event {} on date {} amended'.format(form.event_name.data, form.event_date.data))
        event.event_name = form.event_name.data
        event.event_date = form.event_date.data
        event.event_type = form.e_type.data
#        db.session.merge(event)
        db.session.commit()
    elif request.method == 'GET':
        form.event_name.data = event.event_name
        form.event_date.data = event.event_date
        form.e_type.data = event.event_type
    return render_template('event.html', title='Event', form=form)

def get_attendees(event_id):
    attendees = db.session.query(Attendance, Person, Event, SalesType, PayMethod).join(Person).join(Event) \
        .join(SalesType).join(PayMethod).filter(Event.event_id == event_id)
    results = []
    for (a, p, e, st, pm) in attendees:
        results.append(dict(first_name=p.firstname,
                            last_name=p.lastname,
                            is_member=p.ismember,
                            sale_type=st.sale_name,
                            pay_method=pm.pay_method_name,
                            payment=a.amount,
                            event_name=e.event_name,
                            ))
    return results

def get_events():
    events = db.session.query(Event, EventType).join(EventType).order_by(Event.event_date)
    results = []
    for (e, et) in events:
        results.append(dict(event_name=e.event_name,
                            event_date=e.event_date,
                            event_type=et.event_type_name,
                            edit_event=e.event_id))
    return results

@app.route('/personcomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = Person.query.filter(Person.full_name.contains(str(search))).order_by(Person.full_name).all()
    results = [(person.person_id, person.firstname + ' ' + person.lastname) for person in query]
    result_dict = dict(results)      # Covert to dict and use person_id as keywords for names
    return jsonify(matching_results=result_dict)

@app.route('/event_data', methods=['GET'])
def event_change():
    global event
    if request.method == 'GET':
        search = request.args.get('q')
        event = Event.query.filter(Event.event_id == search).first()
        Event.set_current_event(event.event_id)
    pass
    #     rt = None
    #     if event is not None: 
    #         atts = get_attendees(event.event_id)
    #         rt = RegistrationTable(atts, table_id="resultstable")
    #     return render_template('registration.html', title='Home', table=rt)
    # return redirect(url_for('registration'))
