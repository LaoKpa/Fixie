#!/usr/bin/env python3

import io
import sys

import fixie

def printMessage(n, message):
	'''
	Pretty prints a single (unparsed) FIX message.
	:param n: int
	:param message: string
	'''
	assert(type(n) is int)

	if message == '':
		return

	print('%6d: %s%s' % (n, message[:100].replace(fixie.SEPARATOR, '|'), '...' if len(message) > 100 else ''))

	#TODO: error handling
	parsedMessage = fixie.parseMessage(message)
	for k in sorted(parsedMessage.keys()):
		name = fixie.TAG_ID_TO_NAME.get(k, '')

		value = parsedMessage[k]
		valueString = ', '.join(value) if type(value) is list else str(value)

		print('\t%20s [%4d] = %s' % (name, k, valueString))

	print()

def printFile(file):
	'''
	Pretty prints the contents of a file, line by line.
	'''
	for n, message in enumerate(file):
		printMessage(n, message)

def main():
	#Read from the file name passed as an argument, or stdin if none is passed
	if len(sys.argv) <= 1:
		printFile(sys.stdin)
	else:
		with io.open(sys.argv[1]) as fixFile:
			printFile(fixFile)

	return 0

if __name__ == '__main__':
	sys.exit(main())
