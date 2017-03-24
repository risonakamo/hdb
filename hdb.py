import os,sqlite3,random;
from db import db;

validFields=set(["title","type","cover","link","wide"]);

def main():
    d=db("hdb.db");

    while 1:
        command=input(":");
        runCommand(command,d);

def runCommand(command,db):
    command=command.split(" ");

    if command[0]=="s" or command[0]=="search":
        if len(command)<2:
            print("command <tags>");
            return;
        
        tagstart=1;
        randomise=0;
        rstring="";
        if command[1]=="random" or command[1]=="r":
            tagstart=2;
            randomise=1;
            rstring="(random)"

        result=db.getTags(command[tagstart:]);
        writeOutput(result,randomise);
        print("found {} {}".format(len(result),rstring));        
        return;

    if command[0]=="a" or command[0]=="all":
        randomise=0;
        rstring="";
        if len(command)>1 and (command[1]=="random" or command[1]=="r"):
            randomise=1;
            rstring="random";
        
        writeOutput(db.getAll(),randomise);
        print("getting all {}".format(rstring));
        return;

    if command[0]=="o" or command[0]=="output":
        os.system("output.html");
        print("opening output");
        return;

    if command[0]=="tags":
        db.printTagList();
        return;

    if command[0]=="types":
        db.printTypeList();
        return;
    
    if command[0]=="q" or command[0]=="quit" or command[0]=="exit":
        print("quiting");
        quit();        

    if command[0]=="delete":
        if len(command)<2:
            print("delete <id>");
            return;

        db.remove(command[1]);
        print("deleted id {}".format(command[1]));
        return;
        
    if command[0]=="add":
        if len(command)<2:
            print("add <rawfilename>");
            return;

        addRawData(db,command[1]);
        print("adding from file '{}'".format(command[1]));
        return;
        
    if command[0]=="m" or command[0]=="modify":
        if len(command)!=4:
            print("modify <id> <field> <value>");
            return;

        if command[2] not in validFields:
            print("modify <id> <field> <value>");
            print("valid fields:");
            for x in validFields:
                print(x);
            return;
        
        db.updateEntry(command[1],command[2],command[3]);
        print("modifying {}".format(command[1]));
        return;

    if command[0]=="mt" or command[0]=="modifytags":
        if len(command)<3:
            print("modifytags <id> <tag> <tag> <...>");
            return;

        db.updateTags(int(command[1]),command[2:]);
        print("updated tags of {}".format(command[1]));
        return;

    if command[0]=="help":
        os.system("helpdocs\doc.html");
        print("opened help doc");
        return;
    
    print("invalid command");

#not done    
def writeOutput(entries,randomise=0):
    with open("output.html","w+") as ofile:
        htmltop='''
<!doctype html>

<html>

  <head>
    <meta charset="UTF-8">

    <link rel="stylesheet" type="text/css" href="html_resource/style.css">
    <script src="html_resource/main.js"></script>
  </head>
  
  <body>''';

        htmlbot='''
  </body>
  
<html>''';

        ofile.write(htmltop);

        if randomise!=0:
            random.shuffle(entries);
        
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
def parseRawData(filename="rawdata/rawdata"):
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
        if x[0]=="title":
            continue;
        d.add(x[0],x[1],x[2],x[3],x[4],0);
    d.commit();
        
main();
