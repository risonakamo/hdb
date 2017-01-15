import os,sqlite3;

class db:
    def __init__(self,dbFilename):
        self.db=sqlite3.connect(dbFilename);
        self.c=self.db.cursor();
        
        self.idc=0;
        self.loadIdCount();

        self.tagListCache=0;
        self.allListCache=0;
        
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
        if self.tagListCache!=0:
            return self.tagListCache;
        
        self.c.execute("select * from tags");
        self.tagListCache=self.c.fetchall();
        return self.tagListCache;
    
    def printAllTags(self):
        tags=self.getAllTags();
        for x in tags:
            print(x);

    def printTagList(self):
        self.c.execute("select distinct tag from tags");
        for x in self.c.fetchall():
            print(x[0]);

    def printTypeList(self):
        self.c.execute("select distinct type from db");
        for x in self.c.fetchall():
            print(x[0]);
            
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

    def updateEntry(self,eid,field,value):
        self.c.execute("update db set '{}'='{}' where id='{}'".format(field,value,eid));
        self.commit();

    #must be array of tags
    def updateTags(self,eid,tags):
        self.c.execute("update db set tags=tags || '{}' where id='{}'".format(","+",".join(tags),eid));
        self.addTags(eid,tags);            
        self.commit();
                
    def remove(self,eid):
        self.c.execute("delete from db where id='{}'".format(eid));
        self.c.execute("delete from tags where id='{}'".format(eid));
        self.commit();
