#!/usr/bin/python

# takes a relion partcles file and remakes the coordinate files for it, allowing you to back trace where the particles that went into a reconstruction came from
# in the individual micrographs

#to use:
# run on a relion particles file
# start a manual pick job
# copy all of the _backtrace.star files into the manual pick job's directory
# use the file_rename utility to replace _backtrace with _manualpick
# use teh manual pick gui to look at the results


import sys
vers = '0.2'
###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i and '#' in i:
            labelsdic[i.split('#')[0]] = labcount
            labcount+=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

try:
    (labels,header,data) = read_starfile(sys.argv[1])
except:
    sys.exit('''USAGE: rln-parts-trace <rln data starfile>

%% Relion particle backtrace - Version {0}
%% INSTRUCTIONS
%% run the script on a relion particles file
%% start a manual pick job, make sure to add "--pickname (backtrace)" in the additional arguments box
%% manually pick a point on one micrograph and save the results so relion creates the directory structure
%% copy all of the _backtrace.star files into the manual pick job's directory
%% continue the manual pick job to see the reults'''.format(vers))


header = '''data_

loop_ 
_rlnCoordinateX #1 
_rlnCoordinateY #2 
'''

micrographs = {}
for i in data:
    print i[labels['_rlnMicrographName ']]
    if i[labels['_rlnMicrographName ']] not in micrographs:
        micrographs[i[labels['_rlnMicrographName ']]] = []
    micrographs[i[labels['_rlnMicrographName ']]].append((i[labels['_rlnCoordinateX ']],i[labels['_rlnCoordinateY ']]))
        
#print micrographs

for i in micrographs:
    filename = i.split('/')[-1].split('.')[0]
    outfile = open('{0}_backtrace.star'.format(filename),'w')
    outfile.write(header)
    for coordpair in micrographs[i]:
        outfile.write('{0}  {1}\n'.format(coordpair[0],coordpair[1]))
    outfile.close()



