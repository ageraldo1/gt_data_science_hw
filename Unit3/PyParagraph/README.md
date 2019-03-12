# PyParagraph

## Usage:

	usage: main.py [-h] [--paragraph_source_path] [--print_to_screen]
				   [--export_to_file] [--export_dest_path]

	PyParagraph Application

	optional arguments:
	  -h, --help            show this help message and exit
	  --paragraph_source_path
							path for source paragraph file
	  --print_to_screen     print analysis result to screen
	  --export_to_file      export analysis result to file
	  --export_dest_path    path for export analysis file

## Example 1:
	python main.py


	PyParagraph Application - Data Science BootCamp 2019

	Parameters:
		Path for source CSV dataset.......: resources/paragraph_1.txt
		Print analysis result to screen...: True
		Export analysis result to file....: True
		Path for export analysis file.....: resources/result.txt


	Paragraph Analysis
	--------------------------------
	Approximate Word Count.......: 131
	Approximate Sentence Count...: 5
	Average Letter Count.........: 6.2
	Average Sentence Length......: 26.2

	Process completed in 0.109366 second(s)

## Example 2:
	 python main.py --paragraph_source_path=resources/paragraph_1.txt --export_dest_path=resources/result_1.txt


	PyParagraph Application - Data Science BootCamp 2019

	Parameters:
		Path for source CSV dataset.......: resources/paragraph_1.txt
		Print analysis result to screen...: True
		Export analysis result to file....: True
		Path for export analysis file.....: resources/result_1.txt


	Paragraph Analysis
	--------------------------------
	Approximate Word Count.......: 131
	Approximate Sentence Count...: 5
	Average Letter Count.........: 6.2
	Average Sentence Length......: 26.2

	Process completed in 0.062534 second(s)

## Example 3:
	python main.py --paragraph_source_path=resources/paragraph_2.txt --export_dest_path=resources/result_2.txt


	PyParagraph Application - Data Science BootCamp 2019

	Parameters:
		Path for source CSV dataset.......: resources/paragraph_2.txt
		Print analysis result to screen...: True
		Export analysis result to file....: True
		Path for export analysis file.....: resources/result_2.txt


	Paragraph Analysis
	--------------------------------
	Approximate Word Count.......: 285
	Approximate Sentence Count...: 11
	Average Letter Count.........: 5.0
	Average Sentence Length......: 25.9

	Process completed in 0.015626 second(s)
