import pandas as pd


def printTable(data,rows,columns,title):

    columnSelector = ' '.join(['l' for i in range(columns)])

    print('\\begin{table}[H]')
    print('\t\\centering')
    print('\t\\begin{tabular}{',columnSelector,'}')
    print('\t\t\\hline')

    #Make the header
    print('\t\t' + ' & '.join( ['\\textbf{' + str(header)  + '}' for header in data.columns]) + '\\\\')
    print('\t\t\\hline')

    for i in data.index:

        print('\t\t' + ' & '.join( [str(item) for item in data.iloc[i,:]]) + '\\\\')
    
    print('\t\t\\hline')
    print('\t\\end{tabular}')


    print('\t\\caption{<++>}')
    print('\t\\label{tab:' + title + '}')
    print('\end{table}')

if __name__ == '__main__':

    data = pd.read_csv('data.csv')
    printTable(data,len(data.index),len(data.columns),'data');
