# contactHoursCounter.py
#
# D. Nekrasz, dnekrasz@bu.edu, Office of Distance Education
# 10/10/2017
#
# This will read a BU ODE course HTML file and count the number of words,
# images, tables (not including tables nested within tables) and test
# yourself objects.
#
# The word counter is very rudimentary, counting literal words of letters,
# numbers or a combination of both, separated by white space.  Knowing that
# other programs have more sophisticated algorithms, I provide an output
# file stripped of all tags, comments and HTML metacharacters that can be
# imported into another program.
#
# Input:  Valid HTML (text) file
#
# Outputs:
#   1.  Four tab-separated integers:  The number of words, images, tables
#       and test yourself objects to stdout
#   2.  Text file of all words separated by a space into file
#       <input filename>.stripped.txt
#
import sys, re

if len(sys.argv) < 2:
    print('Usage: python countImages1.py <inputfile>')
    exit(1)

inputFileName = sys.argv[1].rstrip()



# Debug flag, 0 (false, no debug) or 1 (true, debug)
debug = 0



print('\n\nStarting contactHoursCounter.py', end='')
if debug: print(' in debug mode')
print('\n\n')

# Read input file into string inputData
if debug: print('Reading input file \'' + inputFileName + '\'... ', end='')
with open(inputFileName, 'r') as infile:
    inputData = infile.read()
infile.closed
if debug: print('Done.')



# Strip comments, scripts and HTML metacharacters put result into dataNoComments
if debug: print('Stripping comments and HTML metacharacters... ', end='')
regexFindComments = '(?:(?=<!--)([\s\S]*?)-->)|(?:(?=<script>)([\s\S]*?)<\/script>)|(?:&[a-z0-9]+;)'
dataNoComments = re.sub(regexFindComments, '', inputData)
if debug: print('Done.')



# Count images, store in numImages
if debug: print("Counting images... ", end='')
numImages = 0
regexFindImg = '<img'
numImages = len(re.findall(regexFindImg, dataNoComments, re.IGNORECASE))
if debug: print('Done.\nNumber of images is ' , numImages, '\n')



# Count tables, store in numTables
# First, extract all the <table> and </table> tags with a rudimentary tokenizer
dataTableTags = re.split(r'(<table)|(</table)', dataNoComments, 0, re.IGNORECASE)

# Counts "local" occurences of <table, used to count nested tables
tableCounter = 0

# Overall table count, not including nested tables. Incremented when an
# outer table's (in the case of nested) or single table's </table> tag
# is read
numTables = 0

for line in dataTableTags:
    if line == "<table":
        tableCounter = tableCounter + 1
        if debug: print('New <table> tag encountered, tableCounter = ', tableCounter)
    if line == "</table":
        tableCounter = tableCounter - 1
        if debug: print('</table> tag encountered, tableCounter = ', tableCounter)
        if tableCounter == 0:
            numTables = numTables + 1
            if debug: print('Last </table> tag, numTables = ', numTables)
if debug: print('Done.\nFinal table count: ', numTables, '\n')



# Strip tags into dataNoTags, all empty lines are preserved
if debug: print('Stripping HTML tags... ', end='')
stripTagsRegEx = '(?:(?=<\/?)([\s\S]*?)>)'
dataNoTags = re.sub(stripTagsRegEx, '', dataNoComments, 0, re.IGNORECASE)
if debug: print('Done.')

# Convert all whitespace to a single space to dataJustOneSpace
if debug: print('Cleaning up whitespace... ', end='')
dataJustOneSpace = re.sub(r'\s+', ' ', dataNoTags)
if debug: print('Done.')

# Now write that to the output file <input file>.stripped.txt
print('Writing stripped file to \'' + inputFileName + '.stripped.txt\'... ', end='')
f = open(inputFileName + '.stripped.txt', 'w')
f.write(dataJustOneSpace)
f.close()
if debug: print('Done.')
else: print('\n')



# Count words from dataJustOneSpace
if debug: print('Counting words... ', end='')
numWords = 0
dataWords = dataJustOneSpace.split(" ")

# It is still possible to get a blank space at the beginning and end
# which will increase the word count by two, so get rid of these, and any
# other blank words
for word in dataWords:
    if not word: dataWords.remove(word)

numWords = len(dataWords)
if debug: print('Done.\nNumber of words is ', numWords, '\n')



# Count Test Yourself blocks, store in numTYs
numTYs = 0
if debug: print('Counting Test Yourself blocks... ', end='')
numTYs = 0
regexFindTy = 'class\s*=\s*("testcenter")|("test")'
numTYs = len(re.findall(regexFindTy, dataNoComments, re.IGNORECASE))
if debug: print('Done.\nNumber of Test Yourself blocks is ' , numTYs, '\n')



print('For file \'' + inputFileName + '\':')
print('Words, Images, Tables, Test Yourselves')
print(numWords, numImages, numTables, numTYs, sep='\t', end='\n')
print('\nEnd of contactHoursCounter.py\n\n')