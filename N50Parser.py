from collections import OrderedDict
import argparse

# create specific object
parser = argparse.ArgumentParser(description="N50 parser")
parser.add_argument("-i", "--input", action="store", dest="input", required=True,
                    help="Input file with sequences")
parser.add_argument("-o", "--output", action="store", dest="output",
                    help="output file")
parser.add_argument("-o2", "--output2", action="store", dest="output2",
                    help="output file")
args = parser.parse_args()


def read_file(fasta_file):
    """Parse fasta file and return sequence and description dicts"""
    seq_dict = OrderedDict()
    desc_dict = OrderedDict()
    with open(fasta_file, 'r') as infile:
        seq_id = None
        seq = []
        desc = ''
        for line in infile:
            line = line.strip()
            if line.startswith('>'):
                if seq_id is not None:
                    seq_dict[seq_id] = ''.join(seq)
                    desc_dict[seq_id] = desc
                seq_id = line[1:].split()[0]
                seq.clear()
                desc = line[1:].split(maxsplit=1)[1] if ' ' in line else ''
            else:
                seq.append(line)
        if seq_id is not None:
            seq_dict[seq_id] = ''.join(seq)
            desc_dict[seq_id] = desc
    return seq_dict, desc_dict


def calc_n50(length_dict):
    """Calculate N50 from the lengths of sequences"""
    lengths = sorted(length_dict.values(), reverse=True)
    total_length = sum(lengths)
    half_length = total_length // 2
    cum_length = 0
    for i, length in enumerate(lengths):
        cum_length += length
        if cum_length >= half_length:
            return i+1, length


# Parse input file
seq_dict, desc_dict = read_file(args.input)

# Calculate sequence lengths
length_dict = {seq_id: len(seq) for seq_id, seq in seq_dict.items()}

# Calculate N50
n50, n50_length = calc_n50(length_dict)

# Write output files
with open(args.output, 'w') as outfile, open(args.output2, 'w') as outfile2:
    outfile.write("L50\t{}\n".format(n50))
    outfile.write("N50\t{}\n".format(n50_length))
    for seq_id, length in length_dict.items():
        outfile2.write(f"{seq_id} : {length}\n")
