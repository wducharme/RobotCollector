
# Import the modules needed to run the script.
import sys, os
import time
import thread


class Robot():

    def __init__(self, name, robtype):
        self.name = name
        self.robtype = robtype
        self.taskList = []
        self.coins = 0
        self.completedTasks = 0
        self.overallCoins = 0

    def addTask(self, task):
        self.taskList.append(task)
        self.runTask(task.duration)


    def running_task(self,duration):
        t_end = time.time() + duration
        while time.time() < t_end:
            continue
        
        print self.name + " finished a task!"
        self.coins += self.taskList[0].value
        self.completedTasks += 1
        self.overallCoins += self.taskList[0].value
        self.taskList.pop(0)
        



    def runTask(self, time):
        thread.start_new_thread(self.running_task, (time,))



class Task():

    def __init__(self,name,duration, value):
        self.name = name
        self.duration = duration
        self.value = value

 
# Main definition - constants

taskDict = {1:Task('Doing the dishes', 5, 25),
                2:Task('Sweeping the floor', 10, 50),
                3:Task('Cleaning the house', 20, 100),
                4:Task('Taking out the recycling', 10, 50),
                5:Task('Making a sandwhich', 5, 25),
                6:Task('Mowing the lawn', 30, 150),
                7:Task('Raking the leaves', 25, 125),
                8:Task('Giving the dog a bath', 20, 100),
                9:Task('Baking some cookies', 20, 100),
                10:Task('Washing the car', 25, 125)}

typeDict = {1:'Unipedal',
            2:'Bipedal',
            3:'Quadrupedal',
            4:'Arachnid',
            5:'Radial',
            6:'Aeronautical'}

robotList = []


coinBalance = 100
 
# =======================
#     MENUS FUNCTIONS
# =======================
 
def startup():

    print "----------------------------------------------"
    print "Welcome to Robot Collector"
    print "The aim of this game is to collect as many coins and build as many robots as you can"
    print "Each robot costs 100 coins to make"
    print "Earn coins by having robots complete tasks"
    print "Have fun"
    print "Note: If the main menu isn't reflecting the most updated # of coins/robots, reload the main menu with option 5"

# Main menu
def main_menu():
    robotCount = len(robotList)
    global coinBalance
    choices = {'1': create,
                '2': viewCurrent,
                '3': addTask,
                '4': checkLeaderboard,
                '5': main_menu,
                '0': exit}

    for robot in robotList:
        if robot.coins > 0:
            coinBalance += robot.coins
            robot.coins = 0


    print "\n----------------------------------------------"
    print "Current Balance: " + str(coinBalance) + ""
    print "Robot Count: " + str(robotCount)
    print "\n "
    
    print "Please choose what you want to do:"
    print "1) Create a new robot"
    print "2) View current robots"
    print "3) Add a task to a robot"
    print "4) Check leaderboard"
    print "5) Reload main menu"
    print "\n0) Quit"
    choice = raw_input("")
    exec_choice(choice, choices)
 
    return
 
# Execute main menu
def exec_choice(choice, choices):
    ch = choice.lower()
    if ch == '':
        main_menu()
    else:
        try:
            choices[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            main_menu()
    return
 

def create():

    print "----------------------------------------------"
    print "Create Robot: "

    global coinBalance

    if coinBalance < 100:
        print "You do not have enough coins to buy a new robot"
        main_menu()

    
    print "Please enter the name you want:"
    name = raw_input("")

    if name == "":
        print "Please enter a non blank name"
        create()

    print "Please choose a type:"

    print "1) Unpiedal"
    print "2) Bipedal"
    print "3) Quadrupedal"
    print "4) Arachnid"
    print "5) Radial"
    print "6) Aeronautical"

    robType = fixInput(raw_input(""))

    if not robType or robType < 0 or robType > len(typeDict):
        print "Please enter a valid type"
        create()

    newRobot = Robot(name, typeDict[robType])

    robotList.append(newRobot)

    print "Robot " + str(name) + " created!"
    coinBalance -= 100
    print "New coin balance: " + str(coinBalance)
    main_menu()

    
    

def viewCurrent():
    print "----------------------------------------------"
    if len(robotList) == 0:
        print "No robots to display"
        main_menu()

    print "Current Robots:"
    for robot in robotList:
        print "Robot Name: " + robot.name
        if len(robot.taskList) > 0:
            print "\tCurrent Task: " + robot.taskList[0].name
        if len(robot.taskList) > 1:
            aList = ""
            for i in range(1, len(robot.taskList)):
                if i == len(robot.taskList)-1:
                    aList += robot.taskList[i].name
                else:
                    aList += robot.taskList[i].name + ", "
            print "\tPending Tasks: " + aList
    main_menu()


def addTask():
    if len(robotList) == 0:
        print "No robots active at the moment, please create one"
        main_menu()

    print "Choose a robot you want to add a task for:"
    for i,robot in enumerate(robotList):
        print str(i+1) + ") " + robot.name

    robChoice = fixInput(raw_input(""))
    if not robChoice or robChoice < 0 or robChoice > len(robotList):
        print "Please choose a valid robot"
        addTask()


    print "Choose a task you would like to add:"

    print "1) Do the dishes - Time: 5 seconds, Coins: 25"
    print "2) Sweep the house - Time: 10 seconds, Coins: 50"
    print "3) Do the laundry - Time: 20 seconds, Coins: 100"
    print "4) Take out the recycling - Time: 10 seconds, Coins: 50"
    print "5) Make a sandwich - Time: 5 seconds, Coins: 25"
    print "6) Mow the lawn - Time: 30 seconds, Coins: 150"
    print "7) Rake the leaves - Time: 25 seconds, Coins: 125"
    print "8) Give the dog a bath - Time: 20 seconds, Coins: 100"
    print "9) Bake some cookies - Time: 20 seconds, Coins: 100"
    print "10) Wash the car - Time: 25 seconds, Coins: 125"

    taskChoice = fixInput(raw_input(""))

    if not taskChoice or taskChoice < 0 or taskChoice > len(taskDict):
        print "Please choose a valid task"
        addTask()


    robotList[robChoice-1].addTask(taskDict[taskChoice])

    main_menu()


def checkLeaderboard():
    print "----------------------------------------------"
    print "Leaderboard: "
    tempRobotList = sorted(robotList, key=lambda robot: robot.overallCoins, reverse = True)
    count = 1
    for robot in tempRobotList:
        print str(count) + ". " + robot.name + ": " + str(robot.overallCoins) + " coins"
        count += 1
    main_menu()




 
 
# Exit program
def exit():
   sys.exit()

def fixInput(userIn):
    temp = int(userIn)
    return temp

 
 
# Program entry
if __name__ == "__main__":
    # Launch main menu
    startup()
    main_menu()

