import csv
import os
import io
import argparse
import datetime
import re


def init():
    global paragraph_source_path
    global print_to_screen
    global export_to_file
    global export_dest_path
    global start_exec

    start_exec = datetime.datetime.now()

    parser = argparse.ArgumentParser(description='PyParagraph Application')
    parser.add_argument('--paragraph_source_path',type=str, metavar='', required=False, help='path for source paragraph file', default='resources/paragraph_1.txt')
    parser.add_argument('--print_to_screen',type=lambda x: (str(x).lower() in ['true','1', 'yes']), metavar='', required=False, help='print analysis result to screen', default=True)
    parser.add_argument('--export_to_file',type=lambda x: (str(x).lower() in ['true','1', 'yes']), metavar='', required=False, help='export analysis result to file', default=True)
    parser.add_argument('--export_dest_path',type=str, metavar='', required=False, help='path for export analysis file', default='resources/result.txt')
    args = vars(parser.parse_args())

    paragraph_source_path = args['paragraph_source_path']
    print_to_screen = args['print_to_screen']
    export_to_file = args['export_to_file']
    export_dest_path = args['export_dest_path']

    splash_screen()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def splash_screen():
    clear()
    
    print (f'''
PyParagraph Application - Data Science BootCamp 2019

Parameters:
    Path for source CSV dataset.......: {paragraph_source_path}
    Print analysis result to screen...: {print_to_screen}
    Export analysis result to file....: {export_to_file}
    Path for export analysis file.....: {export_dest_path}

''')

def perform_analysis():

    analysis_result = io.StringIO()
    
    p_analysis = {
        "word_count": "'?([_-a-zA-z0-9']+)'?",
        "sentence_count": "[^\.\!\?]*[\.\!\?]",
        "letter_count": "[A-Za-z]",
        "sentence_length": "[.!?]\s?"
    }

    p_result = []

    with open(file=paragraph_source_path, mode='r', encoding='utf-8') as f:
        content = f.read()

        for k,v in p_analysis.items():
            pattern = re.compile(r'{}'.format(v))
            matches = pattern.finditer(content)

            p_result.append(len(tuple(matches)))

        p_result.append(p_result[2]/p_result[0] if p_result[0] > 0 else 0 ) # average letter count
        p_result.append(p_result[0]/p_result[3] if p_result[3] > 0 else 0 ) # average sentence length

        analysis_result.write("Paragraph Analysis\n")
        analysis_result.write("--------------------------------\n")
        analysis_result.write(f"Approximate Word Count.......: {p_result[0]}\n")
        analysis_result.write(f"Approximate Sentence Count...: {p_result[1]}\n")
        analysis_result.write(f"Average Letter Count.........: {p_result[4]:,.1f}\n")
        analysis_result.write(f"Average Sentence Length......: {p_result[5]:,.1f}\n")

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
