# Library Rat's Diary

Library Rat's Diary is a program for cataloging your reading history and display statistics and graphs about your book library. 

LRD is meant to replace spreadsheet control for readers who prefer these over an online service like Goodreads or LibraryThing. LRD accepts every user's whims - all fields are optional, even Title.

### About

Library Rat's Diary is my first (useful) Python application. 

Dependencies: matplotlib, pyqt5.

Third party content: [Oxygen icon set](https://github.com/KDE/oxygen-icons5).

### Running from source code (beginner-friendly step-by-step)

Windows:

1. Download LRD by clicking on **Code** > **Download ZIP** near the top of this page and extract the ZIP.
2. Download Python 3.7 or better from [python.org](https://www.python.org/) and install it.
3. Open command prompt or PowerShell and type **pip install pyqt5** to add PyQt5 to Python.
4. Still on command prompt or PowerShell, type **pip install matplotlib** to add matplotlib to Python.
5. Double-click **start_lrd.pyw**.

Linux:

1. Download LRD by clicking on **Code** > **Download ZIP** near the top of this page and extract the ZIP.
2. Most distros come with Python3 pre-installed, but if you don't have it, install Python 3.7 or better.
3. Open terminal and type **pip3 install pyqt5** to add PyQt5 to Python.

3b. Was pip3 not found? Try **sudo apt-get python3-pip** (or equivalent command for your package manager) to install pip3.
4. Still on terminal, type **pip3 install matplotlib** to add matplotlib to Python.
5. Go to the folder where **start_lrd.pyw** is, open in terminal and type **python3 start_lrd.pyw**.

### Importing your Goodreads library

1. On Goodreads, go to **My Books** > **Import and Export** > **Export Library**, then download your library export file.
2. On LRD, click on **Import** and select the CSV file you just downloaded.

### Exporting to Excel

1. On Excel, click on **Data** > **From text**.
2. Set **Original data type** to "Delimited" and **File Origin** to "65001: UTF-8". Click next.
3. Check "Comma" on **Delimiters** then click on Finish.
