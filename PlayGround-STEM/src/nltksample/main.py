'''
def getline(line, delimiter=','):
    def _gen():
        while True:
            if delimiter in line:
                yield line[0:line.index(delimiter)]
                break
            else:
                yield line
    return "".join(_gen())
'''
import nltk

infile = "Layout-Media.csv"
outfile = "Revised.csv"
text = ""
f = open(infile,'r')
g = open(outfile, 'w')
while True:
    text = f.readline()
    if len(text) > 10 :
        text = nltk.clean_html(text)
        text = text.split(',')
        if len(text[10]) > 3 :
            new = text[0] + "," + text[1] + "," + text[3] + "," + text[10] + "\n"
            g.write(new)
            #print text[10]
        
    if len(text) == 0:
        break
g.close()
    #text += testline
#text = nltk.clean_html(text)
#print text
