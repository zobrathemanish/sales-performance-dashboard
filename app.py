from flask import Flask, request
import subprocess

app = Flask(__name__)

# Global variable to store the Streamlit process
streamlit_process = None

@app.route('/')
def start_streamlit():
    global streamlit_process
    # Check if Streamlit is already running; if not, start it
    if streamlit_process is None or streamlit_process.poll() is not None:
        streamlit_process = subprocess.Popen(
            ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.headless=true"]
        )
    return "Streamlit app is running!"

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
    app.run(debug=True, host="0.0.0.0", port=5000)
