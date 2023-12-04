from flask import Flask, render_template, request
import csv
import io
from sol import BookManager


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file and file.filename.endswith('.csv'):
            data = process_csv(file)
            return render_template('display.html', data=data)

    return render_template('upload.html')

def process_csv(file):
    # Convert the binary stream to a text stream
    text_stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)

    # Process your CSV file and return data
    csv_reader = csv.reader(text_stream)
    data = []
    book_manager = BookManager()
    for row in csv_reader:
        start_time, end_time = int(row[0]), int(row[1])
        if start_time == 0:
            data.append([start_time, end_time, book_manager.remove(end_time)])
        else:
            data.append([start_time, end_time, book_manager.add(start_time, end_time)])
    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

