"""Class to decode the encoded file. To Decode a file, the meta data, i.e
   data containing, alphabets representation is required.
"""

from binary_tree import binary
import argparse 

class decode:

    def __init__(self):
        """constructor for decode class.
           
           self.meta : binary_tree.binary object
           self.string = string, contents of the file
        """

        #get arguemtns from terminal
        self.args = self.get_argument()
        self.file_name = self.args[0]
        self.meta_file_name = self.args[1]

        self.meta = self._make_decode_tree(self._load_meta(self.meta_file_name))
        self.binary_bits = self._read_from_file(self.file_name)

   
    def get_argument(self):
        ap = argparse.ArgumentParser()
        ap.add_argument('-d', nargs = 2, required = True, help = '-d <_compressed_file_name> <key_file>')
        args = ap.parse_args()
        return args.d


    def _get_bits(self, f):
        """Utility fucntion to get individual bits from a byte"""

        #we store teh number represented by the binary digits in teh file,
        #in byte. Then we extract each bit using the right shift operator.

        byte = (ord(x) for x in f.read())
        for x in byte:
            for i in xrange(8):
                yield (x >> i) & 1

    
    def _read_from_file(self, file_name):
        
        """Read encoded data from file and return string
        """

        string = ''
        for x in self._get_bits(open(file_name, 'r')):
            string += str(x)
        
        return string


    def _load_meta(self, meta_file_name):
        #load key file and extract the contents to a list

        with open(meta_file_name) as f:
            lines = f.read()

        lines.strip('\t')
        meta = lines.strip('\t').split('\t')
        return meta

    def _create_original_file(self, string):
        """Creates the file which contains the decoded content,
           i.e original content
        """

        with open('original_' + self.file_name[:-4] + '.txt', 'wb') as f:
            f.write(string)


    def _make_decode_tree(self, meta):
        """
        meta : list, contains key at even index and decoding value at odd index.
        """

        tree = binary()
        for x in xrange(0, len(meta) - 1, 2):
            temp = tree

            for decode in meta[x+1]:
                if decode == '1':
                    if temp.right == None:
                        temp.right = binary()
                        temp = temp.right

                    else:
                        temp = temp.right

                elif decode == '0':
                    if temp.left == None:
                        temp.left = binary()
                        temp = temp.left

                    else:
                        temp = temp.left

            temp.key = meta[x]
        return tree


    def decode(self):
        """Method to convert compressed data back into its original form"""

        original = ''
        temp = self.meta
        length = len(self.binary_bits)
        index = 0

        while index < length:
            if temp.key != None:
                original += temp.key
                temp = self.meta
                continue

            if self.binary_bits[index] == '1':
                temp = temp.right

            else:
                temp = temp.left
        
            index += 1

        self._create_original_file(original)

if __name__ == '__main__':
    ob = decode()
    ob.decode()
