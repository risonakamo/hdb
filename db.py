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
            if self.idc=="":
                self.idc=0;
        
    def add(self,title="",ttype="",cover="",link="",tags="",wide=0):
        self.idc+=1;
        self.c.execute('''insert into db values("{}","{}","{}","{}","{}","{}","{}")'''.format(self.idc,title,ttype,cover,link,tags,wide));
        tags=tags.split(",");
        tags.append(ttype);
        self.addTags(self.idc,tags);

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

    def getAllTags(self):
        self.c.execute("select * from tags");
        return self.c.fetchall();
    
    def printAllTags(self):
        tags=self.getAllTags();
        for x in tags:
            print(x);
            
    def addTags(self,idc,tags):
        command="insert into tags values ";
        for x in tags:
            command+='("{}","{}"),'.format(idc,x);

        command=command[:-1];
        self.c.execute(command);

    def dexecute(self,command):
        self.c.execute(command);
        for x in self.c.fetchall():
            print(x);

    #tags must be array of strings
    def getTags(self,tags):
        tcount=len(tags);
        tagstring="";
        for x in tags:
            tagstring+="'"+x+"',";

        tagstring=tagstring[:-1];
        self.c.execute("select db.* from tags,db where (tags.tag in ({})) and (tags.id=db.id) group by db.id having count(db.id)={}".format(tagstring,tcount));
        return self.c.fetchall();
