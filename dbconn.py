import os
import mysql.connector
import app



user = os.environ['DBUSER']
password = os.environ['DBPASS']
host = os.environ['DBHOST']
database =  os.environ['DB']
raise_on_warnings = True
    
  


cnx = cnx = mysql.connector.connect(user=user, password=password, host=host, port=3306, database=database, ssl_ca="{ca-cert filename}", ssl_disabled=False)

cursor = cnx.cursor(dictionary=True)

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

cnx.close()