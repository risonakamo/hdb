import os,sqlite3;

class db:
    def __init__(self,dbFilename):
        self.db=sqlite3.connect(dbFilename);
        self.c=self.db.cursor();
        
        self.idc=0;
        self.loadIdCount();
        
        self.c.execute('''create table if not exists db (id int,title text,type text,cover text,link text)''');
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
        
    def add(self,title="<>",ttype="<>",cover="<>",link="<>"):
        self.idc+=1;
        self.c.execute('''insert into db values("{}","{}","{}","{}","{}")'''.format(self.idc,title,ttype,cover,link));

    def commit(self):
        with open("idcount","w") as ic:
            ic.write(str(self.idc));            
        self.db.commit();
        
    def getall(self):
        self.c.execute('''select * from db''');
        return self.c.fetchall();

    def gettype(self,ttype):
        self.c.execute('''select * from db where type="{}"'''.format(ttype));
        return self.c.fetchall();

def main():
    d=db("sample.db");
    d.add("title1","type1","cover","link");
    d.commit();
    print(d.getall());
    
main();
