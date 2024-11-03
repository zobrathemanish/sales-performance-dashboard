from flask import Flask, redirect, request
import subprocess
import os

app = Flask(__name__)

# Global variable to store the Streamlit process
streamlit_process = None

@app.route('/')
def start_streamlit():
    global streamlit_process
    # Get the Render-assigned port
    port = os.environ.get("PORT", 8501)
    
    # Start Streamlit on the same port if it's not already running
    if streamlit_process is None or streamlit_process.poll() is not None:
        streamlit_process = subprocess.Popen(
            ["streamlit", "run", "streamlit_app.py", "--server.port", str(port), "--server.headless=true"]
        )
    
    # Redirect to the Streamlit app URL
    return redirect(f"http://localhost:{port}")

@app.route('/shutdown')
def shutdown():
    global streamlit_process
    if streamlit_process is not None:
        streamlit_process.terminate()
        streamlit_process = None
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return "Server shutting down..."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
