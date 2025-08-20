from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from extensions import db, mongo_db
from models import *
import threading
from datetime import date, datetime, time
from sqlalchemy.orm import class_mapper

load_dotenv()
app = Flask(__name__)

# MySQL ayarları
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DATABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# MongoDB ayarları
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

# Uzantıları başlat
db.init_app(app)
mongo_db.init_app(app)

transfer_done = False

def run_transfer():
    global transfer_done
    with app.app_context():
        from database_manager import transfer_data
        transfer_data()
        transfer_done = True  # Transfer bitince mesaj değişir

# Transfer işlemini ayrı thread ile başlat
threading.Thread(target=run_transfer).start()

@app.before_request
def check_transfer_status():
    if not transfer_done and request.endpoint != 'index':
        return jsonify({"error": "Veri transferi devam ediyor, lütfen bekleyin"}), 503

@app.route('/')
def index():
    return "Veri transferi tamamlandı!" if transfer_done else "Veri transferi devam ediyor..."


def serialize_value(val):
    if isinstance(val, (datetime, date, time)):
        return val.isoformat()
    return val

@app.route('/data', methods=['GET'])
def get_all_data():
    data = {}
    # Tüm modelleri dinamik olarak al (SQLAlchemy 2.0 uyumlu)
    for mapper in db.Model.registry.mappers:
        model_class = mapper.class_
        if hasattr(model_class, '__tablename__'):
            table_name = model_class.__tablename__
            rows = model_class.query.all()
            table_data = []
            for row in rows:
                row_dict = {}
                for col in row.__table__.columns:
                    row_dict[col.name] = serialize_value(getattr(row, col.name))
                table_data.append(row_dict)
            data[table_name] = table_data

    return jsonify(data)


@app.route('/get_by_imei', methods=['GET'])
def get_data_by_imei():
    data = {}
    imei_value = request.args.get('imei')

    if not imei_value:
        return jsonify({"error": "imei parametresi eksik"}), 400

    # Tüm modelleri dinamik olarak al
    for mapper in db.Model.registry.mappers:
        model_class = mapper.class_
        if hasattr(model_class, '__tablename__'):
            table_name = model_class.__tablename__

            # Sadece 'imei' sütunu varsa sorgula
            if 'imei' in [col.name for col in model_class.__table__.columns]:
                rows = model_class.query.filter_by(imei=imei_value).all()
                table_data = []
                for row in rows:
                    row_dict = {}
                    for col in row.__table__.columns:
                        row_dict[col.name] = serialize_value(getattr(row, col.name))
                    table_data.append(row_dict)
                data[table_name] = table_data

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
