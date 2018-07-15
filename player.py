#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gamelib import *
from item import *
from entity import Entity

class Player(Entity):

    def __init__(self):

        self.LVL = 1
        self.MAXEXP = 100
        self.EXP = 0
        self.sprite = ["`O````````",
                       "`t````````",
                       "`^````````"]
        self.MAXHP = 30
        self.HP = 30
        self.MAXPWR = 5
        self.PWR = 5
        self.ATK = 16
        self.DEF = 2
        self.SPD = 5
        self.LCK = 5
        
        self.itemList = [EggCracker(), Grape(), EggCracker(), AAABattery()]



    # Prints the player's stats in the correct format
    #       STR[] 'extraList' - A list of strings to append after each stat, used for leveling up - OPTIONAL
    #       STR[] 'statList' - A string version of all stats, used for leveling up - OPTIONAL
    def printStats(self, statList, extraList):
        
        # Checks to see if an statList was provided. If not, make one using player stats
        try:
            len(statList)
        except:
            statList = []
            statList.append(str(self.MAXHP))
            statList.append(str(self.ATK))
            statList.append(str(self.DEF))
            statList.append(str(self.SPD))
            statList.append(str(self.LCK))
            statList.append(str(self.LVL))
            
        # Checks to see if an extraList was provided. If not, make an empty one
        try:
            len(extraList)
        except:
            extraList = []
            for i in range(0,6):
                extraList.append("")
        
        # Generates a new sprite where all ` characters are converted to spaces
        newSprite = []
        for i in range(0,len(self.sprite)):
            newSprite.append(self.sprite[i].replace("`"," "))
        
        clear()
        printText("  YOU       " +      " HP:  " + str(statList[0]) + extraList[0] + "`"
                  "            " +      " ATK: " + str(statList[1]) + extraList[1] + "`"
                  "  " + newSprite[0] + " DEF: " + str(statList[2]) + extraList[2] + "`"
                  "  " + newSprite[1] + " SPD: " + str(statList[3]) + extraList[3] + "`"
                  "  " + newSprite[2] + " LCK: " + str(statList[4]) + extraList[4] + "`"
                  " `"
                  "            " +      " LEVEL " + str(statList[5]) + extraList[5] + "`"
                  "            " +      " EXP:  " + str(self.EXP) + "/" + str(self.MAXEXP))



    def levelUp(self):
        self.EXP = self.EXP - self.MAXEXP
        self.MAXEXP = self.MAXEXP*2
        printText("Holy crap, you leveled up!`" +
                  "Press ANY KEY to continue...")
        instantInput()

        # Generates randomized stat upgrades
        statList = [self.MAXHP, self.ATK, self.DEF, self.SPD, self.LCK, self.LVL]
        plusList = []
        plusList.append(randint(8,14))
        self.MAXHP += plusList[0]
        self.HP += plusList[0]
        plusList.append(randint(1,2))
        self.ATK += plusList[1]
        plusList.append(randint(1,2))
        self.DEF += plusList[2]
        plusList.append(randint(1,2))
        self.SPD += plusList[3]
        plusList.append(randint(1,1))
        self.LCK += plusList[4]
        plusList.append(1)
        self.LVL += 1

        # Ports the stat upgrade list to a new list, modified for displaying stats
        plusListStr = []
        for i in range(0,6):
            s = ""
            for j in range(0,3 - len(str(statList[i]))):
                s += " "
            plusListStr.append(s + " + " + str(plusList[i]))

        # Initial stat gain display ie. "HP: 100 + 20"
        clear()
        self.printStats(statList, plusListStr)
        time.sleep(1)

        # Stat gain addition loop ie. "HP: 120"
        for i in range(0, 6):
            
            if i == 0:
                statList[0] += plusList[0]
            elif i == 1:
                statList[1] += plusList[1]
            elif i == 2:
                statList[2] += plusList[2]
            elif i == 3:
                statList[3] += plusList[3]
            elif i == 4:
                statList[4] += plusList[4]
            elif i == 5:
                statList[5] += plusList[5]
            plusListStr[i] = ""
            
            self.printStats(statList, plusListStr)
            time.sleep(0.4)

        # Bonus point allocation
        bonus = 2
        while bonus > 0:
            
            # SpaceList ensures proper spacing of the [#] boxes during the bonus point section
            spaceList = []
            for i in range(0,5): # Loops through all stats
                sp = ""
                for j in range(0,3 - len(str(statList[i]))): # Loops through all number of spaces necessary
                        sp += " "
                sp += "[" + str(i+1) + "]"
                spaceList.append(sp)
            spaceList.append("")
                    
            self.printStats(statList, spaceList)
                
            reply = printPrompt("You have " + str(bonus) + " extra bonus stat points. Choose a stat to allocate a point to.`"
                                "Note: Allocating a point to HP will increase it by 5 instead of 1`"
                                "[1] HP`"
                                "[2] ATK`"
                                "[3] DEF`"
                                "[4] SPD`"
                                "[5] LCK", 5, False)

            # [1] HP
            if reply == 1:
                self.MAXHP += 5
                self.HP += 5
                statList[0] += 5

            # [2] ATK
            elif reply == 2:
                self.ATK += 1
                statList[1] += 1
            
            # [3] DEF
            elif reply == 3:
                self.DEF += 1
                statList[2] += 1

            # [4] SPD
            elif reply == 4:
                self.SPD += 1
                statList[3] += 1

            # [2] LCK
            elif reply == 5:
                self.LCK += 1
                statList[4] += 1

            bonus -= 1

        # New Special Move textbox
        if self.LVL <= 3:
            if self.LVL == 2:
                s = "SEARING BEANS"
            elif self.LVL == 3:
                s = "PASSIONATE HUG"
            clear()
            self.printStats(False, False)
            printText("You learned the Special Move: " + s + "!`"
                      "Press ANY KEY to continue...")
            instantInput()

        clear()
        self.printStats(False, False)
        printText("You are now level " + str(self.LVL) + "!`"
                  "Press ANY KEY to continue...")
        instantInput()
    
    
    
    def gameOver(self):
        clear()
        wait = ""
        spacing = ""
        for i in range(0, int(GUI_LENGTH/2) - 4):
            spacing += " "
        for i in range(0,4):
            printText("```" +
                      spacing + "GAME OVER`" +
                      spacing + "   :'(`" +
                      "`" +
                      spacing + "   " + wait + "`")
            time.sleep(1)
            wait += "."
            clear()
    
    # Restores PWR of Player while making sure it does not surpass MAXPWR
    #       INT 'PWRamount' - How much PWR to restore
    # Returns how much PWR was actually restored 
    def restorePWR(self, PWRamount):
        PWRinitial = self.PWR
        if PWRamount + self.PWR > self.MAXPWR:
            self.PWR = self.MAXPWR
        else:
            self.PWR = self.PWR + PWRamount
        return self.PWR - PWRinitial
    
    # Prompts the user which enemy they would like to target (If there is more than one)
    #       ENEMY[] 'enemyList' - List of enemies in current battle
    #       GUI  'GUI' - The game's current GUI
    def printEnemyPrompt(self, enemyList, GUI):
            enemyCount = len(enemyList)
            if enemyCount > 1:
                GUI.drawEnemyIndex(enemyList)
                GUI.printGUI()
                prompt = "Which enemy do you want to attack?`"
                for e in range(0, enemyCount):
                    prompt += "[" + str(e+1) + "] " + enemyList[e].name + "`"
                prompt += "[" + str(enemyCount+1) + "] BACK"
                reply = printPrompt(prompt, enemyCount+1, GUI) - 1
            else: reply = 0
            
            if reply == enemyCount:
                GUI.drawHealthAndPower(self, enemyList)
                return 0
            return enemyList[reply]
            
    # Removes all dead enemies and redraws the 'enemyList'
    #       ENEMY[] 'enemyList' - List of enemies
    #       ITEM[] 'battleItems' - List of items dropped in battle so far
    #       GUI  'GUI' - The game's current GUI
    def removeDeadEnemies(self, enemyList, battleItems, GUI):
        battleEXP = 0
        removeList = []
        for enemy in enemyList:
            if enemy.HP == 0:
                battleEXP += enemy.EXP
                enemy.drops(battleItems)
                removeList.append(enemy)
        for enemy in removeList:
            enemyList.remove(enemy)
        GUI.eraseEnemies()
        GUI.drawEntity(enemyList)
        return battleEXP
    
    # Carries out any attack, and provides all necessary prompts and textboxes
    #       ENEMY[] 'enemyList' - List of enemies
    #       ITEM[] 'battleItems' - List of items dropped in battle so far
    #       GUI  'GUI' - The game's current GUI
    #       INT  'specialMoveIndex' - The index specifying which special move to carry out (Or 0, if a regular attack)
    #       FLT  'multiplier' - Multiplies damage
    def handleAttack(self, enemyList, battleItems, GUI, specialMoveIndex, multiplier):
        battleEXP = 0
        # NOT a special move - (Regular attack)
        if specialMoveIndex == 0:
            # Prompts the user which enemy they would like to target (If there is more than one)
            target = self.printEnemyPrompt(enemyList, GUI)
            if target == 0:
                return -1;
            
            DMG = self.calculateAttackDamage(target, multiplier, True, True, True)
            target.takeDamage(DMG[0])
            message = ""
            
            # If the attack misses
            if DMG[3]:
                message = "Your attack missed!`"
            
            # If the attack was critical
            elif DMG[2]:
                message = "Critical hit!`"
            
            # If the attack defeated the enemy
            deathMessage = ""
            if target.HP == 0:
                deathMessage = target.name + " is defeated!`"
            
            GUI.drawHealthAndPower(self, enemyList)
            GUI.printGUI()
            printText(message + "You hit " + target.name + " for " + str(DMG[0]) + " damage!`" +  deathMessage + "" +
                      "Press any key to continue. . . ")
            instantInput()
            
            battleEXP += self.removeDeadEnemies(enemyList, battleItems, GUI)
            GUI.drawHealthAndPower(self, enemyList)
        
        # [1] Relaxing Yoga 
        # "Immense concentration allows you to reach nirvana, restoring 50% of your HP"
        elif specialMoveIndex == 1:
            heal = int(self.MAXHP/2) + 1
            HPdifference = self.restoreHP(heal)
            GUI.drawHealthAndPower(self, enemyList)
            GUI.printGUI()
            printText("You were healed for " + str(HPdifference) + " health!`"
                      "Press ANY KEY to continue...")
            instantInput()
            
        # [2] Searing Beans
        # "Spill a very hot can of beans at the enemies, causing each enemy to take 80% of your ATK"
        elif specialMoveIndex == 2:
            message = ""
            # Loop through all enemies, burning them once each
            for target in enemyList:
                DMG = self.calculateAttackDamage(target, multiplier, True, False, False)
                target.takeDamage(DMG[0])

                # If the attack defeated the enemy
                deathMessage = ""
                if target.HP == 0:
                    deathMessage = target.name + " is defeated!`"
                
                message += target.name + " was seared for " + str(DMG[0]) + " damage!`" + deathMessage
            
            GUI.drawHealthAndPower(self, enemyList)
            GUI.printGUI()
            printText(message +
                      "Press any key to continue. . . ")
            instantInput()
            
            battleEXP += self.removeDeadEnemies(enemyList, GUI)
            GUI.drawHealthAndPower(self, enemyList)
            
        # [3] Passionate Hug
        # "Affectionately hug an enemy. The fiery power of love causes the enemy to burn for 200% of your ATK."
        elif specialMoveIndex == 3:
            battleEXP += self.handleAttack(enemyList, GUI, 0, multiplier)
        
        return battleEXP

    # Adds an item to the player's inventory
    #       ITEM 'item' - The actual item given
    #def addItem(self, item):
        
    
    # Handles all the menus required to use an Item, and calls an Item's use function if successful
    #       GUI 'GUI' - The game's current GUI
    #       ENEMY[] 'enemyList' - List of enemies in current battle
    def useItem(self, enemyList, GUI):
        itemCount = len(self.itemList)
        
        # Player doesn't have item? Send em back!
        if itemCount == 0:
            printText("You don't have any items!`"
                      "Press ANY KEY to continue...")
            instantInput()
            return 0
        
        clear() 
        # Print all items and prompt user
        for i in range(itemCount):
            printText("[" + str(i+1) + "] " + self.itemList[i].name + "``" + self.itemList[i].description)
        printText("[" + str(itemCount+1) + "] BACK")
        reply = printPrompt("Choose an item...", itemCount+1, True)
        
        # Did the user want to go back?
        if reply == itemCount+1:
            return 0
        
        # Use the selected item
        clear()
        GUI.printGUI()
        self.itemList[reply-1].use(self, enemyList, GUI);
        del self.itemList[reply-1]
        printText("Press any key to continue. . .")
        instantInput()
        return 1