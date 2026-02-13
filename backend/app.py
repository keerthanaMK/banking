from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from fpdf import FPDF

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
db = SQLAlchemy(app)

class FixedDeposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tenure = db.Column(db.Integer, nullable=False)  # in months
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    interest_rate = db.Column(db.Float, default=5.0)  # Default 5%

    def calculate_maturity(self):
        total_amount = self.amount * (1 + (self.interest_rate / 100) * (self.tenure / 12))
        return total_amount

    def generate_receipt(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, 'Fixed Deposit Receipt', ln=True, align='C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(200, 10, f'Name: {self.name}', ln=True)
        pdf.cell(200, 10, f'Amount: {self.amount}', ln=True)
        pdf.cell(200, 10, f'Tenure: {self.tenure} months', ln=True)
        pdf.cell(200, 10, f'Start Date: {self.start_date.strftime("%Y-%m-%d")}', ln=True)
        pdf.cell(200, 10, f'Interest Rate: {self.interest_rate}%', ln=True)
        pdf.cell(200, 10, f'Maturity Amount: {self.calculate_maturity()}', ln=True)
        pdf.output(f'{self.name}_FD_receipt.pdf')

@app.route('/fd/create', methods=['POST'])
def create_fd():
    data = request.json
    new_fd = FixedDeposit(
        name=data['name'],
        amount=data['amount'],
        tenure=data['tenure'],
        interest_rate=data.get('interest_rate', 5.0)
    )
    db.session.add(new_fd)
    db.session.commit()
    return jsonify({'message': 'Fixed Deposit created', 'id': new_fd.id}), 201

@app.route('/fd/list', methods=['GET'])
def list_fds():
    fds = FixedDeposit.query.all()
    return jsonify([{'id': fd.id, 'name': fd.name, 'amount': fd.amount, 'tenure': fd.tenure, 'start_date': fd.start_date.strftime('%Y-%m-%d'), 'interest_rate': fd.interest_rate} for fd in fds])

@app.route('/fd/premature_closure/<int:fd_id>', methods=['POST'])
def premature_closure(fd_id):
    fd = FixedDeposit.query.get_or_404(fd_id)
    time_passed = datetime.utcnow() - fd.start_date
    if time_passed.days < (fd.tenure * 30):  # Less than tenure
        penalty_rate = 1.0  # 1% penalty
        maturity_amount = fd.calculate_maturity() * (1 - penalty_rate / 100)
    else:
        maturity_amount = fd.calculate_maturity()
    return jsonify({'maturity_amount': maturity_amount}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)