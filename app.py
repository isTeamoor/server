from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import shutil
import string
from datetime import datetime
from PIL import Image

from database import query, createTable

createTable()

if not os.path.exists("server/images"):
    os.makedirs("server/images")
if not os.path.exists("server/images/compressed"):
    os.makedirs("server/images/compressed")

def sanitize_filename(filename):
    forbidden_characters = "\\?%*:|\"\{|}\/<>!$"
    sanitized_filename = ''.join(c for c in filename if c not in forbidden_characters)
    return sanitized_filename

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({'data': 'Hi'})

@app.route('/db/newLot', methods=['POST'])
def createLot():
    img = request.files['img']
    img_name = sanitize_filename(img.filename)
    description = sanitize_filename(request.form['description'])
    label = sanitize_filename(request.form['label'])
    user_id = request.form['user_id']

    currentDate = datetime.now()
    mark = str(int(currentDate.timestamp()*100000000))

    filename = os.path.splitext(img_name)[0] + "-" + mark + os.path.splitext(img_name)[1]

    img.save(os.path.join("server/images", filename))

    orig_img = os.path.join("server/images", filename)
    img = Image.open(orig_img)
    img = img.convert("RGB")
    img.thumbnail((img.width // 2, img.height // 2))

    compressed_filename = os.path.splitext(filename)[0] + '.jpg'
    img.save(os.path.join("server/images/compressed", compressed_filename), format="JPEG", quality=50)

    ### Создание записей в бд
    newLot = query('set', f"INSERT INTO lots (label, description, img) VALUES ('{label}', '{description}', '{filename}')", 'lots')
    return jsonify({'creating new lot': 'success'})


@app.route('/db/allLots')
def send_Lots():
    data = query('get', "SELECT * FROM lots")
    response = []
    for item in data:
        lot = {
            'id': item[0],
            'label': item[1],
            'description': item[2],
            'bids': item[3],
            'img': 'https://isteamoor1.pythonanywhere.com/db/get_image/' + item[3],
        }
        response.append(lot)
    return jsonify(response)

@app.route('/db/get_image/<img>/<section>')
def get_image(section, img):
    section = sanitize_filename(section)
    img = sanitize_filename(img)
    img_path = ''

    current_directory = os.getcwd()

    if section == 'c':
        img_path = os.getcwd() +'/server/images/compressed/' + os.path.splitext(img)[0] + '.jpg'
    elif section == 'f':
        img_path = os.getcwd() +'/server/images/' + img
    if not os.path.exists(img_path):
        return jsonify({"error": img_path})


    return send_file(img_path, mimetype='image/jpeg')


@app.route('/db/newBid', methods=['POST'])
def new_Bid():
    data = request.json
    lot_id = data['lot_id']
    user_id = data['user_id']
    amount = data['amount']
    date = data['date']
    query('set', f"INSERT INTO bids (lot_id, user_id, amount, date) VALUES ('{lot_id}', '{user_id}', '{amount}', '{date}')", 'bids')

    bids = query('get',f"SELECT * FROM bids WHERE lot_id = '{lot_id}'")
    response = []
    for bid in bids:
        response.append({
            'id': bid[0],
            'lot_id': bid[1],
            'user_id': bid[2],
            'amount': bid[3],
            'date': bid[4]
        })
    return jsonify({'bids': response})



if __name__ == "__main__":
    app.run(debug=True)
