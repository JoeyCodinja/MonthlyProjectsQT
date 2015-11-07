__author__ = 'Danuel'

import sys
import subprocess

if __name__ == "__main__":
    output_file = "ui_.py"

    if sys.argv[1] is not None:
        output_file_workon = output_file.split('.')
        output_file = output_file_workon[0] + sys.argv[1].split('.')[0] + '.' + output_file_workon[1]

    # Calls the pyuic4 module to process the Qt ui file producing a .py file we can use
    if subprocess.call(["pyuic4", '-o', output_file, sys.argv[1]], shell=True):
        print("Success")



