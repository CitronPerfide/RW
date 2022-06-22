from collections import OrderedDict
import argparse

# create specific object
parser = argparse.ArgumentParser(description = "N50 parser")

#parser = argparse.ArgumentParser(prog="N50Parser.py", usage="N50")







parser.add_argument("-i", "--input", action="store", dest="input", required=True,
                    help="Input file with sequences")
parser.add_argument("-o", "--output", action="store", dest="output",
                    help="output file")
parser.add_argument("-o2", "--output2", action="store", dest="output2",
                    help="output file")


args = parser.parse_args()



def read_file(fasta_file):
    "Parse fasta file"
    descriptiondict = OrderedDict()
    dictionnary = OrderedDict()
    with open(fasta_file, 'r') as infile:
        for line in infile:
            record = line.strip()
            if record and record[0] == '>':
                seqid = record.split(" ")[0][1:]
                dictionnary[seqid] = ""
                description = record.split(" ", 1)[1]
                descriptiondict[seqid] = description
                continue
            dictionnary[seqid] += record

    return dictionnary, descriptiondict



seqdict, descriptdict = read_file(args.input)
#print(seqdict[seqid])


lengthdict = OrderedDict()
for sequenceid in seqdict:
    lengthdict[sequenceid] = len(seqdict[sequenceid])


length = sum(lengthdict.values())


N_number = sum([seqdict[seqid].count("N") for seqid in seqdict])

print(N_number)
print(length)
all_len = sorted(lengthdict.values(), reverse=True)
print(all_len)

if length > 0:
    acum = 0

    for y in range (len(all_len)):
        if acum <= length / 2:
            acum = all_len[y] + acum
            n = y #L50
        else:
            break


    n = n + 1
    print("The L50 is", n)
    print("The N50 is", all_len[n-1])

with open(args.output, 'w') as outfile:
    outfile.write("L50\t{}\n".format(n))
    outfile.write("N50\t{}\n".format(all_len[n-1]))


with open(args.output2, "w") as file:
    for key, value in lengthdict.items():
        file.write(f"{key} : {value}\n")

