#!/usr/bin/python3

import pandas as pd
import argparse
import sys
import os

__version__ = '0.0.1'

filenameRowSelector = '+r'
filenameColumnSelector = '+c'

# These are the selectors which define the position inside a latex file
# For example the tage mytable would be represented in the latex file as <mytable>
tagStart = '<'
tagEnd = '>'

# The default image width
imageWidth = 0.8

supportedImages = ['.jpg','.png','.jpeg']

# Make a backup of latex files before writing tables to them
writeBackup = True

# Get the directory from where the script is called
dir_path = os.getcwd() + os.sep

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

def printImage(name,relativePath):

    output = None

    outstring = ''
    outstring = outstring + '\\begin{figure}[H]\n'
    outstring = outstring + '\t\\centering\n'
    outstring = outstring + '\t\\captionsetup{justification=centering}\n'
    outstring = outstring + str('\t\\includegraphics[width=%.2f\\linewidth]{%s}\n' % (imageWidth,relativePath))
    outstring = outstring + '\t\\caption{<++>}\n'
    outstring = outstring + str('\t\\label{fig:%s}\n' %(name))
    outstring = outstring + '\\end{figure}\n'
    return outstring

def makeArgs():

    parser = argparse.ArgumentParser(description='latable V{}'.format(__version__),
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t','--target',
            metavar='TARGET',
            type=str,
            nargs='*',
            help='Target file from which to generate latex. Adds all .csv, .jpg, .png and .jpeg files in working directory if not specified.')
    parser.add_argument('-d','--directory',
            type=str,
            nargs=1,
            help='Target directory from where to source csv files. Adds all files from directory recursivly.')
    parser.add_argument('-o','--output',
            type=str,
            nargs=1,
            help='Target output latex file. Generated Latex is placed in specified tag "<filename>" locations.')
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
            for inputFile in options['target']:
                processTag(inputFile,options['output'][0],options['column'],options['row'])

        elif options['directory'] is not None:
            #An output file was given and a source directory for csv
            #Do the same as below, excet get the csvs from specified directory
            for fileName in os.listdir(options['directory'][0]):
                if os.path.splitext(fileName)[1] == '.csv' or os.path.splitext(fileName)[1] in supportedImages:
                    processTag(os.path.join(options['directory'][0],fileName),options['output'][0],options['column'],options['row'])

        else:
            #An output file is given with no target input
            #Search the current directory recursivly for csvs.
            #For each csv found, look for the tag, if tag exists write data there
            for fileName in os.listdir(os.path.dirname(dir_path)):
                if fileName.endswith(".csv") or os.path.splitext(fileName)[1] in supportedImages:
                    processTag(os.path.join(dir_path,fileName),options['output'][0],options['column'],options['row'])

    # Check if an input file was passed
    #Here one file is just printed to stdout, this is good for vim buffer
    elif options['target']is not None:
        for fileName in options['target']:
            if fileName.endswith(".csv"):
                output = processSingle(fileName,options['column'],options['row'])
                if output is not None:
                    print(output)
            elif os.path.splitext(fileName)[1] in supportedImages:
                #Here the output file name is the current directory
                print(processImage(fileName,dir_path))

    # No input file or output file was passed
    # Check if a directory was specified before continuing
    elif options['directory'] is not None:
        # Directory specified.
        # Now find all csv's in the directory and print them to stdout
        for fileName in os.listdir(options['directory'][0]):
            if fileName.endswith(".csv"):
                output = processSingle(os.path.join(options['directory'][0],fileName),options['column'],options['row'])
                if output is not None:
                    print(output)
            elif os.path.splitext(fileName)[1] in supportedImages:
                #Here the output file name is the current directory
                print(processImage(os.path.join(options['directory'][0],fileName),dir_path))

    else:
        #No intput directory, or single file or output file specified
        #Just look for all csvs and print them recursivly to stdout.
        #This forms the default option
        for fileName in os.listdir(dir_path):
            if fileName.endswith(".csv"):
                output = processSingle(fileName,options['column'],options['row'])
                if output is not None:
                    print(output)
            elif os.path.splitext(fileName)[1] in supportedImages:
                #Here the output file name is the current directory
                print(processImage(fileName,dir_path))

    return

def processTag(inputFile,outputFile,useColumn,useRow):

    #Here we need to get the intput file name and look for it as a tag
    #in the output file
    #If the tag is found, then process the input and print it at that location
    #If not foudn then print message to stdout.

    #Modify the selectors to match the filename
    if filenameRowSelector in inputFile:
        useRow = True

    if filenameColumnSelector in inputFile:
        useColumn = False

    #Strip extra comonents of file name to get tag
    tagName = os.path.basename(inputFile)
    tagName = tagName.replace(filenameRowSelector,'')
    tagName = tagName.replace(filenameColumnSelector,'')
    tagName = tagName.replace('.csv','')

    for extension in supportedImages:
        tagName = tagName.replace(extension,'')

    if os.path.splitext(inputFile)[1] == '.csv':
        #Get the table in latex form
        output = processSingle(inputFile,useColumn,useRow)

        # Check a valid table was produced
        if output is None:
            #Problem making table / file doesn' texist
            return None

    elif os.path.splitext(inputFile)[1] in supportedImages:
        output = processImage(inputFile,outputFile)

    else:
        return None

    #Look for the tag in the output file.
    try:
        lines = open(outputFile).read().splitlines()

    except:
        print('Output file: {} doesn not exist'.format(outputFile))
        return None

    lineNumber = None

    for index,line in enumerate(lines):
        if str(tagStart + tagName + tagEnd) in line:
            if writeBackup is True:
                open(outputFile.replace('.tex','') + '_backup' + '.tex','w').write('\n'.join(lines))

            lineNumber = index
            lines[index] = output
            open(outputFile,'w').write('\n'.join(lines))
            break

    #Lines is still equal to none if tag wasn't found
    if lineNumber is None:
        print('Tag "{}" not found in file: {}'.format(tagName,outputFile))

    return lineNumber

def processImage(inputFile,outputFile):

    #Given an input file, detemine the label (tag name)
    #Determine the relative paths between the image and the output file.

    #Replace any possible extension and exteded path to just get label name
    name = os.path.basename(inputFile)
    for extension in supportedImages:
        name = name.replace(extension,'')

    #Get the relave path between two images
    path = os.path.relpath(inputFile,os.path.dirname(outputFile))

    return printImage(name,path)

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
        return None

    name = os.path.basename(name)

    return printTable(data,rows,columns,name,useColumn,useRow);

if __name__ == '__main__':

    #Program eneters and branches from here.
    parser = makeArgs()
    options = vars(parser.parse_args())
    processArgs(options)
