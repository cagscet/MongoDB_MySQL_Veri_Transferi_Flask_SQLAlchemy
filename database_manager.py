import os
from datetime import datetime
import uuid
from extensions import db, mongo_db
from models import Information, Relays, RebootInfo, AcFailInfo, GSMConnectionInfo, ServerConnectionInfo, Monitor, Meters, MeterData, MeterDataDetails

def transfer_data():
    mongo_database = mongo_db.cx[os.getenv("MONGO_DB")]
    collection = mongo_database[os.getenv("MONGO_COLLECTION")]
    documents = collection.find()

    count = 0
    for doc in documents:
        info = doc.get('INFORMATION', {})
        comm = info.get('COMM', {})

        new_info = Information(
            id=str(doc.get('_id')),
            imei=int(comm.get('IMEI')) if comm.get('IMEI') else None,
            version=info.get('version'),
            LastIP=info.get('Last_IP'),
            mac=info.get('mac'),
            prov_version=None,  # JSON'da yoksa None bırakabilirsin
            conf_version=None,
            cpu_serial=info.get('cpu_serial'),
            hw_version=info.get('hw_version'),
            gsm_modul_name=comm.get('gsm_module_version'),
            gsm_connect_type=comm.get('module_type'),
            imsi=int(comm.get('IMSI')) if comm.get('IMSI') else None,
            sim_id=None,
            gsm_no=None,
            operator_name=None,
            cell_MNC=int(info.get('COMM', {}).get('MNC')) if info.get('COMM', {}).get('MNC') else None,
            cell_MCC=int(info.get('COMM', {}).get('MCC')) if info.get('COMM', {}).get('MCC') else None,
            LAC=int(info.get('COMM', {}).get('LAC')) if info.get('COMM', {}).get('LAC') else None,
            serialno=None
        )
        try:
            db.session.merge(new_info)
            count += 1
        except Exception as e:
            print(f"Hata oluştu: {e}")
            db.session.rollback()
    try:
        db.session.commit()
        print(f"{count} kayıt MySQL'e başarıyla aktarıldı.")
    except Exception as e:
        db.session.rollback()
        print(f"Hata oluştu: {e}")

def transfer_information(doc):
    info = doc.get('INFORMATION', {})
    comm = info.get('COMM', {})

    new_info = Information(
        id=str(doc.get('_id')),
        imei=int(comm.get('IMEI')) if comm.get('IMEI') else None,
        version=info.get('version'),
        LastIP=info.get('Last_IP'),
        mac=info.get('mac'),
        prov_version=None,
        conf_version=None,
        cpu_serial=info.get('cpu_serial'),
        hw_version=info.get('hw_version'),
        gsm_modul_name=comm.get('gsm_module_version'),
        gsm_connect_type=comm.get('module_type'),
        imsi=int(comm.get('IMSI')) if comm.get('IMSI') else None,
        sim_id=None,
        gsm_no=None,
        operator_name=None,
        cell_MNC=int(info.get('COMM', {}).get('MNC')) if info.get('COMM', {}).get('MNC') else None,
        cell_MCC=int(info.get('COMM', {}).get('MCC')) if info.get('COMM', {}).get('MCC') else None,
        LAC=int(info.get('COMM', {}).get('LAC')) if info.get('COMM', {}).get('LAC') else None,
        serialno=None
    )
    try:
        db.session.merge(new_info)
    except Exception as e:
        print(f"Information tablosu aktarım hatası: {e}")
        db.session.rollback()

def transfer_relays(doc):
    event = doc.get('EVENT', {})
    for relay_key in ['RELAY1', 'RELAY2', 'RELAY3']:
        relay_events = event.get(relay_key, [])
        relay_id = int(relay_key.replace('RELAY', ''))
        for r in relay_events:
            state = int(r.get('state')) if r.get('state') else None
            date_time_str = r.get('date')
            if date_time_str:
                dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                date_only = dt.date()
                time_only = dt.time()
            else:
                date_only = None
                time_only = None

            new_relay = Relays(
                id=str(uuid.uuid4()),
                imei=int(doc.get('imei')) if doc.get('imei') else None,
                date=date_only,
                RelayID=relay_id,
                ChangeDate=time_only,
                State=state
            )
            db.session.merge(new_relay)

def transfer_reboot_info(doc):
    event = doc.get('EVENT', {})
    reboot_events = event.get('Reboot', [])
    for r in reboot_events:
        state = r.get('state')
        date_time_str = r.get('date')
        if date_time_str:
            dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            date_only = dt.date()
            time_only = dt.time()
        else:
            date_only = None
            time_only = None
        new_reboot = RebootInfo(
            id=str(uuid.uuid4()),
            imei=int(doc.get('imei')) if doc.get('imei') else None,
            date=date_only,
            reboot_time=time_only,
            RebootType=state
        )
        db.session.merge(new_reboot)

def transfer_ac_fail_info(doc):
    event = doc.get('EVENT', {})
    ac_events = event.get('AC', [])
    for r in ac_events:
        state = r.get('state')
        date_time_str = r.get('date')
        if date_time_str:
            dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            date_only = dt.date()
            time_only = dt.time()
        else:
            date_only = None
            time_only = None
        new_ac = AcFailInfo(
            id=str(uuid.uuid4()),
            imei=int(doc.get('imei')) if doc.get('imei') else None,
            date=date_only,
            ac_time=time_only,
            ac_state=state
        )
        db.session.merge(new_ac)

