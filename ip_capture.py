from flask import Flask, request
import datetime
import os
import socket

app = Flask(__name__)

# Ensure log file exists
if not os.path.exists('ips_log.txt'):
    with open('ips_log.txt', 'w') as f:
        f.write("IP Capture Log - Educational Purpose\n")

@app.route('/')
def home():
    # Return a simple page with just a button
    return """
    <html>
    <head><title>Demo</title></head>
    <body>
    <form action="/capture" method="post">
        <button type="submit">Click here</button>
    </form>
    </body>
    </html>
    """

@app.route('/capture', methods=['POST'])
def capture():
    # Get visitor's IP address
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get server's IP address
    try:
        server_ip = socket.gethostbyname(socket.gethostname())
    except:
        server_ip = "Unable to determine"

    # Log to file and console
    log_entry = f"{timestamp} - Visitor IP: {ip} - Server IP: {server_ip} - User-Agent: {user_agent}"
    with open('ips_log.txt', 'a') as f:
        f.write(log_entry + '\n')
    print(log_entry)  # Also print to console for Render logs

    # Return empty response - no page displayed
    return '', 204

@app.route('/admin')
def admin():
    try:
        with open('ips_log.txt', 'r') as f:
            log_content = f.read()
        return f"""
        <html>
        <head><title>Admin - IP Logs</title></head>
        <body>
        <h1>IP Capture Logs</h1>
        <pre style="background-color: #f5f5f5; padding: 20px; font-family: monospace; white-space: pre-wrap;">{log_content}</pre>
        <p><a href="/">Back to Site</a></p>
        </body>
        </html>
        """
    except FileNotFoundError:
        return "<h1>No logs yet</h1>"



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Starting IP capture server...")
    print(f"Running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
