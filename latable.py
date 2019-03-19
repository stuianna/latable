import pandas as pd
import argparse
import sys
import os

__version__ = '0.0.1'

filenameRowSelector = '+r'
filenameColumnSelector = '+c'

#Get the working directory for either a frozen app or dev app
if getattr(sys, 'frozen', False):
    #Set the path to the directory where the executable is located
    dir_path = os.path.dirname(sys.executable) + os.sep
else:
    dir_path = os.path.dirname(os.path.abspath(__file__)) + os.sep

def printTable(data,rows,columns,title,useCol,useRow):

    #This is the juicy part.
    #Make a latex table from the passed dataframe.

    # Determine how many columns there are
    if useRow:
        columnSelector = 'l | '  + ' '.join(['l' for i in range(columns)])
    else:
        columnSelector = ' '.join(['l' for i in range(columns)])

    outString = ''

    #Print the table 'header'
    outString = outString + '\\begin{table}[H]' + '\n'
    outString = outString + '\t\\centering' + '\n'
    outString = outString + '\t\\begin{tabular}{' + str(columnSelector) + '}' + '\n'
    outString = outString + '\t\t\\hline' + '\n'

    #Make the header 
    if useCol and not useRow:
        outString = outString + '\t\t' + ' & '.join( ['\\textbf{' + str(header)  + '}' for header in data.columns]) + '\\\\' + '\n'
        outString = outString + '\t\t\\hline' + '\n'

    elif useCol and useRow:
        outString = outString + '\t\t' + '\\textbf{' + str(data.index.name) + '} & ' + ' & '.join( ['\\textbf{' + str(header)  + '}' for header in data.columns]) + '\\\\' + '\n'
        outString = outString + '\t\t\\hline' + '\n'

    # No row names in as header
    if not useRow:
        for i in data.index:
            outString = outString + '\t\t' + ' & '.join( [str(item) for item in data.iloc[i,:]]) + '\\\\' + '\n'

    #Using row names as headers
    else:
        for index,value in enumerate(data.index):
            
            outString = outString + '\t\t' + '\\textbf{' + str(value) + '} & ' + ' & '.join( [str(item) for item in data.iloc[index,:]]) + '\\\\' + '\n'

    
    outString = outString + '\t\t\\hline' + '\n'
    outString = outString + '\t\\end{tabular}' + '\n'


    outString = outString + '\t\\caption{<++>}' + '\n'
    outString = outString + '\t\\label{tab:' + title + '}' + '\n'
    outString = outString + '\end{table}' + '\n'
    return outString


def makeArgs():

    parser = argparse.ArgumentParser(description='latable V{}'.format(__version__),
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t','--target',
            metavar='TARGET',
            type=str,
            nargs='*',
            help='Target file from which to generate a table. Adds all csv files in working directory if not specified.')
    parser.add_argument('-d','--directory',
            type=str,
            nargs=1,
            help='Target directory from where to source csv files. Adds all files from directory recursivly.')
    parser.add_argument('-o','--output',
            type=str,
            nargs=1,
            help='Target output latex file. Generated tables are placed in specified tag "<filename>" locations.')
    parser.add_argument('-c','--column',
            action='store_false',
            default=True,
            help='Column headings are located in first row of csv. (Default = True)')
    parser.add_argument('-r','--row',
            action='store_true',
            default=False,
            help='Row headings are located in first columns of csv. (Default = False)')
    parser.add_argument('-v','--version',action='version',
            version='latable V{}'.format(__version__),help='Display program version')
    return parser

def openCSV(fileName,useColumn,useRow):

    #This function opens a csv file based on the passed usecolum and userow
        #useCoumns -> The row contains the columns heading
        #useRows -> The first column contains the row headinds.
    try:
        if useColumn and not useRow:
            data = pd.read_csv(fileName)
        elif useColumn and useRow:
            data = pd.read_csv(fileName,index_col=0)
        elif not useColumn and useRow:
            data = pd.read_csv(fileName,header=None,index_col=0)
        elif not useColumn and not useRow:
            data = pd.read_csv(fileName,header=None)
        else:
            #Shouldn't get here
            return None,None,None,None
    except:
        print('File: {} does not exist.'.format(fileName))
        return None,None,None,None

    fileName = fileName.replace(filenameRowSelector,'')
    fileName = fileName.replace(filenameColumnSelector,'')
    fileName = fileName.replace('.csv','')

    return data,len(data.index),len(data.columns),fileName

def processArgs(options):

    # Check if an output file was specified
    if options['output'] is not None:
        if options['target']is not None:
            #A target file and an output file was given
            #Search for the tag with name of input file in output file
            #If the tag exists, write the output in that location
            #If tag doesn't exist print error
            pass

        elif options['directory'] is not None:
            #An output file was given and a source directory for csv
            #Do the same as below, excet get the csvs from specified directory
            pass

        else:
            #An output file is given with no target input
            #Search the current directory recursivly for csvs.
            #For each csv found, look for the tag, if tag exists write data there
            pass

    # Check if an input file was passed
    #Here one file is just printed to stdout, this is good for vim buffer
    elif options['target']is not None:
        for inputFile in options['target']:
            output = processSingle(inputFile,options['column'],options['row'])
            if output is not None:
                print(output)

    # No input file or output file was passed
    # Check if a directory was specified before continuing
    elif options['directory'] is not None:
        # Directory specified.
        # Now find all csv's in the directory and print them to stdout
        for fileName in os.listdir(os.path.dirname(options['directory'][0])):
            if fileName.endswith(".csv"):
                output = processSingle(os.path.join(options['directory'][0],fileName),options['column'],options['row'])
                if output is not None:
                    print(output)
        pass

    else:
        #No intput directory, or single file or output file specified
        #Just look for all csvs and print them recursivly to stdout.
        #This forms the default option
        for fileName in os.listdir(dir_path):
            if fileName.endswith(".csv"):
                output = processSingle(fileName,options['column'],options['row'])
                if output is not None:
                    print(output)




    return

def processTag(inputFile,outputFile,useColumn,useRow):

    #Here we need to get the intput file name and look for it as a tag
    #in the output file
    #If the tag is found, then process the input and print it at that location
    #If not foudn then print message to stdout.


    return

def processSingle(inputFile,useColumn,useRow):

    #In this function a single input file is taken, opened and read
    #File name arguments and command line arguments are processed here
    #The resulting found table is return as a single string variable.

    if filenameRowSelector in inputFile:
        useRow = True

    if filenameColumnSelector in inputFile:
        useColumn = False

    data,rows,columns,name = openCSV(inputFile,useColumn,useRow)

    if data is None:
        return

    return printTable(data,rows,columns,name,useColumn,useRow);

if __name__ == '__main__':

    #Program eneters and branches from here.

    parser = makeArgs()
    options = vars(parser.parse_args())
    processArgs(options)
