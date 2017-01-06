def main():
    data=[];
    entry=[];
    with open("rawdata") as ifile:        
        for l in ifile:            
            l=l[:-1];
            if l=="---":
                data.append(entry);
                entry=[];
                continue;
            entry.append(l);            
        
    return data;




main();
