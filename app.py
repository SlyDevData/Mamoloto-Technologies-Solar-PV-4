from flask import Flask, render_template, request, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
from datetime import datetime

app = Flask(__name__)

# ---------- EMAIL CONFIG ----------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "slycorporate@gmail.com"   
SENDER_PASSWORD = "your-app-password"   # REPLACE with Gmail App Password
RECEIVER_EMAIL = "slycorporate@gmail.com"

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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        send_email_alert(name, email, phone, subject, message)
        return render_template('contact.html', success=True)
    return render_template('contact.html', success=False)

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

@app.route('/blog')
def blog():
    # Sample blog posts (in production, fetch from DB or markdown files)
    posts = [
        {
            'title': 'The Future of AI in Solar PV 4.0',
            'date': 'June 15, 2026',
            'author': 'Dr. Mamoloto Tlabela',
            'category': 'AI & Energy',
            'excerpt': 'Artificial intelligence is transforming solar PV from static generation into dynamic, self-optimising energy systems...',
            'slug': 'future-of-ai-solar-pv'
        },
        {
            'title': 'Commissioning Guide for Hybrid Solar Systems',
            'date': 'May 28, 2026',
            'author': 'Engineering Team',
            'category': 'Technical Guides',
            'excerpt': 'A step-by-step approach to safely and efficiently commission hybrid solar PV systems in African conditions...',
            'slug': 'commissioning-guide-hybrid-solar'
        },
        {
            'title': 'Why Digital Twins Matter for African Utilities',
            'date': 'May 10, 2026',
            'author': 'Dr. Mamoloto Tlabela',
            'category': 'Digital Twin',
            'excerpt': 'Digital twins offer African utilities a powerful tool for predictive maintenance, grid stability, and operational efficiency...',
            'slug': 'digital-twins-african-utilities'
        },
        {
            'title': 'Microgrids: The Backbone of Energy Resilience',
            'date': 'April 22, 2026',
            'author': 'Research Team',
            'category': 'Microgrids',
            'excerpt': 'Hybrid microgrids combine solar, storage, and smart controls to deliver reliable power to remote communities and industrial sites...',
            'slug': 'microgrids-energy-resilience'
        }
    ]
    return render_template('blog.html', posts=posts)

# ---------- STATIC PDF DOWNLOAD ----------
@app.route('/download-profile')
def download_profile():
    return send_from_directory('static', 'Mamoloto_Technologies_Profile.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)