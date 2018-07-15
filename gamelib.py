#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from random import choice
import time
import sys
import os
if os.name == 'nt':
    import msvcrt

# Clears the console
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    #print("\n\n")

# Prints a message in the correct format
#       STR  'message' - The message to be displayed within the box
#
# PRECNT: Messages cannot contain a single word of GUI_LENGTH characters or longer
def printText(message):
    
    # Generates and prints the roof of the message box   ie. "╔══════════╗"
    top = "╔"
    for i in range(0, GUI_LENGTH):
        top += "═"
    print(top + "╗")
    
    # Generates and prints the inside of the message box ie. "║A message ║"
    while len(message) > GUI_LENGTH or message.find("`") != -1:

        # Index of the last space in the current line of the message
        lastSpace = message[:GUI_LENGTH+1].rfind(" ")
        
        # If no space is found in the current line, one is added into the message at the 'GUI_LENGTH'th index
        if lastSpace == -1:
            message = message[:GUI_LENGTH] + " " + message[GUI_LENGTH:]
            lastSpace = GUI_LENGTH

        # The ` character indicates a new line. If it's found, it takes the place of the last space
        if message[:GUI_LENGTH+1].find("`") != -1:
            lastSpace = message[:GUI_LENGTH+1].find("`")

        # Creates a message to dispay in the current line (GUI_LENGTH chars)
        lineMessage = message[:lastSpace]
        for i in range(0,GUI_LENGTH-len(lineMessage)):
            lineMessage += " "
        
        print("║" + lineMessage + "║")
        message = message[lastSpace+1:]

    # Modifies the last line in the message box to be GUI_LENGTH characters in length
    for i in range(0,GUI_LENGTH-len(message)):
            message += " "
    print("║" + message + "║")
    
    # Generates and prints the roof of the message box   ie. "╚══════════╝"
    bot = "╚"
    for i in range(0,GUI_LENGTH):
        bot += "═"
    print(bot + "╝")



# On windows console: waits until a a key is pressed and returns its ordinal form, take 48 (This way, entering 1 returns 1, etc.)
# On any other OS, calls instantInput(), and converts input to an int. If invalid, returns 0
def instantInput():
    if os.name != "nt": # Everything but windows here (Unix)
        try:
            return int(input())
        except:
            return 0
    else:               # Windows here
        while True:
            key = ord(msvcrt.getch()) - 48
            if key != -48:
                return key
            time.sleep(0.1)



# Prints a prompt and re-prompts the player until a valid choice has been selected
#   STR  'message' - Prompts this message (Must also contain choices)
#   INT  'optionCount' - The amount of possible options in the prompt
#   GUI  'GUI' - The current GUI in the game
def printPrompt(message, optionCount, GUI):
    printText(message)
    reply = instantInput()
    retryString = "That is not a valid input. Try again "
    while True:
        if reply > 0 and reply <= optionCount:
            return reply
        clear()
        printText(message)
        retryString += ". . . "
        printText(retryString)
        reply = instantInput()
    



# Prints messages one character at a time, all fancy-like
# Note: Definitely does not work on the IDLE console
def printFancyText(message):
    # If running in IDLE - avoids fanciness
    if "idlelib" in sys.modules:
        printText(message)

    # If running in elsewhere ie. console
    else:
        for i in range(0,len(message)):
            clear()
            if "GUI" in globals():
                GUI.printGUI()
            printText(message[:i+1])
            if message[i] != " ":
                time.sleep(0.005)

def writeOptions():
    options = open("options.txt", "w")
    options.write("GUI_LENGTH = " + str(GUI_LENGTH) + "\n")
    options.write("GUI_ENTITY_SPACE = " + str(GUI_ENTITY_SPACE) + "\n")
    options.write("GUI_PLAYER_INDEX = " + str(GUI_PLAYER_INDEX) + "\n")
    options.write("GUI_ENEMY_INDEX = " + str(GUI_ENEMY_INDEX) + "\n")
    options.write("MAX_ENEMY_COUNT = " + str(MAX_ENEMY_COUNT) + "\n")
    options.close()

#
#def populateEnemyList(enemyList, :
from enemy import *
    

# Updates the enemy list with the appropriate enemies for the current difficulty
def addEnemy(enemyList, difficulty):
    for i in range(difficulty,-1,-1):
        # If the loop gets all way to the index corresponding to difficulty 1, 100% to return the corresponding enemy
        if i == 0:
            enemyList.append(enemyLookup(0))
            return
        else:
        # 50% chance to return the enemy corresponding to the current difficulty
        # Otherwise, run the loop again and run the same chance on the enemy corresponding to the previous difficulty
            if randint(0,1) == 1:
                enemyList.append(enemyLookup(i))
                return

# Returns the proper enemy based on the difficulty index provided
def enemyLookup(index):
    #return AntHill()
    if index == 0:
        return Spider()
    elif index == 1:
        return Bat()
    elif index == 2:
        return Bat()
    elif index == 3:
        return Spider()
    elif index == 4:
        return SpiderCultist()
    elif index == 5:
        return SpiderCultist()
    elif index == 6:
        return Spider()
    elif index == 7:
        return Bat()
    elif index == 8:
        return SpiderCultist()
    elif index == 9:
        return SpiderCultist()
    elif index == 10:
        return SpiderLord()
    else:
        return Spider()



# Constant variables
GUI_LENGTH = 100
GUI_ENTITY_SPACE = 10
GUI_PLAYER_INDEX = 5
GUI_ENEMY_INDEX = 25
MAX_ENEMY_COUNT = 3

optionsList = []

# Try to extract the options from options.txt
try:
    options = open("options.txt", "r")
    optionsList = []
    for i in range(5):
        # This god damn disaster of a line extracts the first number from a string and converts it to an int, and throws an exception if there is no valid int
        # Thanks apricity! - https://stackoverflow.com/questions/26825729/extract-number-from-string-in-python
        optionsList.append( int(''.join(list(filter(str.isdigit, options.readline())))) )
    GUI_LENGTH = optionsList[0]
    GUI_ENTITY_SPACE = optionsList[1]
    GUI_PLAYER_INDEX = optionsList[2]
    GUI_ENEMY_INDEX = optionsList[3]
    MAX_ENEMY_COUNT = optionsList[4]
except:
    GUI_LENGTH = 100
    GUI_ENTITY_SPACE = 10
    GUI_PLAYER_INDEX = 5
    GUI_ENEMY_INDEX = 25
    MAX_ENEMY_COUNT = 3
    writeOptions()
    printText("WARNING: Could not read options.txt. Options have been reset and options.txt has been modified appropriately.`"
          "Press any key to continue. . .")
    instantInput()