def transfer_gsm_connection_info(doc):
    gsm_conn = doc.get('GSMCONNECTIONINFO', {})
    log_list = gsm_conn.get('LogOfConnection', [])
    for log in log_list:
        date_time_str = log.get('date_time')
        if date_time_str:
            dt = datetime.strptime(date_time_str, '%Y-%m-%d,%H:%M:%S')
        else:
            dt = None
        new_gsm = GSMConnectionInfo(
            id=str(uuid.uuid4()),
            imei=int(doc.get('imei')) if doc.get('imei') else None,
            datetime=dt,
            conn_or_disconn=True,
            ip=log.get('IP'),
            SignalLevel=int(log.get('SignalLevel')) if log.get('SignalLevel') else None,
            mmc=int(log.get('MNC')) if log.get('MNC') else None,
            mcc=int(log.get('MCC')) if log.get('MCC') else None,
            lac=int(log.get('LAC')) if log.get('LAC') else None,
            cid=int(log.get('CID')) if log.get('CID') else None
        )
        db.session.merge(new_gsm)

def transfer_server_connection_info(doc):
    server_conn = doc.get('SERVERCONNECTIONINFO', {})
    # Burada LogOfConnection vb yok, sadece sayı var, örnek JSON’da detay yok.
    # Örnek yapalım, ama gerçek veride detay varsa ona göre genişletilebilir.
    # Zaten datetime vb yok.
    # Bu tabloya veri atmak için uygun alanlar yok görünüyor JSON’da.
    pass

def transfer_monitor(doc):
    monitor = doc.get('MONITOR', {})
    gsmSignalLevel_list = monitor.get('gsmSignalLevel', [])
    usage_flash_list = monitor.get('usage_flash', [])
    usage_ram_list = monitor.get('usage_ram', [])
    battery_temp_list = monitor.get('battery_temp', [])
    battery_volt_list = monitor.get('battery_volt', [])
    cpu_temp_list = monitor.get('cpu_temp', [])

    # Burada genelde listeler var, tek bir tarih yok.
    # Eğer tarih yoksa örnek olarak tek bir kayıt atabiliriz ya da atlama yapılabilir.
    # Biz basitçe tek kayıt atıyoruz ilk elemanlarla.

    def safe_int(val):
        try:
            if val is None:
                return None
            if isinstance(val, str):
                return int(val.replace('%','').strip())
            return int(val)
        except:
            return None

    new_monitor = Monitor(
        id=str(uuid.uuid4()),
        imei=int(doc.get('imei')) if doc.get('imei') else None,
        datetime=None,  # JSON'da datetime yok
        usage_flash=safe_int(usage_flash_list[0]) if usage_flash_list else None,
        usage_ram=safe_int(usage_ram_list[0]) if usage_ram_list else None,
        battery_temp=safe_int(battery_temp_list[0]) if battery_temp_list else None,
        battery_volt=safe_int(battery_volt_list[0]) if battery_volt_list else None,
        cpu_temp=safe_int(cpu_temp_list[0]) if cpu_temp_list else None,
        gsmSignalLevel=safe_int(gsmSignalLevel_list[0]) if gsmSignalLevel_list else None
    )
    db.session.merge(new_monitor)

def transfer_meters(doc):
    # JSON’da meters için uygun alan göremedim, varsa ekleyebiliriz.
    pass

def transfer_meter_data(doc):
    performance = doc.get('PERFORMANCE', {})
    default_inst = performance.get('DefaultInst') or performance.get('DefaultINST') or performance.get('DefaultINSTPROG')
    if not default_inst:
        return
    for meter_serial_str, data in default_inst.items():
        new_meter_data = MeterData(
            id=str(uuid.uuid4()),
            imei=int(doc.get('imei')) if doc.get('imei') else None,
            meter_serial=int(meter_serial_str),
            datetime=None,
            DailyCount=data.get('DailyCount'),
            NumofSend=data.get('NumofSend'),
            dataUID=None,
            Rate=int(float(str(data.get('RATE','0').replace('%','').replace(',','.'))) if data.get('RATE') else 0)
        )
        db.session.merge(new_meter_data)

def transfer_meter_data_details(doc):
    # JSON’da bu detaylar yok, varsa buraya eklenir
    pass

def transfer_data():
    mongo_database = mongo_db.cx[os.getenv("MONGO_DB")]
    collection = mongo_database[os.getenv("MONGO_COLLECTION")]
    documents = collection.find()

    count = 0
    for doc in documents:
        transfer_information(doc)
        transfer_relays(doc)
        transfer_reboot_info(doc)
        transfer_ac_fail_info(doc)
        transfer_gsm_connection_info(doc)
        transfer_server_connection_info(doc)
        transfer_monitor(doc)
        transfer_meters(doc)
        transfer_meter_data(doc)
        transfer_meter_data_details(doc)
        count += 1

    try:
        db.session.commit()
        print(f"{count} kayıt MySQL'e başarıyla aktarıldı.")
    except Exception as e:
        db.session.rollback()
        print(f"Commit sırasında hata: {e}")