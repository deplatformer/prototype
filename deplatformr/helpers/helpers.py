import os
from zipfile import ZipFile

def unzip(zip_file):

    try:
        # Get root name of zip file, use as directory name
        contents_dir = os.path.splitext(zip_file)
        # Create a ZipFile Object
        with ZipFile(zip_file, 'r') as unzip_dir:
            # Extract all the contents of zip file in FB directory
            unzip_dir.extractall(contents_dir[0])
        # Get absolute path of the FB directory
        abs_unzip_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), contents_dir[0])

        return (abs_unzip_dir)

    except Exception as e:
        print ("Not a valid zip file or location.")
        print(e)
