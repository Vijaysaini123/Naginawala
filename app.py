from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText


from flask import Flask, request, jsonify, send_from_directory
import random
import time



app = Flask(__name__)

@app.route('/contactform', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Compose the email
        body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage:\n{message}"
        msg = MIMEText(body)
        msg['Subject'] = f"Contact Form: {subject}"
        msg['From'] = "rimjhim15151@gmail.com"  # Sender
        msg['To'] = "engineer.vijaysaini@gmail.com"  # Recipient

        # Send the email using Gmail SMTP (requires App Password)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login("rimjhim15151@gmail.com", "fnqkfybpxtxqcvmt")
                server.sendmail(msg['From'], [msg['To']], msg.as_string())
            return render_template('contact.html', success=True)
        except Exception as e:
            return render_template('contact.html', error=str(e))
    return render_template('contact.html')


# In-memory stores for demo
otp_store = {}  # contact: (otp, expiry_time)
user_history = {
    "9876543210": ["Order #1234", "Order #5678", "Support Ticket #4321"],
    "9123456789": ["Order #1111", "Support Ticket #2222"]
}

@app.route('/')
def index():
    return send_from_directory('.', 'login.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    contact = data.get('contact')
    if not contact or not contact.isdigit() or len(contact) != 10:
        return jsonify(success=False, message="Invalid contact number."), 400

    otp = str(random.randint(100000, 999999))
    expiry = time.time() + 300  # OTP valid for 5 minutes
    otp_store[contact] = (otp, expiry)

    # In production, send OTP via SMS gateway here.
    print(f"DEBUG: OTP for {contact} is {otp}")

    return jsonify(success=True)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    contact = data.get('contact')
    otp = data.get('otp')
    stored = otp_store.get(contact)
    if not stored:
        return jsonify(success=False, message="OTP not sent or expired."), 400
    real_otp, expiry = stored
    if time.time() > expiry:
        otp_store.pop(contact, None)
        return jsonify(success=False, message="OTP expired."), 400
    if otp != real_otp:
        return jsonify(success=False, message="Incorrect OTP."), 400

    # OTP verified, fetch user history
    history = user_history.get(contact, [])
    otp_store.pop(contact, None)  # Remove OTP after successful login
    return jsonify(success=True, history=history)

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)



if __name__ == '__main__':
    app.run(debug=True)
