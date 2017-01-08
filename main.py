import os,sqlite3;
from db import db;

def main():
    d=db("sample.db");
    # d.add("bob2","type1","img2","link2.com","bill,pop",0);
    # d.commit();
    addRawData(d,"rawdata");
    writeOutput(d.getAll());
    # d.printAllTags();
    # d.dexecute("select db.* from tags,db where (tags.tag in ('anal','loli','cg')) and (tags.id=db.id) group by db.id having count(db.id)=3");


#not done    
def writeOutput(entries):
    with open("output.html","w+") as ofile:
        htmltop='''
<!doctype html>

<html>

  <head>
    <meta charset="UTF-8">

    <link rel="stylesheet" type="text/css" href="style.css">
    <script src="main.js"></script>
  </head>
  
  <body>''';

        htmlbot='''
  </body>
  
<html>''';

        ofile.write(htmltop);

        for x in entries:
            ofile.write(genEntryBox(x[1],x[2],x[5],x[3],x[4],x[0],x[6]));

        ofile.write(htmlbot);

def genEntryBox(title,ttype,tags,cover,link,eid,wide=0):
    if wide!=0:
        wide='class="wide" ';
    else:
        wide="";

    ttype=ttype+" "+str(eid);
        
    html='''
<a href="{}">
  <div class="entry-box">
    <div class="img-box">
      <img {}src="{}">
    </div>
    
    <div class="info-box">
      <p class="tags">{}</p>
      <p class="title">{}</p>
      <p class="type">{}</p>
    </div>
  </div>
</a>'''.format(link,wide,cover,tags,title,ttype);
    return html;

#read rawdata file and return data array
def parseRawData(filename="rawdata"):
    data=[];
    entry=[];
    with open(filename) as ifile:        
        for l in ifile:            
            if l[-1]=="\n":
                l=l[:-1];
            if l=="---":
                entry.append(0); #wide value maybe change later
                data.append(entry);                
                entry=[];
                continue;
            entry.append(l);            
        
    return data;

#read rawdata and add to database
def addRawData(d,filename="rawdata"):
    data=parseRawData(filename);
    for i,x in enumerate(data):
        if i==0:
            continue;
        d.add(x[0],x[1],x[2],x[3],x[4],0);
    d.commit();
        
main();
