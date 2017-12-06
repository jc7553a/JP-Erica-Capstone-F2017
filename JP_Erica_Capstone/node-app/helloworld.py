import sys, json
<<<<<<< HEAD
import numpy as np
#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])
=======

# #Read data from stdin
# def read_in():
#     lines = sys.stdin.readlines()
#     #Since our input would only be having one line, parse our JSON data from that
#     return json.loads(lines[0])
>>>>>>> 5d1811e0a88af564ac1ce4cde071073638426ab5

# def main():
#     #get our data as an array from read_in()
#     lines = read_in()

#     linesString = ""
#     for l in lines:
#         linesString += str(l)

<<<<<<< HEAD
    #return the sum to the output stream

    print "Hello there " + linesString

#start process
if __name__ == '__main__':
    main()
=======
#     #return the sum to the output stream
#     print "Hello there "
#     sys.stdout.flush()

# #start process
# if __name__ == '__main__':
#     main()

data = "this began life in python"
print "data"
# sys.stdout.flush()
>>>>>>> 5d1811e0a88af564ac1ce4cde071073638426ab5
