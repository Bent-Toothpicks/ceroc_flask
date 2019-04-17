from flask_table import Table, Col, BoolCol, ButtonCol, DateCol, LinkCol

class RegistrationTable(Table):
    classes = ["table", "table-bordered", "table-striped", "mb-0", "compact", "fixed-bottom"]
    first_name = Col('First Name')
    last_name = Col('Last Name')
    is_member = BoolCol("Is a Member", no_display='')  # Show nots as blank
    sale_type = Col('Entry Type ')
    pay_method = Col("Payment Method")
    payment = Col("Payment Amount")
    event_name = Col('event_name')

class EventsTable(Table):
    classes = ["table", "table-bordered", "table-striped", "mb-0", "compact", "fixed-bottom"]
    event_name = Col('Event Name')
    event_date = DateCol('Event Date')  # , date_format=(d, format='short', locale='en_AU'))
    event_type = Col("Event Type")
    edit_event = LinkCol('Edit', 'update_event', url_kwargs=dict(id='edit_event'))

class SalesTypes(Table):
    pass

class PersonTable(Table):
    pass