from flask import Flask
from flask import render_template
from flask import request, send_file
from listaparseri import dutylistparser
import io

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('frontpage.html')

@app.route("/convert", methods=['POST'])
def convert_to_calendar():
    f = request.files['file']
    year = int(request.form['year'])
    month = int(request.form['month'])
    calendar_string = dutylistparser(f, year, month)
    return send_file(io.BytesIO(calendar_string), as_attachment=True, download_name=f"tyovuorot.ics")
