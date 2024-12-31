# from flask import Flask, Response, request, render_template_string, jsonify
# import cv2
# import smtplib
# from email.mime.text import MIMEText
# from model import Model
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = Flask(__name__)

# # Email Configuration
# SENDER_EMAIL = "omarkamalabuassaf1@gmail.com"
# SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# model = Model()

# violence_detected = False
# email_sent = False
# camera_feed_url = None
# recipient_email = None


# def send_email():
#     """
#     Sends an email notification when violence is detected.
#     """
#     global email_sent
#     if email_sent or not recipient_email:
#         return

#     try:
#         subject = "Violence Detected Alert"
#         body = "Violence has been detected in the live CCTV feed. Please take immediate action."
#         msg = MIMEText(body)
#         msg['Subject'] = subject
#         msg['From'] = SENDER_EMAIL
#         msg['To'] = recipient_email

#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(SENDER_EMAIL, SENDER_PASSWORD)
#             server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
#             print("Email sent successfully!")
#         email_sent = True  # Set the flag to avoid duplicate emails
#     except Exception as e:
#         print(f"Failed to send email: {e}")


# def generate_frames():
#     """
#     Capture frames from the camera feed and process them for violence detection.
#     """
#     global violence_detected, email_sent
#     if not camera_feed_url:
#         return

#     cap = cv2.VideoCapture(camera_feed_url)

#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         label = model.predict(image=frame)['label']
#         violence_detected = (label.lower() == "violence")

#         if violence_detected:
#             cv2.putText(frame, "VIOLENCE DETECTED!", (10, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
#             send_email()
#         else:
#             email_sent = False

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     """
#     Render the main page with the form and live stream.
#     """
#     global camera_feed_url, recipient_email

#     if request.method == 'POST':
#         camera_feed_url = request.form.get('camera_feed_url')
#         recipient_email = request.form.get('recipient_email')

#     return render_template_string('''
#     <!doctype html>
#     <html lang="en">
#     <head>
#         <title>Live CCTV Feed</title>
#         <style>
#             body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f9; color: #333; }
#             h1 { margin: 20px; }
#             .alert { color: red; font-size: 24px; font-weight: bold; margin-top: 20px; }
#             video { width: 80%; height: auto; margin: auto; display: block; }
#             form { margin: 20px; }
#             input { padding: 10px; margin: 10px; font-size: 16px; }
#             button { padding: 10px 20px; font-size: 16px; }
#         </style>
#     </head>
#     <body>
#         <h1>Live CCTV Feed</h1>
#         <form method="POST">
#             <input type="text" name="camera_feed_url" placeholder="Enter Camera IP Address" required>
#             <input type="email" name="recipient_email" placeholder="Enter Recipient Email" required>
#             <button type="submit">Start Surveillance</button>
#         </form>
#         {% if camera_feed_url and recipient_email %}
#             <img src="/video_feed" alt="Live Video Feed">
#             <div id="alert-box" class="alert"></div>
#         {% endif %}
#         <footer>&copy; 2024 Live CCTV Surveillance</footer>
#     </body>
#     </html>
#     ''', camera_feed_url=camera_feed_url, recipient_email=recipient_email)


# @app.route('/video_feed')
# def video_feed():
#     """
#     Route to serve the video feed.
#     """
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/violence_status')
# def violence_status():
#     """
#     API endpoint to return the current violence status.
#     """
#     return jsonify({"violence": violence_detected})


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)




from flask import Flask, Response, request, render_template_string, jsonify
import cv2
import smtplib
from email.mime.text import MIMEText
from model import Model
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Email Configuration
SENDER_EMAIL = "omarkamalabuassaf1@gmail.com"
SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

model = Model()

violence_detected = False
email_sent = False
camera_feed_url = None
recipient_email = None


def send_email():
    """
    Sends an email notification when violence is detected.
    """
    global email_sent
    if email_sent or not recipient_email:
        return

    try:
        subject = "Violence Detected Alert"
        body = "Violence has been detected in the live CCTV feed. Please take immediate action."
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
            print("Email sent successfully!")
        email_sent = True  # Set the flag to avoid duplicate emails
    except Exception as e:
        print(f"Failed to send email: {e}")


def generate_frames():
    """
    Capture frames from the camera feed and process them for violence detection.
    """
    global violence_detected, email_sent
    if not camera_feed_url:
        return

    cap = cv2.VideoCapture(camera_feed_url)

    while True:
        success, frame = cap.read()
        if not success:
            break

        label = model.predict(image=frame)['label']
        violence_detected = (label.lower() == "violence")

        if violence_detected:
            cv2.putText(frame, "VIOLENCE DETECTED!", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            send_email()
        else:
            email_sent = False

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Render the main page with the form and live stream.
    """
    global camera_feed_url, recipient_email

    if request.method == 'POST':
        ip_address = request.form.get('ip_address')
        port = request.form.get('port')
        recipient_email = request.form.get('recipient_email')
        camera_feed_url = f"http://{ip_address}:{port}/video"

    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <title>Live CCTV Feed</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f9; color: #333; }
            h1 { margin: 20px; }
            .alert { color: red; font-size: 24px; font-weight: bold; margin-top: 20px; }
            video { width: 80%; height: auto; margin: auto; display: block; }
            form { margin: 20px; }
            input { padding: 10px; margin: 10px; font-size: 16px; }
            button { padding: 10px 20px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Live CCTV Feed</h1>
        <form method="POST">
            <input type="text" name="ip_address" placeholder="Enter IP Address (e.g., 192.168.10.236)" required>
            <input type="text" name="port" placeholder="Enter Port (e.g., 4747)" required>
            <input type="email" name="recipient_email" placeholder="Enter Recipient Email" required>
            <button type="submit">Start Surveillance</button>
        </form>
        {% if camera_feed_url and recipient_email %}
            <img src="/video_feed" alt="Live Video Feed">
            <div id="alert-box" class="alert"></div>
        {% endif %}
        <footer>&copy; 2024 Live CCTV Surveillance</footer>
    </body>
    </html>
    ''', camera_feed_url=camera_feed_url, recipient_email=recipient_email)


@app.route('/video_feed')
def video_feed():
    """
    Route to serve the video feed.
    """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/violence_status')
def violence_status():
    """
    API endpoint to return the current violence status.
    """
    return jsonify({"violence": violence_detected})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

