This is an update of [https://code.google.com/archive/p/goofile/](https://code.google.com/archive/p/goofile/) for Python 3, with the addition of a setup.py file for easy pip installation.

To install, download or clone repository:

    git clone https://github.com/sosukeinu/goofile.git goofile
    
then `cd` into the resulting directory

    cd goofile
    
then, install using pip

    pip install .
    
You can then run the script from anywhere on your system using:

    goofile -d {domain to search} -f {filetype, i.e. pdf}
    
for example

    goofile -d kali.org -f pdf
