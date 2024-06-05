from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import or_, and_
from datetime import date, datetime
from uuid import uuid4
import os

# Dhmiourgia antikeimenou Flask
app = Flask(__name__)

# Orismos URI gia th syndesh me th vash dedomenwn, xrhsimopoiwntas th metablhth periballontos DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/customer')

# Apenergopoihsh parakolou8hshs allagwn sta antikeimena SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Orismos mystikou kleidiou gia ton sxhmatismo twn synedriwn
app.secret_key = os.urandom(24)

# Dhmiourgia antikeimenou SQLAlchemy gia th diaxeirish ths vashs dedomenwn
db = SQLAlchemy(app)

# Anaptyjhs metatrophs gia aytomatikh diaxeirish metatrophwn vashs dedomenwn
migrate = Migrate(app, db)

#klasi pelati
class Customer(db.Model):
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid4()))
    id_number = db.Column(db.String(8), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    addresses = db.relationship('Address', backref='customer', lazy=True)
    phone_numbers = db.relationship(
        'PhoneNumber', backref='customer', lazy=True)

#klasi Dieuthinsis
class Address(db.Model):
    customer_id = db.Column(db.String(36), db.ForeignKey(
        'customer.id'), primary_key=True)
    address = db.Column(db.String(200), nullable=False)

#klasi tilefwnwn
class PhoneNumber(db.Model):
    customer_id = db.Column(db.String(36), db.ForeignKey(
        'customer.id'), primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)


# Dimiourgia pinakwn sti vasi
with app.app_context():
    db.create_all()

#Vaidate synartiseis
def validate_id_number(id_number):
    if len(id_number) != 8:
        return False
    if not id_number[:2].isalpha() or not id_number[2:].isdigit():
        return False
    return True


def validate_name(name):
    return len(name) >= 3 and name[0].isupper() and name[1:].islower()


def validate_gender(gender):
    return gender.lower() in ['male', 'female']


def validate_birth_date(birth_date):
    try:
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        age = (date.today() - birth_date).days // 365
        return age >= 16
    except ValueError:
        return False


def validate_address(address):
    if not isinstance(address, str):
        return False
    words = address.split()
    if len(words) < 1:
        return False
    last_word = words[-1]
    if not last_word.isdigit() or len(last_word) > 3:
        return False
    return True


def validate_phone_number(phone_number):
    if not isinstance(phone_number, str):
        return False
    if not phone_number.isdigit() or len(phone_number) != 10:
        return False
    return True

#Enwsi me to Form
@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('form.html', customers=customers)

#Sybmit synartisi
@app.route('/submit-form', methods=['POST'])
def submit_form():
    id_number = request.form['id_number']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    birth_date = request.form['birth_date']
    addresses = request.form.getlist('addresses')
    phone_numbers = request.form.getlist('phone_numbers')

    errors = []

    # Epikurwsi dedomenwn eisagwgis
    if not id_number:
        errors.append('Παρακαλώ εισαγάγετε τον αριθμό ταυτότητας.')
    elif not validate_id_number(id_number):
        errors.append('Λανθασμένος αριθμός ταυτότητας')

    if not first_name:
        errors.append('Παρακαλώ εισαγάγετε το όνομα.')
    elif not validate_name(first_name):
        errors.append('Μη έγκυρο όνομα.')

    if not last_name:
        errors.append('Παρακαλώ εισαγάγετε το επώνυμο.')
    elif not validate_name(last_name):
        errors.append('Μη έγκυρο επώνυμο.')

    if not gender:
        errors.append('Παρακαλώ επιλέξτε το φύλο.')
    elif not validate_gender(gender):
        errors.append('Μη έγκυρο φύλο.')

    if not birth_date:
        errors.append('Παρακαλώ εισαγάγετε την ημερομηνία γέννησης.')
    elif not validate_birth_date(birth_date):
        errors.append('Μη έγκυρη ημερομηνία γέννησης.')

    if not addresses:
        errors.append('Παρακαλώ εισαγάγετε τουλάχιστον μία διεύθυνση.')
    else:
        for address in addresses:
            if not validate_address(address):
                errors.append(f'Μη έγκυρη διεύθυνση: {address}')

    if not phone_numbers:
        errors.append('Παρακαλώ εισαγάγετε τουλάχιστον έναν αριθμό τηλεφώνου.')
    else:
        for phone_number in phone_numbers:
            if not validate_phone_number(phone_number):
                errors.append(f'Μη έγκυρος αριθμός τηλεφώνου: {phone_number}')

    if errors:
        session['form_errors'] = errors
        return redirect(url_for('index'))
    else:
        # Elegxos an yparxei pelatis me idio AT
        existing_customer = Customer.query.filter_by(
            id_number=id_number).first()
        if existing_customer:
            error_message = 'Υπάρχει ήδη πελάτης με αυτό τον αριθμό ταυτότητας.'
            flash(error_message, 'error')
            return redirect(url_for('index'))
        else:
            new_customer = Customer(
                id_number=id_number,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birth_date=birth_date
            )
            db.session.add(new_customer)
            db.session.commit()

            for address in addresses:
                new_address = Address(
                    customer_id=new_customer.id, address=address)
                db.session.add(new_address)

            for phone_number in phone_numbers:
                new_phone_number = PhoneNumber(
                    customer_id=new_customer.id, phone_number=phone_number)
                db.session.add(new_phone_number)

            db.session.commit()
            flash('Επιτυχής προσθήκη πελάτη.', 'success')

    return redirect(url_for('index'))

#Synartisi diavasmatos pelati
@app.route('/read_customer', methods=['POST'])
def read_customer():
    customer_id = request.json.get('customer_id')

    if customer_id:
        customer = Customer.query.get(customer_id)
        if customer:
            customer_data = {
                'id': customer.id,
                'id_number': customer.id_number,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'gender': customer.gender,
                'birth_date': str(customer.birth_date),
                'entry_date': str(customer.entry_date),
                'addresses': [address.address for address in customer.addresses],
                'phone_numbers': [phone.phone_number for phone in customer.phone_numbers]
            }
            return jsonify(customer_data)
        else:
            return jsonify({'error': 'Customer not found'}), 404
    else:
        customers = Customer.query.all()
        all_customers_data = []
        for customer in customers:
            customer_data = {
                'id': customer.id,
                'id_number': customer.id_number,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'gender': customer.gender,
                'birth_date': str(customer.birth_date),
                'entry_date': str(customer.entry_date),
                'addresses': [address.address for address in customer.addresses],
                'phone_numbers': [phone.phone_number for phone in customer.phone_numbers]
            }
            all_customers_data.append(customer_data)
        return jsonify(all_customers_data)

#Synartisi anazitisis pelati
@app.route('/search_customer', methods=['POST'])
def search_customer():
    search_value = request.json.get('search_value')
    if search_value:
        customers = Customer.query.filter(
            or_(
                Customer.id_number.like(f'%{search_value}%'),
                Customer.first_name.like(f'%{search_value}%'),
                Customer.last_name.like(f'%{search_value}%'),
                Customer.gender.like(f'%{search_value}%')
            )
        ).order_by(
            Customer.last_name,
            Customer.first_name,
            Customer.id_number
        ).all()
        if customers:
            customers_data = []
            for customer in customers:
                customer_data = {
                    'id': customer.id,
                    'id_number': customer.id_number,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'gender': customer.gender,
                    'birth_date': str(customer.birth_date),
                    'entry_date': str(customer.entry_date),
                    'addresses': [address.address for address in customer.addresses],
                    'phone_numbers': [phone.phone_number for phone in customer.phone_numbers]
                }
                customers_data.append(customer_data)
            return jsonify(customers_data)
        else:
            # Epistrofi kenou pinaka an den yparxei apotelesma
            return jsonify([])
    else:
        return jsonify({'error': 'Δεν παρέχεται αναζήτηση'}), 400


# Synartisi gia update  customer
@app.route('/update-customer', methods=['POST'])
def update_customer():
    data = request.json
    customer_id = data.get('id')

    if customer_id:
        customer = Customer.query.get(customer_id)
        if customer:
            # Elegxos sta dedomena enimerwsis
            if 'id_number' in data and validate_id_number(data['id_number']):
                customer.id_number = data['id_number']
            if 'first_name' in data and validate_name(data['first_name']):
                customer.first_name = data['first_name']
            if 'last_name' in data and validate_name(data['last_name']):
                customer.last_name = data['last_name']
            if 'gender' in data and validate_gender(data['gender']):
                customer.gender = data['gender']
            if 'birth_date' in data and validate_birth_date(data['birth_date']):
                customer.birth_date = datetime.strptime(
                    data['birth_date'], '%Y-%m-%d').date()
            if 'addresses' in data and all(validate_address(address) for address in data['addresses']):
                for address in data['addresses']:
                    customer.addresses.append(Address(address=address))
            if 'phone_numbers' in data and all(validate_phone_number(phone) for phone in data['phone_numbers']):
                for phone in data['phone_numbers']:
                    customer.phone_numbers.append(
                        PhoneNumber(phone_number=phone))

            db.session.commit()
            return jsonify({'message': 'Επιτυχής ενημέρωση πελάτη'})
        else:
            return jsonify({'error': 'Ο πελάτης δε βρέθηκε'}), 404
    else:
        return jsonify({'error': 'Δεν παρέχεται αναγνωριστικό πελάτη'}), 400

#Synartisi diagrafis pelati
@app.route('/delete-customer', methods=['POST'])
def delete_customer_view():
    customer_id = request.json['customer_id']
    if not customer_id:
        return jsonify({'error': 'Ο πελάτης δεν βρέθηκε'}), 404

    with db.session() as session:
        customer = session.get(Customer, customer_id)
        if customer:
            # Diagrafi dieuthinsewn kai tilefwnwn
            Address.query.filter_by(customer_id=customer_id).delete()
            PhoneNumber.query.filter_by(customer_id=customer_id).delete()
            # Diagrafi Pelati
            session.delete(customer)
            session.commit()
            return jsonify({'message': 'Ο πελάτης διαγράφηκε με επιτυχία'})
        else:
            return jsonify({'error': 'Ο πελάτης δεν βρέθηκε'}), 404

#Main synartisi
if __name__ == '__main__':
    app.app_context().push()
    # Orismos mystikou kleidiou gia ton sxhmatismo twn synedriwn
    app.secret_key = 'your_secret_key_here'
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=4000)
