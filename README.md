# File System App
This is a command-line application for working with files. It provides four operations:
* Creating a file with given data
* Deleting a file with given path
* Reading the content of a file
* Retrieving file metadata
# Installation
1. Clone the repository: git clone https://github.com/pantech48/file_system_app
2. Install dependencies: ```pip install -r requirements.txt```
3. Run the program: ```python main.py --help```
# Usage
The program takes command-line arguments to perform different operations on files.

* To create a file, use the --create option followed by the path of the file to be created and the data to write to the file (optional). If no data is provided, an empty file will be created.
Example:

```shell
python main.py --create /path/to/new_file.txt "This is some data to write to the file."
```

* To delete a file, use the --delete option followed by the path of the file to be deleted.
Example:

````shell
python main.py --delete /path/to/file.txt
````
* To read the content of a file, use the --read option followed by the path of the file to be read.
Example:

````shell
python main.py --read /path/to/file.txt
````

* To retrieve the metadata of a file, use the --metadata option followed by the path of the file.
Example:

````shell
python main.py --metadata /path/to/file.txt
````
# Credits
This application was developed by [Yevgeniy Putrin].