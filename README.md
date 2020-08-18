# Library Rat's Diary

Library Rat's Diary is a program for cataloging your reading history and display statitics and graphs about your book library. 

LRD is meant to replace spreadsheet control for readers who prefer these over an online service like Goodreads or LibraryThing. LRD accepts every user's whims - all fields are optional, even Title.

### Running from source code

Windows:

1. Download LRD by clicking on **Code** > **Download ZIP** near the top of this page and extract the ZIP.
2. Download Python 3.7 or better from [python.org](https://www.python.org/) and install it.
3. Open command prompt or PowerShell and type **pip install pyqt5** to add PyQt5 to Python.
4. Still on command prompt or Powershell, type **pip install matplotlib** to add matplotlib to Python.
5. Double-click **start_lrd.pyw**.

### Importing your Goodreads library

1. On Goodreads, go to **My Books** > **Import and Export** > **Export Library**, then download your library export file.
2. On LRD, click on **Import** and select the CSV file you just downloaded.

### Exporting to Excel

1. On Excel, click on **Data** > **From text**.
2. Set **Original data type** to "Delimited" and **File Origin** to "65001: UTF-8". Click next.
3. Check "Comma" on **Delimiters** then click on Finish.
