### HUFFMAN COMPRESSION

This compression algorithm is based on the fact that not every message could use
every character of ascii codes. There we create our own binary encoding messages
with higher frequincies of characters will use lesser bits of memory.

##### FEATURES

* Makes the size of any text file smaller based on its frequencies.
* No loss of data.
* Easy to use.
* Ability to encode and decode data fastly.

##### USAGE

* Copy the file you wish to encode, in the python script directory.
* From terminal or command prompt, type `python encode.py -e <file_name.txt>`
* This will save the compressed file in the directory of python script.
* A `key` file will be created which will be used for decoding purposes.
* To decode type `python decode.py -d <compressed_file.bin> <key_file.txt>`.

##### USES

Compression has tons of uses everywhere.

* Can be used for faster sending of text files over internet.
* Saves space on disk.
* Can also be used as a security measure to protect your files.


##### Note
This will only work on `python 2.7.x`. `python 3` is not supported at the time of writing.

