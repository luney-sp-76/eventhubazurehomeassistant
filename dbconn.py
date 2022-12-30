
import mysql.connector
import app

db_admin_name = app.DBUSER
db_server_name = app.DBHOST
db_name =  app.DB
password=app.DBPASS
    
try:
    conn = mysql.connector.connect(user=db_admin_name,
                                   password=password,
                                   database=db_name,
                                   host=db_server_name
                                   ,ssl_ca='/Users/paulolphert/git_repo/QUB Final Project/DigiCertGlobalRootCA.crt.pem')
except mysql.connector.Error as err:
    print(err) 





cursor = conn.cursor()

cursor.execute(
    'SELECT device_name, current_level_percentual_offset,wattage_percentual_offset,energy_kwh, temperature_degrees_centigrade, voltage_level_percentual_offset, '
    ' device_energy.date_of_read from device'
    ' LEFT JOIN device_current'
    ' ON device_current.device_id = device.device_id'
    ' LEFT JOIN device_energy'
    ' ON device_energy.device_id = device.device_id'
    ' LEFT JOIN device_power'
    ' ON device_power.device_id = device.device_id'
    ' LEFT JOIN device_temperature'
    ' ON device_temperature.device_id = device.device_id'
    ' LEFT JOIN device_voltage'
    ' ON device_voltage.device_id = device.device_id'
    ' WHERE device.is_smart_device = true and device.device_id IN(select device_id from user_device WHERE user_id =1);')

results = cursor.fetchall()

for row in results:
    name = row['device_name']
    percentage = row['current_level_percentual_offset']
    print('%s | %s' % (name, percentage))

conn.close()