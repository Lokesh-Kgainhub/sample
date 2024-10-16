import platform
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to run a Ping command with IPv4 or IPv6
def ping(host, ip_version):
    if platform.system() == "Windows":
        # Windows uses -6 for IPv6 and no flag for IPv4
        if ip_version == 'ipv6':
            command = ['ping', '-6', host]
        else:
            command = ['ping', host]
    else:
        # Linux/macOS uses -6 for IPv6 and no flag for IPv4
        if ip_version == 'ipv6':
            command = ['ping', '-6', host]
        else:
            command = ['ping', host]
    
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

# Function to run Traceroute command with IPv4 or IPv6 and timeout
def traceroute(host, ip_version):
    if platform.system() == "Windows":
        # Windows uses tracert instead of traceroute
        if ip_version == 'ipv6':
            command = ['tracert', '-6', host]
        else:
            command = ['tracert', host]
    else:
        # Linux/macOS uses traceroute
        if ip_version == 'ipv6':
            command = ['traceroute', '-6', host, '-w', '2']  # Timeout set to 2 seconds per hop
        else:
            command = ['traceroute', host, '-w', '2']  # Timeout set to 2 seconds per hop

    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

# Function to simulate a BGP query (can be extended with real BGP query implementation)
def bgp_query(host):
    return f"Simulated BGP query for {host}."

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        query_type = request.form['query_type']
        host = request.form['host']
        ip_version = request.form.get('ip_version', 'ipv4')  # Default to 'ipv4'
        
        if query_type == 'ping':
            output = ping(host, ip_version)
        elif query_type == 'traceroute':
            output = traceroute(host, ip_version)
        elif query_type == 'bgp':
            output = bgp_query(host)
        else:
            output = 'Invalid query type selected.'
    
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
