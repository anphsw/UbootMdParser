#!/usr/bin/python2
import sys, getopt, binascii

def main(argv):
	inputfile = ' '
	outputfile = ' '
	debug = 0
	try:
		opts, args = getopt.getopt(argv, "dhi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print "Invalid option, please run as:"
		printhelp()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			printhelp()
			sys.exit()
		elif opt in ("-i"):
			inputfile = arg
		elif opt in ("-o"):
			outputfile = arg
		elif opt in ("-d"):
			debug = 1

	print inputfile
	print outputfile
	timeToParse(inputfile, outputfile, debug)

def timeToParse(input, output, debug):
	f = open(input, 'r')
	outfile = open(output, 'w')
	lastoffset = 0
	while True:
		line = f.readline()
		if not line: break
		offset = int(line[0:8], 16)
		hextoParse = line[10:18] + line[19:27] + line[28:36] + line[37:45]
		if ((lastoffset >= offset) or (lastoffset + 16 != offset)) and (lastoffset != 0):
			print "Non-contigous offsets:"
			print "%08x" % lastoffset
			print "%08x" % offset
			sys.exit(2)
		if len(hextoParse) != 32:
			print "Corrupted line:"
			print line
			sys.exit(2)
		#hextoParse.replace(' ','')
		if debug == 1:
			print "%08x" % offset
			print hextoParse
		b_s = binascii.unhexlify(hextoParse)
		outfile.write(b_s)
		lastoffset = offset
	outfile.close()
	f.close()
	print "Finished parsing, now exiting..."

def printhelp():
	print 'ubootParse.py -i <inputfile> -o <outputfile> -d'

if __name__ == "__main__":
	main(sys.argv[1:])
