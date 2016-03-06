import re,os,sys
script, filename = sys.argv

# For debug purposes, a folder can be created which outputs the counted lines.
cleanedFolder = "cleaned"
debugMode = True

def countCodeLines():
    # If the program is in debug mode
    if debugMode:
        # Create the output folder if it does not exist
        if not os.path.exists(cleanedFolder):
            os.makedirs(cleanedFolder)
        # Create the output file
        outputFilename = cleanedFolder+ "/output_" + filename
        outputFile = open(outputFilename,'w')
        
    # Open the input file, read it's contents.
    # Note: Should check that there is enough RAM in the Python VM first...
    inputFile = open(filename)
    lines = inputFile.readlines()

    # Counter for the "valid" lines
    actualCodeLines = 0

    # Below are the identifiers for special lines #
    # Start & end of a multi-line comment
    multilineStart = re.compile(r"/\*")
    multilineEnd = re.compile(r"\*/")
    
    # Indicators that the current command "line" continues on the next line.
    # Our aim is to count this sort of "split" command only 1 time.
    notEndedLine = re.compile(r"[\(,&|]+ *$")
    
    # Some things such as {, else, do, } and only spaces/empty line are ignored.
    oneLineLogic = "(else|do|continue|pass|break)"
    nonLine = re.compile(r"^(("+
        oneLineLogic +  "[:{]?)? *((\)|}\)?);|[{}])|" + oneLineLogic + ")[:{]?$")

    # Keep track of whether a multi-line comment has been started
    # so that we know not to count any more lines until the end is found.
    multilineStarted = False

    # Go through each line
    for i in range(0,len(lines)):
        # Take it, remove the padded spaces/tabs, delete single-line comments
        line = lines[i]
        line = line.strip()
        line = re.sub(r"(//|#)+.+","", line)
        
        # Find whether it's entirely a "non-line". If it is
        # skip further processing, and don't count this line.
        if nonLine.match(line) != None:
            continue
        
        # If a multi-line comment is Started
        if multilineStarted == True:
            # check whether we've reached the End of it.
            if multilineEnd.match(line) != None:
                multilineStarted = False
                continue
        
        # If the line is empty, or we are still in a multi-line comment
        if len(line) == 0 or multilineStarted:
            # do nothing with this line
            pass
        # If the line is not part of a multi-line comment, and not empty
        else:
            # check whether it's the start of a multi-line.
            # If it is not
            if multilineStart.match(line) == None:
                # check whether it's an unfinished command, that continues
                # on the next line.
                # If it is not
                if notEndedLine.search(line) == None:
                    # this line counts!
                    actualCodeLines += 1
                    
                    # If the debug-mode is on, also store in the "clean" file
                    if debugMode:
                        outputFile.write(line + "\n")
                        
                # If it is a non-ended line,
                else:
                    # combine this line with the next line...
                    # ... effectively having the full command on one line
                    # in the end!
                    if(i < len(lines)-1):
                        lines[i+1] = line + lines[i+1]
                        
            # If it is a multi-line comment start
            else:
                # Check whether it's actually only all on one line!
                # If it is not
                if multilineEnd.search(line) == None:
                    # we have to ignore lines until we do find the end.
                    multilineStarted = True

    # Once done, close input file
    inputFile.close()
    
    # If applicable, close output file
    if debugMode:
        outputFile.write("Total lines: " + str(actualCodeLines))
        outputFile.close()
    
    # Return number of counted lines in the file
    return actualCodeLines

if __name__ == '__main__':
    print(countCodeLines())