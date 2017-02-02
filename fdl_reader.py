# Imports
import os, sys, random
from time import gmtime, strftime
from mine.FractalWorld import *

height1 = 1000 #height and width of the canvas created for drawing on.
width1 = 1400

# Classes
class Rule:
    def __init__(self, leftSide=None, rightSide=None):
        self.leftSide = leftSide
        self.rightSide = rightSide

    def __str__(self):
        return str(self.leftSide)+" -> "+str(self.rightSide)       

class Command:
    def __init__(self, command="nop", argument=None):
        self.command = command
        self.argument = argument

    def __str__(self):
        return ""+str(self.command)+" "+str(self.argument)

    def execute(self, turtle, length, newwidth=1, color="blue"):
        if color == "random":
            color = "#%02x%02x%02x" % (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        if self.command == "fd":
            fd(turtle, length, newwidth, color)
        if self.command == "bk":
            fd(turtle, -length, newwidth, color)
        if self.command == "lt":
            turtle.lt(self.argument)
        if self.command == "rt":
            turtle.rt(self.argument)
        if self.command == "nop":
            pass
        #if self.command == "scale":
        #    pass

class NewFractal:
    def __init__(self, rules=[], commands={}, length=0.0, depth=0.0, start="", width=1, color="blue"):
        self.rules = rules
        self.commands = commands
        self.length = length
        self.depth = depth
        self.start = start
        self.width = width
        self.color = color

    def __str__(self):
        String = "Rules: "
        for rule in self.rules:
            String = String+str(rule)+", "
        String = String+"\nCommands: "
        for command in self.commands:
            String = String+str(command)+" "+str(self.commands.get(command))+", "
        String = String+"\n"
        String = String+"Length: "+str(self.length)
        String = String+"\n"
        String = String+"Depth: "+str(self.depth)
        String = String+"\n"
        String = String+"Start: "+str(self.start)
        String = String+"\n"
        String = String+"Width: "+str(self.width)
        String = String+"\n"
        if self.color != "":
            String = String+"Color: "+str(self.color)
        else:
            String = String+"Color: Blue"
        return String
        
    def draw(self):
        print(self)
        myworld = FractalWorld(height=height1, width=width1, delay=0)
        bob = Fractal(draw = False)
        #bob.x = (width1 / 2) + 50 # can be used to adjust the starting posistion for the turtle, could also be set in the .fdl file, and be added as properties of Fractal.
        bob.y = -(height1 / 2) + 50
        theoneruletorulethemall = applyRuleStr(self.start, self.rules, self.depth)
        for letter in theoneruletorulethemall:
            if self.commands[letter].command == "scale":
                self.length = self.length * self.commands[letter].argument
            # if self.commands[letter].command == "width": # width could also be implemented as a command so it would be possible to change it everytime a line is drawn
            #    self.width = self.commands[letter].argument
            else:
                self.commands[letter].execute(bob, self.length, self.width, self.color)
        #print(tobecmds) # can be used to check that rules are applies correctly, for small depths at least.        
        

# Functions
def applyRuleStr(cmdstr, Rules, depth):
    """Applies a rule to a str"""
    assert type(cmdstr) is str 
    i = 0
    while i < depth:
        for rule in Rules:
            cmdstr = cmdstr.replace(rule.leftSide,rule.rightSide)
        i = i+1
    return cmdstr
           
def load(name):
    print("Time begun: "+strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    if os.path.isfile(name) == True:
        file = open(name, "r")
    elif os.path.isfile(name+".fdl") == True:
        file = open(name+".fdl", "r")
    else:
        print("File "+name+" doesn't exists")
        return
    myfractal = NewFractal(rules=[], commands={}, length=0.0, depth=0.0, start="", width=1, color="") #creates a new Fractal
    for line in file.readlines():
        line = line.replace(" ","")
        line = line.replace("\n","")
        if "start" in line: # adding of non-command properties starts.
            myfractal.start = line[5:]
        if "rule" in line:
            myfractal.rules.append(Rule(line[4],line[7:]))
        if "length" in line:
            myfractal.length = float(line[6:])
        if "depth" in line:
            myfractal.depth = float(line[5:])
        if "width" in line:
            myfractal.width = float(line[5:])
        if ("color" in line) or ("colour" in line):
            myfractal.color = line[5:]
        if "cmd" in line: # adding of commads starts here.
            if "scale" in line:
                myfractal.commands[line[3]] = Command(line[4:9], float(line[9:]))
            if ("fd" in line) or ("bk" in line):
                myfractal.commands[line[3]] = Command(line[4:6], myfractal.length)
            if ("rt" in line) or ("lt" in line):
                myfractal.commands[line[3]] = Command(line[4:6], float(line[6:]))
            if "nop" in line:
                myfractal.commands[line[3]] = Command()
    myfractal.draw()

load(str(sys.argv[1]))
print("Time done: "+strftime("%Y-%m-%d %H:%M:%S", gmtime()))
wait_for_user()

