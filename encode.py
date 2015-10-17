"""class to encode data into smaller bits according to their 
   frequinces of occurance.
"""

from binary_tree import binary
from operator import itemgetter
import argparse 


class encode:

    def __init__(self):
        """Constructor for encode class.

        input
        =====
        file_name : str, file whose message is to be encoded

        """
        
        
        self.args = self.get_argument()
        self.file_name = self.args[0]
        #get frequency of each charater and sort it in descending order
        #and save it in a list.

        self.string = self._get_string(self.file_name)
        self.freq = self._sort(self._frequency(self.string))


    def get_argument(self):
        ap = argparse.ArgumentParser()
        ap.add_argument('-e', nargs = 1, required = True, help = '-c <file_name>')
        args = ap.parse_args()
        return args.e


    def _get_string(self, file_name):
        with open(file_name) as f:
            string = f.readline()

        return string


    def _merge(self, tree1, tree2):
        """Utility function to merge two trees into one

        input
        =====
        tree1, tree2: binary_tree.Binary, binary tree object

        """

        temp = binary()
        temp.value = tree1.value + tree2.value
        temp.left = tree1
        temp.right = tree2
        return temp


    def _frequency(self, string):
        #creates dictionary to calculate frequincy of characters

        values = {}
        for alphabet in string:
            if alphabet in values:
                values[alphabet] += 1

            else:
                values[alphabet] = 1

        freq = []
        for key,values in values.iteritems():
            freq.append((key,values))

        return freq


    def _sort(self, freq):
        return sorted(freq, key = itemgetter(1))

    
    def _make_tree(self):
        #Create single node trees in desceding order stored in list
        trees = []
        for x in self.freq:
            trees.append(binary(value = x[1], key = x[0]))

        #return descending order list
        return trees[::-1]   


    def _combine(self):
        """Combines the single node trees into one, for encoding and decoding a
           a string
        """

        #TODO
        #not the best way, priority queue or heap will make the algo more
        #efficient

        trees = self._make_tree()
        while len(trees) > 1:
            new_tree = self._merge(trees.pop(), trees.pop())

            #start checking in desceding order
            #max comparision, 26 letters of alphabetes, or more if special characters
            #included. Insert new tree according to its place

            length = len(trees)
            for i in xrange(length):
                if trees[i].value <= new_tree.value:
                    trees.insert(i, new_tree)
                    break

                if i == length - 1:
                    trees.insert(i, new_tree)

        #new_tree is the final tree with the total count as node
        return new_tree 


    def _path_leaf(self, tree, path):
        """Find paths of leaf nodes in a combination of 0 and 1. 0 represents left node
           and 1 right node. This essentially creates a meta data for encoding and de-
           coding purposes

           Input
           =====
            tree : binary_tree.binary
            path : string, path of a leaf node

        """

        #This function finds all the leaf paths in the tree, represented by a 0 or a 1.
        #0 represents a left node and 1 represents a right node. The node with the higest
        #value have the least length of the path. 
        #We visit all the paths using a recursive function and store all the paths in a 
        #list with appropriate keys. Thus these paths will serve as a table or metadata
        #for encoding.

        if type(tree.key) == str:
            return [tree.key, ''.join(path)]

        left = self._path_leaf(tree.left, path+'0')
        right = self._path_leaf(tree.right, path+'1')

        ans = []
        ans.extend(left)
        ans.extend(right)
        
        return ans

    
    def _create_dict(self, ans):
        temp_dict = {}
        for x in xrange(0,len(ans),2):
            temp_dict[ans[x]] = ans[x+1]

        return temp_dict


    def _encode_to_file(self, meta):
        """This method encodes each byte as per our meta data and string(file)
           and saves in a file
           
           input
           =====
           meta : dict, contains the frequencies of each character
        """

        from array import array

        #get the 0s and 1s of all the characters and fit them in a byte.
        #Each byte can at utmost contain 8 bits. If a byte ends in half,
        #we continue it in the next byte.

        bin_array = array('B')
        f = file('compressed_'+self.file_name[:-4]+'.bin', 'wb')

        binary_bits = ''

        for character in self.string:
            binary_bits += meta[character]

        size = len(binary_bits)

        #we have to make sure the size of whole string is a multiple of 8
        #if its not, we add 0 to fill the byte

        if len(binary_bits) % 8 == 0:
            pass

        else:
            binary_bits += '0' * ((len(binary_bits) / 8 * 8) + 8 - len(binary_bits))
        
        #write it to a file
        for x in xrange(0, len(binary_bits), 8):
            bin_array.append(int(binary_bits[x:x+8][::-1], 2))

        bin_array.tofile(f)
        f.close()


    def _create_meta(self, meta):
        """Creates meta data(key) for decoding purpose"""

        #'\t' is the delimeter for spliting the list.
        f = file(self.file_name[:-4] + '_key.txt', 'wb')

        for key in meta.keys():
            f.write(key+'\t')
            f.write(meta[key]+'\t')

        f.close()    


    def compress(self):
        """Method to compress data using binary tree created. Creates two files.
           One that contains the compressed data, other the key for extracting the
           data.
        """

        tree = self._combine()
        meta = self._create_dict(self._path_leaf(tree, ''))

        #create compressed file
        self._encode_to_file(meta)  

        #create key file
        self._create_meta(meta)


if __name__ == '__main__':
    x = encode()
    x.compress()

            
