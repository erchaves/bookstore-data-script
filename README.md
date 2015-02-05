# bookstore-data-script
A simple script to parse some file data

By default, the makeReport.py file should be in the same directory as a folder called ```process_home``` (the name used by the bookstore's file system).
Running ```python makeReport.py``` will create a report.csv file.

Some settings can be tweaked with variables declared at the top of makeReport.py.  For example:
```
shouldFilterZeroValues = True
datdDirectoryPath = 'process_home'
reportFilePath = 'report.csv'
```