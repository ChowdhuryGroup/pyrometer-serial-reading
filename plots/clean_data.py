f = open("2024-03-15_15-30-27.tsv", "r")
outfile = open("2024-03-15_15-30-27_cleaned.tsv", "w")

previous_current = ""
for line in f:
    current = line.split("\t")[1]
    if current == previous_current:
        continue
    outfile.write(line)
    previous_current = current
