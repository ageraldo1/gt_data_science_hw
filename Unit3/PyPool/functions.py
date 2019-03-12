import csv
import os
import io
import argparse
import datetime

def init():
    global csv_source_path
    global print_to_screen
    global export_to_file
    global export_dest_path
    global start_exec

    start_exec = datetime.datetime.now()

    parser = argparse.ArgumentParser(description='PyPool Application')
    parser.add_argument('--csv_source_path',type=str, metavar='', required=False, help='path for source CSV dataset(budget_data.csv)', default='resources/election_data.csv')
    parser.add_argument('--print_to_screen',type=lambda x: (str(x).lower() in ['true','1', 'yes']), metavar='', required=False, help='print analysis result to screen', default=True)
    parser.add_argument('--export_to_file',type=lambda x: (str(x).lower() in ['true','1', 'yes']), metavar='', required=False, help='export analysis result to file', default=True)
    parser.add_argument('--export_dest_path',type=str, metavar='', required=False, help='path for export analysis file', default='resources/result.txt')
    args = vars(parser.parse_args())

    csv_source_path = args['csv_source_path']
    print_to_screen = args['print_to_screen']
    export_to_file = args['export_to_file']
    export_dest_path = args['export_dest_path']

    splash_screen()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def splash_screen():
    clear()
    
    print (f'''
PyPool Application - Data Science BootCamp 2019

Parameters:
    Path for source CSV dataset.......: {csv_source_path}
    Print analysis result to screen...: {print_to_screen}
    Export analysis result to file....: {export_to_file}
    Path for export analysis file.....: {export_dest_path}

''')

def perform_analysis():
    candidate = {}

    analysis_result = io.StringIO()      

    with open(file=csv_source_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
     
        for line in csv_reader:
            if line['Candidate'] in candidate:
                candidate[line['Candidate']] = candidate[line['Candidate']] + 1
            else:
                candidate[line['Candidate']] = 1

        total_votes = sum(candidate.values())

        analysis_result.write("Election Results\n")
        analysis_result.write("-------------------------\n")
        analysis_result.write(f"Total Votes : {total_votes}\n")
        analysis_result.write("-------------------------\n")

        for k,v in sorted(candidate.items(), key=lambda e: e[1], reverse=True):
            analysis_result.write (f"{k}: {v/total_votes:.3%} ({v})\n")
        
        analysis_result.write("-------------------------\n")
        analysis_result.write(f"Winner : {sorted(candidate.items(), key=lambda e: e[1], reverse=True)[0][0]}\n")
        analysis_result.write("-------------------------\n")

    return analysis_result.getvalue()

def perform_output(result):
    if ( print_to_screen == True):
        print (result)
    
    if ( export_to_file == True):
        with open(export_dest_path, "w") as f:
            f.writelines(result)

def end():
    seconds_elapsed = (datetime.datetime.now() - start_exec).total_seconds()
    print (f"Process completed in {seconds_elapsed} second(s)")
