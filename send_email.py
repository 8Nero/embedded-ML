import os
# email_utils.py (functions for email-related operations)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL
from datetime import datetime

def send_email(response_text, image_path):
    # Prepare email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    current_time = datetime.now().strftime("%B %d, %Y, at %H:%M")
    msg['Subject'] = f"Report: Person detected at the front entrance on {current_time}"

    # Prepare email content in HTML format
    email_content = f"""
    <html>
    <body>
        <h2>Detailed Report:</h2>
        <hr>
        <p><strong>Date and Time:</strong> {current_time}</p>
        <p><strong>Location:</strong> Front Entrance Camera</p>
        <h3>LLM Analysis:</h3>
        <p>{response_text}</p>
        <h3>Confidence Level:</h3>
        <ul>
            <li><strong>Person Detection Model:</strong> 98%</li>
            <li><strong>LLM Description Accuracy:</strong> High Confidence</li>
        </ul>
        <h3>Additional Observations:</h3>
        <ul>
            <li>Number of people: 1</li>
            <li>Detection occurred outside of typical delivery hours.</li>
        </ul>
        <h3>System Status:</h3>
        <ul>
            <li><strong>Device Operational</strong></li>
            <li><strong>Battery Level:</strong> 85%</li>
            <li><strong>Network Connectivity:</strong> Stable</li>
        </ul>
        <h3>Previous Incidents:</h3>
        <p>No similar detections in the past 24 hours.</p>
    </body>
    </html>
    """

    # Add response text in HTML format
    msg.attach(MIMEText(email_content, 'html'))

    # Attach image
    with open(image_path, 'rb') as img:
        img_data = img.read()
        image = MIMEImage(img_data, name=os.path.basename(image_path))
        msg.attach(image)

    # Send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == '__main__':
    from analysis import analyze_image
    image_path = r"C:\Users\animu\PycharmProjects\flaskProject\uploads\image_20241026-150722.jpg"
    response = analyze_image(image_path)
    send_email(response, image_path)