def main():
    data=[];
    entry=[];
    with open("rawdata") as ifile:        
        for l in ifile:
            if l[-1]=="\n":
                l=l[:-1];
            if l=="---":
                data.append(entry);
                entry=[];
                continue;
            entry.append(l);            
    print(data);

main();
