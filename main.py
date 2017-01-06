import os,sqlite3;

class db:
    def __init__(self,dbFilename):
        self.db=sqlite3.connect(dbFilename);
        self.c=self.db.cursor();
        
        self.idc=0;
        self.loadIdCount();
        
        self.c.execute('''
        create table if not exists db (
        id int,
        title text,
        type text,
        cover text,
        link text,
        tags text,
        wide int)''');

        self.c.execute('''create table if not exists tags (id int,tag text)''');
        self.db.commit();

    def loadIdCount(self):
        if not os.path.exists("idcount"):
            print("creating idcount");
            with open("idcount","w+") as ic:
                ic.write("0");
            return;

        with open("idcount","r") as ic:
            self.idc=int(ic.read());            
        
    def add(self,title="",ttype="",cover="",link="",tags="",wide=0):
        self.idc+=1;
        self.c.execute('''insert into db values("{}","{}","{}","{}","{}","{}","{}")'''.format(self.idc,title,ttype,cover,link,tags,wide));

    def commit(self):
        with open("idcount","w") as ic:
            ic.write(str(self.idc));            
        self.db.commit();
        
    def getAll(self):
        self.c.execute('''select * from db''');
        return self.c.fetchall();

    def getType(self,ttype):
        self.c.execute('''select * from db where type="{}"'''.format(ttype));
        return self.c.fetchall();

    def printTableAll(self):
        table=self.getAll();            
        for x in table:
            print(x);

def main():
    d=db("sample.db");
    # d.add("bob2","type1","img2","link2.com","bill,pop",0);
    # d.commit();
    d.printTableAll();

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
            ofile.write(genEntryBox(x[1],x[2],x[5],x[3],x[4],x[6]));

        ofile.write(htmlbot);

def genEntryBox(title,ttype,tags,cover,link,wide=0):
    if wide!=0:
        wide='class="wide" ';
    else:
        wide="";
        
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
    
def parseRawData():
    data=[];
    entry=[];
    with open("rawdata") as ifile:        
        for l in ifile:            
            l=l[:-1];
            if l=="---":
                entry.append(0); #wide value maybe change later
                data.append(entry);                
                entry=[];
                continue;
            entry.append(l);            
        
    return data;

main();
