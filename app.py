from flask import Flask, render_template, request, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# ---------- EMAIL CONFIG ----------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "mamoloto@tlabela.com"   
SENDER_PASSWORD = "your-app-password"   # Replace with actual password
RECEIVER_EMAIL = "mamoloto@tlabela.com"

def send_email_alert(name, email, phone, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"New Contact: {subject if subject else 'Inquiry'}"

        body = f"""
        New message from Mamoloto Technologies website:

        Name: {name}
        Email: {email}
        Phone: {phone if phone else 'Not provided'}
        Subject: {subject if subject else 'General'}

        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Form submission (email failed): {e}")
        print(f"Name: {name}, Email: {email}, Message: {message}")
        return False

# ---------- ROUTES ----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ----- NEW PAGES -----
@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/knowledge')
def knowledge():
    return render_template('knowledge.html')

@app.route('/press')
def press():
    return render_template('press.html')

@app.route('/founder')
def founder():
    return render_template('founder.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/academy')
def academy():
    return render_template('academy.html')

# ---------- STATIC PDF DOWNLOAD ----------
@app.route('/download-profile')
def download_profile():
    return send_from_directory('static', 'Mamoloto_Technologies_Profile.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)