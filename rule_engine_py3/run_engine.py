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
            #print(te_max)
	
    new_te = []
    for i in range(0, len(te)):
        if te_available[i] == 1:
            new_te.append(te[i])
	
    return new_te

def OGteFilter(te):
	# Remove concepts start at the same position. Will keep longer one if the same start position
    # ORIGINAL VERSION
	te_max = {}
	te_available = [0] * len(te)
	for i in range(0, len(te)):
		if ( str(te[i].start)) not in te_max:
			te_max[ str(te[i].start)] = [0]*2
			te_max[ str(te[i].start)][0] = te[i].end
			te_max[ str(te[i].start)][1] = i
			te_available[i] = 1
		elif te[i].end > te_max[ str(te[i].start) ][0]:
			te_max[ str(te[i].start)][0] = te[i].end
			te_available[te_max[str(te[i].start)][1]] = 0
			te_max[str(te[i].start)][1] = i
			te_available[i] = 1
	
	new_te = []
	for i in range(0, len(te)):
		if te_available[i] == 1:
			new_te.append(te[i])
	
	return new_te

def teFormat(te):
    new_te = []
    ct = 1
    for expr in te:
        data = re.split('\s+', expr.value)
        if (len(data) < 2):
            placehold_value = data.pop(0)
            if (placehold_value[-3:]!='PPD'):
                stop = -2
            else:
                stop = -3
            expr.type = placehold_value[stop:]
            expr.value = placehold_value[0:stop]
        elif   (len(data) > 2):
            expr.type = data[-1]
            expr.value = ' '.join(str(item) for item in data[:-1])
        else:
            if (data[0] == ''):
                split = int(len(data[1])/2)
                placehold_data = data.pop(1)
                expr.type = placehold_data[split:]
                expr.value = placehold_data[0:split]
            else:
                expr.type = data[-1]
                expr.value = data[0]
        match = re.search(expr.value, expr.text) 
        formattedExpr = f"T{ct}\t{expr.type} { expr.start + match.start() }  { expr.start + match.end() }\t{expr.value}"
        ct += 1
        new_te.append(formattedExpr)
    
    return new_te

if __name__ == "__main__":
    import sys
    import glob
    import re

    ''' 1. input text '''

    my_engine= RuleEngine()
    for file in glob.iglob(f"{sys.argv[1]}/*.txt"):
        myf = open(file)
        text=myf.read() #Removed .strip() 
        myf.close()
        results=my_engine.extract(text)
        print ("total %s results" % str(len(results))  )
        
        results = teFilter(results)

        print ("total %s results after filtering" % str(len(results))  )

        results = teFormat(results)

        print ("\n\n-----")
        output_filename = file[:-4] + ".ann"
        output_log = open(output_filename, "w")

        for item in results:
            print (item)
            output_log.write(item + "\n")
        print(f"Output saved to '{output_filename}'.")
        output_log.close()