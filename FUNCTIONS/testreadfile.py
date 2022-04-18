import os

def read_input(parameter):
    os.chdir("..") #FUNCTIONS > GRANELTM
    os.chdir("INPUTRUN") #GRANELTM > INPUTRUN

    #Reading
    filekeep = open(parameter, "r")
    contentkeep = filekeep.read()
    filekeep.close()

    os.chdir("..") #INPUTRUN > GRANELTM
    os.chdir("OUTPUT") #GRANELTM > OUTPUT

    #Writing
    filekeepout = open("OUT_" + parameter, "w")
    filekeepout.write(contentkeep)
    filekeepout.close()

    return















