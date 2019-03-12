# PyBank

Usage:
	python main.py
	usage: main.py [-h] [--csv_source_path] [--print_to_screen] [--export_to_file]
				   [--export_dest_path]

	PyBank Application

	optional arguments:
	  -h, --help           show this help message and exit
	  --csv_source_path    path for source CSV dataset(budget_data.csv)
	  --print_to_screen    print analysis result to screen
	  --export_to_file     export analysis result to file
	  --export_dest_path   path for export analysis file

Example:
	python main.py


	PyBank Application - Data Science BootCamp 2019

	Parameters:
		Path for source CSV dataset.......: resources/budget_data.csv
		Print analysis result to screen...: True
		Export analysis result to file....: True
		Path for export analysis file.....: resources/result.txt


	Financial Analysis
	--------------------------------
	Total Months...................: 86
	Total..........................: $ 38,382,578.00
	Average Change.................: $ -2,315.12
	Greatest Increase in Profits...: Feb-2012 ($ 1,926,159.00)
	Greatest Decrease in Profits...: Sep-2013 ($ -2,196,167.00)

	Process completed in 0.242366 second(s)
