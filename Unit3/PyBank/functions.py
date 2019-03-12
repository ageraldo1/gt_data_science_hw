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

    parser = argparse.ArgumentParser(description='PyBank Application')
    parser.add_argument('--csv_source_path',type=str, metavar='', required=False, help='path for source CSV dataset(budget_data.csv)', default='resources/budget_data.csv')
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
PyBank Application - Data Science BootCamp 2019

Parameters:
    Path for source CSV dataset.......: {csv_source_path}
    Print analysis result to screen...: {print_to_screen}
    Export analysis result to file....: {export_to_file}
    Path for export analysis file.....: {export_dest_path}

''')

def perform_analysis():
    profit_lost = []
    amount_change = []

    avg_change = 0.0
    total_amount_change = 0.0
    row_offset = 2

    analysis_result = io.StringIO()      

    with open(file=csv_source_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
     
        for line in csv_reader:
            profit_lost.append(float(line["Profit/Losses"]))
            
            if ( len(profit_lost) > 1):
                # actual - previous
                amount_change.append(tuple([line["Date"], profit_lost[len(profit_lost)-1] - profit_lost[len(profit_lost)-2] ]))

        if ( csv_reader.line_num > row_offset):
            total_amount_change = sum([pair[1] for pair in amount_change])

            avg_change = total_amount_change / (csv_reader.line_num - row_offset)
            max_change = max(amount_change, key=lambda item: item[1])
            min_change = min(amount_change, key=lambda item: item[1])
            
            analysis_result.write("Financial Analysis\n")
            analysis_result.write("--------------------------------\n")
            analysis_result.write(f"Total Months...................: {len(profit_lost)}\n")
            analysis_result.write(f"Total..........................: $ {sum(profit_lost):,.2f}\n")
            analysis_result.write(f"Average Change.................: $ {avg_change:,.2f}\n")
            analysis_result.write (f"Greatest Increase in Profits...: {max_change[0]} ($ {max_change[1]:,.2f})\n")
            analysis_result.write (f"Greatest Decrease in Profits...: {min_change[0]} ($ {min_change[1]:,.2f})\n")

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
