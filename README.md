ScraperEvents2.py is added to Windows Task Scheduer to run every 10 minutes. The script saves the data to CSV files in the directory where it was run from. The HTML files read in the CSV files and display in a table.
These files are in an Apache HTTP server directory - browsers cannot read files directly (Security reasons, obviously!), so the CSV files must be accessable via the localhost server.
The different HTML files were shown in rotation using Vue Pilot.

