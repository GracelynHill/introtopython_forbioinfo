# This program takes in the name of a FASTA formatted file as an argument, and returns a new file called "nucleotide_counts.tsv" that contains the frequency of each nucelotide in each sequence, the frequency of nucleotides across all sequences, and the ratio of transitions to transversions (comparing the first sequence to all other sequences.) To run the program, write something like this in the command line program of your choice:
# \. Lab4.py example_file.fasta


import sys
#u_input = str(sys.argv[0]) # This line takes in the input from the command line
input_file = open('primatesNuc.fasta', 'r') # This opens the input as a file
output_file = open('nucleotide_counts.tsv', 'w') # creating the nucleotide_counts file
output_file.write('Gene\tA\tC\tG\tT\n') #writing the header
sequences = [] #An empty list of sequences that will be appended later in the script
transition = 0 #blank variables for transitions and transversions that will be edited by a loop later in the script
transversion = 0
AG = ['A', 'G'] #lists defining purines and pyrimidines
CT = ['C', 'T']
counter = 1 # a counter variable that will be used to loop through the list of sequences, caluclating Transition/transversion ratio. It starts at 1 so that it does not count the first sequence.
from Bio.Seq import Seq #Importing biopython modules that make the process of counting nucleotides and reading sequences easier
from Bio import SeqIO
for cur_record in SeqIO.parse(input_file, "fasta"): # This uses biopython to read the file in fasta format. Biopython understands which sections of the file are headers, names, sequences, etc.
    gene_name = cur_record.name
    length = len(cur_record.seq)
    A_count = cur_record.seq.count('A') # Counting the number of all four nucleotides
    C_count = cur_record.seq.count('C')
    G_count = cur_record.seq.count('G')
    T_count = cur_record.seq.count('T')
    A_freq = float((A_count / length) * 100) # changing the nucleotide counts into percentages
    C_freq = float((C_count / length) * 100)
    G_freq = float((G_count / length) * 100)
    T_freq = float((T_count / length) * 100)
    sequences.append(str(cur_record.seq)) #adding all of the sequences to a list that will be used later
    output_line = '%s\t%i\t%i\t%i\t%i\n' % \
    (gene_name, A_freq, C_freq, G_freq, T_freq) #printing out the percentages
    output_file.write(output_line)

fullfrequencyseq = Seq('') #this section adds all of the sequences together into a single sequence
for n in sequences:
  fullfrequencyseq += n
flength = len(fullfrequencyseq) #using the same logic as the last loop to calculate frequency across all sequences
A_fcount = fullfrequencyseq.count('A')
C_fcount = fullfrequencyseq.count('C')
G_fcount = fullfrequencyseq.count('G')
T_fcount = fullfrequencyseq.count('T')
A_ffreq = float((A_fcount / flength) * 100)
C_ffreq = float((C_fcount / flength) * 100)
G_ffreq = float((G_fcount / flength) * 100)
T_ffreq = float((T_fcount / flength) * 100)
output_file.write("frequency across all sequences: " + '\n' + str(A_ffreq) + '\t' + str(C_ffreq) + '\t' + str(G_ffreq) + '\t' + str(T_ffreq) + '\n') #writing the results
output_file.write("Number to the left is the sequence line number. Number to the right is the transition/transversion ratio of that sequence to the first sequence" + '\n') #explaining the formatting of the next section
for n in sequences:
    while counter < len(sequences):
        s1 = sequences[0] #defining the 2 sequences in the list that will be operated on for the transition/transversion ratio
        s2 = sequences[counter]
        counter = counter + 1
        for nt1, nt2 in zip(s1, s2): #looping through the sequences to find transitions and transversions, counting up if they are found
            if nt1 != nt2:
                if nt1 in AG and nt2 in AG:
                    transition += 1
                elif nt1 in CT and nt2 in CT:
                    transition += 1
                else:
                    transversion += 1
        titv = (' ' '%0.11f' % (transition / transversion)) #calculates the ratio
        output_file.write(str(counter + 1) + titv + '\n') #writes the ratio to the file
        transition = 0 #resetting the number of transitions and transversions
        transversion = 0
input_file.close() #closing the file
output_file.close()
