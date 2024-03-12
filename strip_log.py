f = open("log_stripped.txt", "r")
outfile = open("processed_log.txt", "w")

lines = f.readlines()

for line in lines:
    if line[26] == "R":
        continue

    command_bytes = line[40:-4].replace(" ", "\\x")
    output_line = 'b"\\x' + command_bytes + '",\n'
    outfile.write(output_line)
