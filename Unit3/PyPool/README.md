# PyPool

## Usage:

	usage: main.py [-h] [--csv_source_path] [--print_to_screen] [--export_to_file]
				   [--export_dest_path]

	PyPool Application

	optional arguments:
	  -h, --help           show this help message and exit
	  --csv_source_path    path for source CSV dataset(budget_data.csv)
	  --print_to_screen    print analysis result to screen
	  --export_to_file     export analysis result to file
	  --export_dest_path   path for export analysis file

## Example:
	python main.py


	PyPool Application - Data Science BootCamp 2019

	Parameters:
		Path for source CSV dataset.......: resources/election_data.csv
		Print analysis result to screen...: True
		Export analysis result to file....: True
		Path for export analysis file.....: resources/result.txt


	Election Results
	-------------------------
	Total Votes : 3521001
	-------------------------
	Khan: 63.000% (2218231)
	Correy: 20.000% (704200)
	Li: 14.000% (492940)
	O'Tooley: 3.000% (105630)
	-------------------------
	Winner : Khan
	-------------------------

	Process completed in 8.35843 second(s)

	