###
 # <p>Title:  </p>
 # <p>Create Date: 15:09:05 01/10/22</p>
 # <p>Copyright: College of Medicine </p>
 # <p>Organization: University of Florida</p>
 # @author Yonghui Wu
 # @version 1.0
 # <p>Description: </p>
 ##

from RuleEngine import RuleEngine
from TemporalExpression import *

def teFilter(te):
	# Remove concepts start at the same position. Will keep longer one if the same start position
    # Unless expressions are of different types
    
    te_max = {}
    te_available = [0] * len(te)
    for i in range(0, len(te)):
        #print(te[i].text, te[i].start, te[i].end)
        if ( str(te[i].start)) not in te_max:
            te_max[ str(te[i].start)] = [0]*3
            te_max[ str(te[i].start)][0] = te[i].end
            te_max[ str(te[i].start)][1] = i
            te_max[ str(te[i].start)][2] = te[i].value
            te_available[i] = 1
            #print(te_max)
        elif( te[i].end > te_max[ str(te[i].start) ][0]):
            if (te[i].value != te_max[ str(te[i].start) ][2]):
                te_max[ str(te[i].start)] = [0]*3
                te_max[ str(te[i].start)][0] = te[i].end
                te_max[ str(te[i].start)][1] = i
                te_max[ str(te[i].start)][2] = te[i].value
                te_available[i] = 1
            else:
                te_max[ str(te[i].start)][0] = te[i].end
                te_available[te_max[str(te[i].start)][1]] = 0
                te_max[ str(te[i].start)[1]] = i
                te_max[str(te[i].start)][2] = te[i].value
                te_available[i] = 1
	
    new_te = []
    for i in range(0, len(te)):
        if te_available[i] == 1:
            new_te.append(te[i])

    return new_te


def teClean(te):
    new_te = []
    for expr in te:
        data = re.split('\s+', expr.value)
        expr.value = ' '.join(list(data[0:-1]))
        expr.type = data[-1]

        match = expr.text.rfind(expr.value)

        expr.start = expr.start + match#.start()
        expr.end = expr.start + len(expr.value)
       
    
    te_start = {}
    te_available = [0] * len(te)
    
    for i in range(0, len(te)):
        if (te[i].start not in te_start):
            te_start[ te[i].start] = [0]*2
            te_start[ te[i].start][0] = te[i].start
            te_start[ te[i].start][1] = i
            te_available[i] = 1
        else:
            if ((len(te[i].text) < len(te[te_start[te[i].start][1]].text)) & 
                  (te[i].start == te_start[ te[i].start][0])):
                te_available[te_start[te[i].start][1]] = 1
                te_available[i] = 0
            elif ((te[i].start == te_start[ te[i].start][0])): 
                te_available[te_start[te[i].start][1]] = 0
                te_available[i] = 1
    for i in range(0, len(te)):
        if te_available[i] == 1:
            new_te.append(te[i])
	
    return new_te
    

def teFormat(te, csv=False):
    new_te = []
    ct = 1

    if csv == True:
        categories, values = [], []
        for expr in te:
            category, value = expr.type, expr.value
            categories.append(category)
            values.append(value)
        return categories, values
    else:
        for expr in te:
            
            if (expr.value.find(' ')!=-1):
                scores = expr.value.split(' ')
                start = expr.start
                end = expr.end
                for elem in scores:
                    #print(elem)
                    end = start + len(elem)
                    formattedExpr = f"T{ct}\t{expr.type} {start} {end}\t{elem}"
                    start = end + 1
                    ct += 1
                    new_te.append(formattedExpr)
            elif (expr.value.find('//')!=-1):
                scores = expr.value.split('//')
                start = expr.start
                end = expr.end
                for elem in scores:
                    end = start + len(elem)
                    formattedExpr = f"T{ct}\t{expr.type} {start} {end}\t{elem}"
                    start = end + 2
                    ct += 1
                    new_te.append(formattedExpr)
            else:
                formattedExpr = f"T{ct}\t{expr.type} {expr.start} {expr.end}\t{expr.value}"
                new_te.append(formattedExpr)
            ct += 1
            print(formattedExpr)
        
    return new_te


if __name__ == "__main__":
    import sys
    import glob
    import re
    import csv
    import pandas as pd


    ''' 1. input text '''
    my_engine= RuleEngine()
    if not sys.argv[1].endswith('.csv'):
        for file in glob.iglob(f"{sys.argv[1]}/*.txt"):
            
            myf = open(file)
            text=myf.read().lower()#.strip()
            myf.close()
            
            results=my_engine.extract(text)
            #print ("total %s results" % str(len(results))  )
            results = teFilter(results)

            results = teClean(results)

            print ("total %s results after filtering" % str(len(results))  )
            for each in results:
                print(each.type, each.value)

            results = teFormat(results)
            print(results)

            print ("\n\n-----")
            output_filename = file[:-4] + ".ann"
            output_log = open(output_filename, "w")
            try:
                for item in results:
                    output_log.write(item + "\n")
                print(f"Output saved to '{output_filename}'.")
                output_log.close()
            except:
                print(f'No data could be extracted from {file}. Continuing...')
    else:
        df = pd.read_csv(sys.argv[1], header=0, names=['pat_ID', 'note_ID', 'date', 'note_type', 'note_text'])
        for column in ['PPD', 'PY', 'SY', 'QY', 'YQ']:
            df[column] = pd.Series([[] for _ in range(len(df))], dtype=object)

        for idx, row in df.iterrows():
            text = str(row['note_text']).lower().strip()
            try:
                results=my_engine.extract(text)
                print ("total %s results" % str(len(results))  )
                results = teFilter(results)

                results = teClean(results)

                print ("total %s results after filtering" % str(len(results))  )
                
                categories, values = teFormat(results, csv=True)

                for category, value in zip(categories, values):
                    df.loc[idx, category].append(value)

            except:
                continue
        print(f'Saving output file to {str(sys.argv[1])[:-4]}_output_file.csv')
        df.to_csv(f'{str(sys.argv[1])[:-4]}_output_file.tsv', index=False, quoting=csv.QUOTE_ALL, sep='\t')
            
