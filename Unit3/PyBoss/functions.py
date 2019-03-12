import csv
import os
import io
import argparse
import datetime
import re

def init():
    global csv_source_path
    global export_dest_path
    global start_exec

    start_exec = datetime.datetime.now()

    parser = argparse.ArgumentParser(description='PyBoss Application')
    parser.add_argument('--csv_source_path',type=str, metavar='', required=False, help='path for source CSV dataset', default='resources/employee_data.csv')
    parser.add_argument('--export_dest_path',type=str, metavar='', required=False, help='path for export analysis file', default='resources/new_employee_data.csv')
    args = vars(parser.parse_args())

    csv_source_path = args['csv_source_path']
    export_dest_path = args['export_dest_path']

    splash_screen()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def splash_screen():
    clear()
    
    print (f'''
PyBoss Application - Data Science BootCamp 2019

Parameters:
    Path for source CSV dataset.......: {csv_source_path}
    Path for export analysis file.....: {export_dest_path}

''')

def transform():

    record = {}

    with open(file=csv_source_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        with open(file=export_dest_path, mode='w', newline='') as csv_new_file:
            field_names = ["Emp ID", "First Name", "Last Name", "DOB", "SSN", "State"]

            csv_writer = csv.DictWriter(csv_new_file, fieldnames=field_names, delimiter=',')
            csv_writer.writeheader()

            for line in csv_reader:
                source_date = datetime.datetime.strptime(line["DOB"], "%Y-%m-%d")

                record["Emp ID"] = line["Emp ID"]
                record["First Name"] = line["Name"].split(sep=' ')[0]
                record["Last Name"] = line["Name"].split(sep=' ')[1]
                record["DOB"] = str(source_date.month) + "/" + str(source_date.day) + "/" + str(source_date.year)
                record["SSN"] = re.sub('\d', '*', line["SSN"][:-4]) + line["SSN"][-4:]
                record["State"] = get_state_code(line["State"])

                csv_writer.writerow(record)

def perform_output(result):
    pass

def end():
    seconds_elapsed = (datetime.datetime.now() - start_exec).total_seconds()
    print (f"Process completed in {seconds_elapsed} second(s)")

def get_state_code(state_name):
    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
    }    

    return us_state_abbrev[state_name]