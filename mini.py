#!/usr/bin/env python

"""
Notes: Better Support as a module
Abstract classes better, creative service class, do not abuse the constructor, create klass to execute stuff.
"""

import os, sys, re

class glob():

    """
        Scan files in current dir and minify them
    """

    def __init__(self):

        self.glob_list = [] # set list for files to minify

        for fname in os.listdir('.'):
            if fname.endswith('.js') or fname.endswith('.css'):
                self.glob_list.append(fname)

        print('Found following files in your current directory:')
        print(self.glob_list)

        print('Minifying of these has begun.')
        glob = minify(self.glob_list, 0)

class concat():

    """
        Minify and concat files
    """

    def __init__(self, file_to_concat):

        concat = minify(file_to_concat, 2) # initiate minify class
        self.files_to_concat = [] # set list for files to concat

        print('')
        print('Minifying done. Concatenating has begun.')

        """ check if at least 2 files has been set as argument """
        if len(sys.argv) > 3:
            """ if file or sys.argv has not been inputted """
            if(file_to_concat == 'help'):
                concat.help()
                sys.exit()
            else:
                for i in range(2, len(file_to_concat)):
                    self.file_to_concat = file_to_concat[i]
                    self.file_name = os.path.splitext(self.file_to_concat)
                    self.file_name_minified = self.file_name[0] + '.min' + self.file_name[1]

                    self.files_to_concat.append(self.file_name_minified)

            self.execute_concatenation()
        else:
            print('')
            print('Concat has failed. Set at least two files as argument to concat.')
            concat.help()
            sys.exit()

    """ execute concatenation for minified files """
    def execute_concatenation(self):

        if self.file_name[1] == '.css':
            print('')
            print('CSS files detected. Creating concat.css.')
            self.concat_file = 'concat.css'
        elif self.file_name[1] == '.js':
            print('')
            print('JS files detected. Creating concat.js.')
            self.concat_file = 'concat.js'

        """ write the concat file """
        with open(self.concat_file, 'w+') as outfile:
            for fname in self.files_to_concat:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

class minify():

    """
        Minify files
    """

    def __init__(self, file_to_minify, range_from_argument):

        """ if file or sys.argv has not been inputted """
        if(file_to_minify == 'help'):
            self.help()
            sys.exit()
        else:
            for i in range(range_from_argument, len(file_to_minify)):
                self.file_to_minify = file_to_minify[i]
                self.file_name = os.path.splitext(self.file_to_minify)
                self.file_name_minified = self.file_name[0] + '.min' + self.file_name[1]

                self.detect_file_type_and_execute()

    """ detect file type and execute """
    def detect_file_type_and_execute(self):
        if self.file_name[1] == '.css':
            print('')
            print('CSS file detected.')
            self.css() # run css compression
            self.size_calc() # calc size difference
        elif self.file_name[1] == '.js':
            print('')
            print('JS file detected.')
            self.js() # run js compression
            self.size_calc() # calc size difference
        else:
            self.help()

    """ read file """
    def read_file(self, filepath):
        try:
            f = open(filepath, 'r')
        except:
            self.help()
            sys.exit()
        finally:
            return f.read()
            f.close()

    """ write minified version to file """
    def write_file(self, filepath):
        try:
            f = open(self.file_name_minified, 'w+')
        except:
            self.help()
            sys.exit()
        finally:
            f.write(filepath)
            f.close()

    """ calculate size difference """
    def size_calc(self):
        self.file_size = os.path.getsize(self.file_to_minify)
        self.file_size_minified = os.path.getsize(self.file_name_minified)
        self.file_size_saved = self.file_size - self.file_size_minified
        self.file_size_saved_in_percentage = (100 * float(self.file_size_minified) / float(self.file_size)) - 100

        print('Done - take a look at ' + self.file_name_minified)
        print('You have saved ' + str(self.file_size_saved) + ' bytes (' + str(self.file_size_saved_in_percentage) + '%)')

    """ help instructions """
    def help(self):
        print('')
        print('Instructions')
        print('Make sure that:')
        print('1): You are trying to compress a css or js file.')
        print('2): The file exists in your current folder.')
        print('3): You have not misspelled.')
        print('Use like $ python mini.py [-m|--minify,-c|--concat,-s|--scan-dir] [files]')
        print('Concat needs more than file as argument, to concat... obviously.')
        print('...')
        print('')

    """ css minifying """
    def css(self):
        self.string = self.read_file(self.file_to_minify)
        self.strip_comments  = re.sub(r'/\*[\s\S]*?\*/', '', self.string)
        self.strip_urls = re.sub(r'url\((["\'])([^)]*)\1\)', r'url(\2)', self.strip_comments)
        self.strip_whitespace_and_linebreaks = self.strip_urls.replace('\n', '').replace(' ', '')

        self.write_file(self.strip_whitespace_and_linebreaks) # write minified css to file

    """ js minifying """
    def js(self):
        self.string = self.read_file(self.file_to_minify)
        self.strip_comments  = re.sub(r'/\*[\s\S]*?\*/', '', self.string)
        self.strip_one_line_comments = re.sub(r'\/\/(.*)', '', self.strip_comments)
        self.strip_whitespace_and_linebreaks = self.strip_one_line_comments.replace('\n', '').replace(' ', '')

        self.write_file(self.strip_whitespace_and_linebreaks) # write minified js to file

""" run script """
if __name__ == '__main__':

    if len(sys.argv) > 1:
        if (sys.argv[1] == '-m') or (sys.argv[1] == '--minify') :
            mini = minify(sys.argv, 2)
        elif (sys.argv[1] == '-c') or (sys.argv[1] == '--concat'):
            con = concat(sys.argv)
        elif (sys.argv[1] == '-s') or (sys.argv[1] == '--scan-dir'):
            glob = glob()
    else:
        mini = minify('help')
