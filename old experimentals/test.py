def main():
    with open("rawdata") as ifile:
        for l in ifile:
            print(l[:-1]);

main();
