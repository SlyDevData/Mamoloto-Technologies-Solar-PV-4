from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# ---------- EMAIL CONFIGURATION ----------
# IMPORTANT: To send real emails, replace the placeholders below with your SMTP details.
# If you use Gmail, you need an App Password (not your regular password).
# If you leave this as is, the form will still print the message in the terminal.

SMTP_SERVER = "smtp.gmail.com"        # For Gmail. For Outlook: "smtp.office365.com"
SMTP_PORT = 587                       # 587 for TLS
SENDER_EMAIL = "slycorporate@gmail.com" # Replace with your sending email
SENDER_PASSWORD = "Smtla9302" # Replace with your App Password / SMTP password
RECEIVER_EMAIL = "slycorporate@gmail.com" # Where the form emails go

def send_email_alert(name, email, phone, subject, message):
    """Send an email notification to the company."""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"New Contact Form: {subject if subject else 'Inquiry'}"

        body = f"""
        New message from the Mamoloto Technologies website:

        Name: {name}
        Email: {email}
        Phone: {phone if phone else 'Not provided'}
        Subject: {subject if subject else 'General Inquiry'}

        Message:
        {message}

        ---
        This email was sent automatically via the website contact form.
        """
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server and send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        # If email fails (e.g., missing credentials), fallback to console log
        print(f"=== CONTACT FORM SUBMISSION (Email failed: {e}) ===")
        print(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\nMessage: {message}")
        return False


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Try to send the email
        sent = send_email_alert(name, email, phone, subject, message)
        
        # You can check `sent` to show a specific success/failure message if you want
        return render_template('contact.html', success=True)

    return render_template('contact.html', success=False)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)