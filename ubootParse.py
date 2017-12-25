#!/usr/bin/python2
import sys, getopt, binascii

def main(argv):
	inputfile = ' '
	outputfile = ' '
	debug = 0
	strbytes = 16
	try:
		opts, args = getopt.getopt(argv, "dhi:o:b:",["ifile=","ofile="])
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
		elif opt in ("-b"):
			strbytes = int(arg)

	if ((not inputfile) or (not inputfile) or (not opts)):
		printhelp()
		sys.exit(2)

	print inputfile
	print outputfile
	timeToParse(inputfile, outputfile, debug, strbytes)

def timeToParse(input, output, debug, strbytes):
	f = open(input, 'r')
	outfile = open(output, 'w')
	lastoffset = 0
	while True:
		line = f.readline()
		if not line: break
		offset = int(line[0:8], 16)
		strippedcontent = line[10:].replace(' ', '')
		hextoParse = strippedcontent[0:strbytes*2]
		if ((lastoffset >= offset) or (lastoffset + strbytes != offset)) and (lastoffset != 0):
			print "Non-contigous offsets or incorrect number of bytes in source line:"
			print "%08x" % lastoffset
			print "%08x" % offset
			sys.exit(2)
		if len(hextoParse) != strbytes * 2:
			print "Corrupted line:"
			print line
			sys.exit(2)
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
	print 'ubootParse.py -i <inputfile> -o <outputfile> -d -b [bytes in line]'

if __name__ == "__main__":
	main(sys.argv[1:])
