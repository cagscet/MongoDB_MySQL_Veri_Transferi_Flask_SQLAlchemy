from extensions import db

class Information(db.Model):
    __tablename__ = 'information'
    id = db.Column(db.String(36), primary_key=True)
    imei = db.Column(db.BigInteger)
    version = db.Column(db.String(50), nullable=True)
    LastIP = db.Column(db.String(50), nullable=True)
    mac = db.Column(db.String(50), nullable=True)
    prov_version = db.Column(db.String(50), nullable=True)
    conf_version = db.Column(db.String(50), nullable=True)
    cpu_serial = db.Column(db.String(50), nullable=True)
    hw_version = db.Column(db.String(50), nullable=True)
    gsm_modul_name = db.Column(db.String(50), nullable=True)
    gsm_connect_type = db.Column(db.String(50), nullable=True)
    imsi = db.Column(db.BigInteger, nullable=True)
    sim_id = db.Column(db.BigInteger, nullable=True)
    gsm_no = db.Column(db.BigInteger, nullable=True)
    operator_name = db.Column(db.String(50), nullable=True)
    cell_MNC = db.Column(db.Integer, nullable=True)
    cell_MCC = db.Column(db.Integer, nullable=True)
    LAC = db.Column(db.Integer, nullable=True)
    serialno = db.Column(db.Integer, nullable=True)

class Relays(db.Model):
    __tablename__ = 'relays'
    id = db.Column(db.String(36), primary_key=True)
    imei = db.Column(db.BigInteger)
    date = db.Column(db.Date, nullable=True)
    RelayID = db.Column(db.Integer, nullable=True)
    ChangeDate = db.Column(db.Time, nullable=True)
    State = db.Column(db.Integer, nullable=True)

class RebootInfo(db.Model):
    __tablename__ = 'reboot_info'
    id = db.Column(db.String(36), primary_key=True)
    imei = db.Column(db.BigInteger)
    date = db.Column(db.Date, nullable=True)
    reboot_time = db.Column(db.Time, nullable=True)
    RebootType = db.Column(db.String(50), nullable=True)

class AcFailInfo(db.Model):
    __tablename__ = 'ac_fail_info'
    id = db.Column(db.String(36), primary_key=True)
    imei = db.Column(db.BigInteger)
    date = db.Column(db.Date, nullable=True)
    ac_time = db.Column(db.Time, nullable=True)
    ac_state = db.Column(db.String(50), nullable=True)

class GSMConnectionInfo(db.Model):
    __tablename__ = 'gsm_connection_info'
    id = db.Column(db.String(36), primary_key=True)
    imei = db.Column(db.BigInteger)
    datetime = db.Column(db.DateTime, nullable=True)
    conn_or_disconn = db.Column(db.Boolean, nullable=True)  # TINYINT(1) yerine Boolean
    ip = db.Column(db.String(50), nullable=True)
    SignalLevel = db.Column(db.Integer, nullable=True)
    mmc = db.Column(db.Integer, nullable=True)
    mcc = db.Column(db.Integer, nullable=True)
    lac = db.Column(db.Integer, nullable=True)
    cid = db.Column(db.Integer, nullable=True)

class ServerConnectionInfo(db.Model):
    __tablename__ = 'server_connection_info'
    id = db.Column(db.String(36), primary_key=True)
    imei = db.Column(db.BigInteger)
    datetime = db.Column(db.DateTime, nullable=True)
    conn_or_disconn = db.Column(db.Boolean, nullable=True)

class Monitor(db.Model):
    __tablename__ = 'monitor'
    id = db.Column(db.String(36), primary_key=True)
    imei = db.Column(db.BigInteger)
    datetime = db.Column(db.DateTime, nullable=True)
    usage_flash = db.Column(db.Integer, nullable=True)
    usage_ram = db.Column(db.Integer, nullable=True)
    battery_temp = db.Column(db.Integer, nullable=True)
    battery_volt = db.Column(db.Integer, nullable=True)
    cpu_temp = db.Column(db.Integer, nullable=True)
    gsmSignalLevel = db.Column(db.Integer, nullable=True)

class Meters(db.Model):
    __tablename__ = 'meters'
    id = db.Column(db.String(36), primary_key=True)
    imei = db.Column(db.BigInteger)
    meter_serial = db.Column(db.Integer, nullable=True)

class MeterData(db.Model):
    __tablename__ = 'MeterData'
    id = db.Column(db.String(36), primary_key=True)
    imei = db.Column(db.BigInteger)
    meter_serial = db.Column(db.Integer, nullable=True)
    datetime = db.Column(db.DateTime, nullable=True)
    DailyCount = db.Column(db.Integer, nullable=True)
    NumofSend = db.Column(db.Integer, nullable=True)
    dataUID = db.Column(db.BigInteger, nullable=True)
    Rate = db.Column(db.Integer, nullable=True)

class MeterDataDetails(db.Model):
    __tablename__ = 'MeterDataDetails'
    id = db.Column(db.String(36), primary_key=True)
    meterID = db.Column(db.String(24), nullable=True)
    dataUID = db.Column(db.BigInteger, nullable=True)
    DataType = db.Column(db.BigInteger, nullable=True)
    Data_Time = db.Column(db.BigInteger, nullable=True)
