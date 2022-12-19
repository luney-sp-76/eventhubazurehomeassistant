from __future__ import print_function
import dbconn
from datetime import date, datetime, timedelta

#  call to the database
cnx = dbconn.connected()
cursor = cnx.cursor(dictionary=True)


#  returns all the device specifications associated with a given user id
def list_smart_device_specs(user):
    """ :param user:int
    """
    statement = f"""select device_name, current_level_percentual_offset,wattage_percentual_offset,energy_kwh, 
    temperature_degrees_centigrade, voltage_level_percentual_offset, device_voltage.date_of_read from device
    LEFT JOIN device_current
    ON device_current.device_id = device.device_id
    LEFT JOIN device_energy
    ON device_energy.device_id = device.device_id
    LEFT JOIN device_power
    ON device_power.device_id = device.device_id
    LEFT JOIN device_temperature
    ON device_temperature.device_id = device.device_id
    LEFT JOIN device_voltage
    ON device_voltage.device_id = device.device_id
    WHERE device.is_smart_device = true and device.device_id IN(select device_id from user_device WHERE user_id = {user} )"""

    cursor.execute(statement)

    return cursor.fetchall()


results = list_smart_device_specs(1)

for row in results:
    device = row['device_name']
    current_percentage = row['current_level_percentual_offset']
    wattage = row['wattage_percentual_offset']
    energy = row['energy_kwh']
    temperature = row['temperature_degrees_centigrade']
    voltage = row['voltage_level_percentual_offset']
    date_of_read = row['date_of_read']

    print('Name: %s | Percentage: %s | Wattage:  %s | Energy %s | Temperature %s | Voltage %s | Date %s' % (
        device, current_percentage, wattage, energy, temperature, voltage, date_of_read))



#tomorrow = datetime.now().date() + timedelta(days=1)

#add_employee = ("INSERT INTO employees "
               ##############"(first_name, last_name, hire_date, gender, birth_date) "
               #############"VALUES (%s, %s, %s, %s, %s)")
############add_salary = ("INSERT INTO salaries "
              ###########"(emp_no, salary, from_date, to_date) "
             ########## "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

#########data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

# Insert new employee
########cursor.execute(add_employee, data_employee)
#######data_salary = {
  #####'emp_no': emp_no,
  ####'salary': 50000,
  ###'from_date': tomorrow,
  ##'to_date': date(9999, 1, 1),
##}
#cursor.execute(add_salary, data_salary)

# Make sure data is committed to the database
##cnx.commit()

cursor.close()
cnx.close()