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
    # Return the main page with a button
    return """
    <html>
    <head><title>Welcome</title></head>
    <body>
    <h1>Welcome to Our Website</h1>
    <p>Thank you for visiting! This is a demonstration website.</p>
    <p>Click the button below to participate in our visitor tracking demo:</p>
    <form action="/capture" method="post">
        <button type="submit" style="padding: 10px 20px; font-size: 16px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">Click here</button>
    </form>
    <p>Learn more about web development at: <a href="https://example.com">Web Basics</a></p>
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

    # Return confirmation page (without showing captured details)
    return """
    <html>
    <head><title>Thank You</title></head>
    <body>
    <h1>Thank You!</h1>
    <p>Your visit has been recorded in our demo log.</p>
    <p><a href="/">Back to Home</a> | <a href="/logs">View All Logs</a></p>
    </body>
    </html>
    """

@app.route('/logs')
def view_logs():
    try:
        with open('ips_log.txt', 'r') as f:
            log_content = f.read()
        # Format the logs for display, hiding server IP for privacy
        log_lines = log_content.split('\n')
        # Remove server IP information from display
        filtered_lines = []
        for line in log_lines:
            if ' - Server IP: ' in line:
                # Remove the server IP part from the line
                parts = line.split(' - Server IP: ')
                if len(parts) > 1:
                    # Keep only the part before server IP and after the next separator
                    visitor_part = parts[0]
                    remaining_part = parts[1].split(' - ', 1)
                    if len(remaining_part) > 1:
                        line = visitor_part + ' - ' + remaining_part[1]
                    else:
                        line = visitor_part
            filtered_lines.append(line)
        formatted_logs = '<br>'.join(filtered_lines)
        return f"""
        <html>
        <head><title>IP Capture Logs</title></head>
        <body>
        <h1>IP Capture Logs</h1>
        <p>Educational Purpose - Visitor Tracking Demo</p>
        <div style="background-color: #f5f5f5; padding: 20px; border: 1px solid #ddd; font-family: monospace; white-space: pre-wrap;">
        {formatted_logs}
        </div>
        <p><a href="/">Back to Home</a></p>
        </body>
        </html>
        """
    except FileNotFoundError:
        return """
        <html>
        <head><title>Logs</title></head>
        <body>
        <h1>No Logs Yet</h1>
        <p>No visitor data has been captured yet.</p>
        <p><a href="/">Back to Home</a></p>
        </body>
        </html>
        """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Starting IP capture server...")
    print(f"Running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
