import getopt, sys

opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
print(opts)

print(args)
