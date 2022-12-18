import mysql.connector
import app

def connected():
    config = {
        'user': 'poweruser',
        # 'password': 'A5DVtUB8xE6)@xr',
        'password': 'Culturekids1!',
        'host': 'dbserver-powermanager-po19760126.mysql.database.azure.com',
        # 'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
        'database': 'powermanager',
        'raise_on_warnings': True
    }
    connection_x = mysql.connector.connect(**config)
    return connection_x


cnx = connected()

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