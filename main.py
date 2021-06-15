#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gamelib import *
from gui import *
from entity import *
from item import *
from player import *
from enemy import *

while True: # MAIN MENU LOOP - (Runs until user exits)
    clear()
    reply = printPrompt("What would you like to do?`"
                        "[1] Start a new game`"
                        "[2] How to play`"
                        "[3] Options`"
                        "[4] Exit", 4, False)

    # [1] Start a new game
    if reply == 1:
        # New game setup
        difficulty = 1
        world = 0
        GUI = GUIclass(world)
        player = Player()
        enemyList = []
        GUI.drawEntity(player)
        
        encounterCount = 0
        gamelog = open("gamelog.txt", "w")
        
        while True: # PRIMARY GAME LOOP - (Runs until game ends)
            if player.HP == 0:
                break
            GUI.eraseHealthAndPower()
            GUI.printGUI()
            printText(GUI.getIdleText())
            reply = printPrompt("What do you want to do?`"
                                "[1] Explore`"
                                "[2] Use Item`"
                                "[3] Explode (This kills you!)`"
                                "[4] Check Stats", 4, GUI)

            # [1] Explore - (Battle)
            if reply == 1:
                # New battle setup

                encounterCount += 1
                gamelog.write("Encounter #" + str(encounterCount) + ":\n")
                battleEXP = 0
                battleItems = []
                
                # Enemy Spawning: (Still being changed)
                # Boss fight
                if difficulty == 10:
                    enemyList.append(enemyLookup(10))
                    
                # Regular fight
                else:
                    # First enemy is added automatically
                    addEnemy(enemyList, difficulty)
                    # Enemies are repeatedely added with a 50% of success until one fails to be added
                    for e in range(0, MAX_ENEMY_COUNT - 1):
                        if randint(0,1) == 1:
                            addEnemy(enemyList, difficulty)
                            
                        else:
                            break
                
                for enemy in enemyList:
                    gamelog.write("    " + enemy.name + "\n")
                
                # POSSIBLE DIFFICULTY HANDLING: for i in range(0,len(enemyList)):
                
                GUI.drawEntity(enemyList)
                GUI.drawHealthAndPower(player, enemyList)
                GUI.printGUI()
                
                # Print intro text for all enemies
                introText = ""
                for val in enemyList:
                    introText += val.introText()
                    if val == enemyList[-1]:
                        introText = introText[:-1]
                printText(introText)

                while True: # BATTLE LOOP - (Runs until battle ends)
                    enemyCanAct = True

                    # Check if battle is over
                    if len(enemyList) == 0:
                        difficulty = difficulty + 1
                        player.EXP += battleEXP
                        player.HP = player.MAXHP
                        player.PWR = player.MAXPWR
                        gamelog.write("You won the fight!\n\n")
                        
                        # Item Checks
                        if(len(battleItems) > 0):
                            itemString = "You found some items!``"
                            for item in battleItems:
                                itemString += item.name + "`"
                                player.addItem(item)
                            itemString += "`Press any key to continue. . ."
                            printText(itemString)
                        
                        printText("You won the battle!`" +
                                  "You gained " + str(battleEXP) + " EXP`" +
                                  "Press any key to continue. . .")
                        instantInput()

                        # Check for level up
                        if player.EXP >= player.MAXEXP:
                            GUI.printGUI()
                            player.levelUp()
                            #GUI.drawHealthAndPower(player, enemyList)
                        break

                    # PLAYER'S TURN

                    reply = printPrompt("What do want to do?`"
                                        "[1] Attack`"
                                        "[2] Use Special Move`"
                                        "[3] Use Item`"
                                        "[4] Run", 4, GUI)
                
                    # [1] Attack
                    if reply == 1:
                        result = player.handleAttack(enemyList, battleItems, GUI, 0, 1.0)
                        # User went back
                        if result == -1:
                            enemyCanAct = False
                        # User went through with the attack
                        else:
                            battleEXP += result
                        
                    # [2] Use Special Move
                    elif reply == 2:
                        GUI.printGUI()

                        # Prompts user for a special move, listing all unlocked moves
                        prompt = "Choose a Special Move:`"
                        moveCap = player.LVL
                        if player.LVL > 3:
                            moveCap = 3
                        for i in range(0, moveCap):
                            prompt += "[" + str(i+1)
                            if i == 0:
                                prompt += "] Relaxing Yoga  (4 PWR)`Immense concentration allows to reach nirvana, restoring 50% of your HP.`"
                            elif i == 1:
                                prompt += "] Searing Beans  (3 PWR)`Spill a very hot can of beans at the enemies, causing each enemy to take 80% of your ATK.`"
                            elif i == 2:
                                prompt += "] Passionate Hug (3 PWR)`Affectionately hug an enemy. The fiery power of love causes the enemy to burn for 200% of your ATK.`"
                        prompt += "[" + str(moveCap+1) + "] BACK"
                        reply = printPrompt(prompt, moveCap+1, GUI)
                        
                        # Skips the next menu (executing special moves) if back was selected in previous prompt
                        backOption = False
                        if reply > moveCap:
                            enemyCanAct = False
                            backOption = True

                        enoughPWR = True
                        if not backOption:
                            # [1] Relaxing Yoga
                            if reply == 1:
                                if player.PWR >= 4:
                                    player.PWR -= 4
                                    battleEXP += player.handleAttack(enemyList, battleItems, GUI, reply, 1.0)                                
                                else:
                                    enoughPWR = False

                            # [2] Searing Beans
                            elif reply == 2:
                                if player.PWR >= 3:
                                    player.PWR -= 3
                                    battleEXP += player.handleAttack(enemyList, battleItems, GUI, reply, 0.8)
                                else:
                                    enoughPWR = False
                            
                            # [3] Passionate Hug
                            elif reply == 3:
                                if player.PWR >= 3:
                                    player.PWR -= 3
                                    result = player.handleAttack(enemyList, battleItems, GUI, 0, 2.0)
                                    # User went back
                                    if result == -1:
                                        enemyCanAct = False
                                    # User went through with the attack
                                    else:
                                        battleEXP += result
                                else:
                                    enoughPWR = False
                            
                            if not enoughPWR:
                                printText("You don't have enough power to perform this move.`"
                                          "Press any key to continue. . .")
                                instantInput()
                    
                    # [3] Use Item
                    elif reply == 3:
                        itemUsed = player.useItem(enemyList, GUI)
                        if not itemUsed:
                            enemyCanAct = False

                    # [4] Run
                    elif reply == 4:
                        GUI.printGUI()
                        enemyList.clear()
                        GUI.eraseEnemies()
                        player.HP = player.MAXHP
                        player.PWR = player.MAXPWR
                        printText("You booked it out of there!`" +
                                  "Press ANY KEY to continue...")
                        instantInput()
                        gamelog.write("You ran away from the fight\n\n")
                        break

                    # ENEMY'S TURN
                    
                    if enemyCanAct:
                        for enemy in enemyList:
                            enemy.handleAttack(player, enemyList, GUI)
                            GUI.drawHealthAndPower(player, enemyList)
                            GUI.printGUI()
                         
                            # If the player is dead... 
                            if player.HP == 0:
                                player.gameOver()
                                gamelog.write("You were defeated by " + enemy.name)
                                file.close()
                                break
                            

                        # Restore 1 power at the end of the turn
                        if player.PWR < player.MAXPWR:
                            player.PWR = player.PWR + 1
                            GUI.drawHealthAndPower(player, enemyList)

                        # If the player is dead...
                        if player.HP == 0:
                            break
                        
                    GUI.printGUI()  

            # [2] Use Item
            elif reply == 2:
                printText("You used an item. It does nothing`" +
                          "Press ANY KEY to continue...")
                instantInput()


            # [3] Explode
            elif reply == 3:
                clear()
                printText("You exploded... You're dead :(`" +
                          "Press ANY KEY to return to main menu")
                instantInput()
                break

            # [4] Check Stats
            elif reply == 4:
                clear()
                player.printStats(False, False)
                printText("Press ANY KEY to continue...")
                instantInput()
                
    # [2] How to play
    elif reply == 2:
        clear()
        printText("In this game, you advance through progressively more difficult battles.`"
                  "`"
                  "Each battle is turn-based, meaning first you perform an attack, and then each enemy gets to attack after you're done. "
                  "In battle, you will have a couple options: 'Attack', 'Special Move', and 'Run'.`"
                  "`"
                  "ATTACK:`"
                  "Choosing 'attack' will simply prompt you to attack one of the enemies in the battle, and you will deal damage to that enemy. "
                  "How much damage is you do is automatically calculated using your and the enemy's stats. "
                  "Any damage received by something is deducted from it's health (HP), which is displayed above it. "
                  "Stats are talked about in more detail below.`"
                  "`"
                  "SPECIAL MOVE:`"
                  "Choosing 'special move' will bring up a list of all the special moves you know."
                  "Generally, they are more powerful or versatile than a regular attack, but as a cost, they use power (PWR). "
                  "You regenerate 1 power at the end of every turn, so using special moves isn't a big deal, but you won't be able to do so every single turn. "
                  "You only start with one special move, but you gain another every time you defeat enough enemies to level up.`"
                  "Note: Not all special moves attack enemies. For example, the first one you get restores part of your health.`"
                  "`"
                  "RUN:`"
                  "Running away from a battle simply exits it. "
                  "At the moment there is no penalty for running away, so if it looks like you might die, running away might be a good idea.`"
                  "`"
                  "Every time you finish a battle, you earn experience. When you gain enough of it, you 'level up', which increases your stats and unlocks "
                  "a new special move."
                  "`"
                  "Lastly, it's important to note that whenever you enter a new battle, your power and health are initially full.")
        reply = printPrompt("[1] Return to main manu`"
                            "[2] Learn more about stats", 2, False)
        
        # [1] Return to menu
        # [no code needed]
        
        # [2] Learn more about stats
        if reply == 2:
            clear()
            printText("Each stat helps you in battle in a different way:`"
                      "'HP'  - health: The amount of damage you can take before dying.`"
                      "'ATK' - attack: The primary stat that determines how much damage you do to an enemy.`"
                      "'DEF' - defence: A higher defence means you take less damage from atacks.`"
                      "'SPD' - speed: A higher speed increases your chance to dodge an attack. A dodged attack does 0 damage.`"
                      "'LCK' - luck: A higher luck increases your chance to get a critical hit, which DOUBLES the damage of your attack.`"
                      "`"
                      "Defeating baddies will earn you more 'EXP' or experience, which will eventually cause you to level up. "
                      "Leveling up increases all of your stats a little bit, and gets you a new special move to use in combat.`"
                      "`"
                      "Press any key to return to main menu. . .")
            instantInput()
    
    # [3] Options
    elif reply == 3:
        
        while True:
            clear()
            reply = printPrompt("WARNING: Messing with these settings can and will crash the game if you set unreasonable values! If you're reasonable, you (probably) will be fine.`"
                                "`"
                                "[1] GUI_LENGTH ------- The length of the GUI and textboxes.`"
                                "                       This one is can be changed pretty freely, as long as it's long enough to hold the player and enemies.`"
                                "[2] GUI_ENTITY_SPACE - The width of the space allocated to each entity (player and enemies).`"
                                "                       This is probably pretty finicky. Expect crashes or weird GUI artifacts if you change it.`"
                                "[3] GUI_PLAYER_INDEX - The index of GUI where the player starts to be drawn.`"
                                "                       Just make sure it's within GUI_ENTITY_SPACE characters of the GUI_LENGTH, or else you'll crash.`"
                                "[4] GUI_ENEMY_INDEX -- The index of the GUI where the enemies start to be drawn.`"
                                "                       Give ample space in the GUI_LENGTH if you're going to modify this value. It has to have room to draw the maximum amount of enemies.`"
                                "[5] MAX_ENEMY_COUNT -- The maximum amount of enemies allowed in the game.`"
                                "                       As long as the GUI has room for it, you should be able to change this to anything. Except 0. It'll crash if you make it 0.`"
                                "`"
                                "[6] Save changes and return to main menu. . .", 6, False)
            
            if reply == 1:
                printText("Current value of GUI_LENGTH: " + str(GUI_LENGTH) + "`"
                          "Enter a new value. . .")
                GUI_LENGTH = int(input())
            
            elif reply == 2:
                printText("Current value of GUI_ENTITY_SPACE: " + str(GUI_ENTITY_SPACE) + "`"
                          "Enter a new value. . .")
                GUI_ENTITY_SPACE = int(input())
            
            elif reply == 3:
                printText("Current value of GUI_PLAYER_INDEX: " + str(GUI_PLAYER_INDEX) + "`"
                          "Enter a new value. . .")
                GUI_PLAYER_INDEX = int(input())
            
            elif reply == 4:
                printText("Current value of GUI_ENEMY_INDEX: " + str(GUI_ENEMY_INDEX) + "`"
                          "Enter a new value. . .")
                GUI_ENEMY_INDEX = int(input())
            
            elif reply == 5:
                printText("Current value of MAX_ENEMY_COUNT: " + str(MAX_ENEMY_COUNT) + "`"
                          "Enter a new value. . .")
                MAX_ENEMY_COUNT = int(input())
            
            else:
                options = open("options.txt", "w")
                instantInput()
                options.write("GUI_LENGTH = " + str(GUI_LENGTH) + "\n")
                options.write("GUI_ENTITY_SPACE = " + str(GUI_ENTITY_SPACE) + "\n")
                options.write("GUI_PLAYER_INDEX = " + str(GUI_PLAYER_INDEX) + "\n")
                options.write("GUI_ENEMY_INDEX = " + str(GUI_ENEMY_INDEX) + "\n")
                options.write("MAX_ENEMY_COUNT = " + str(MAX_ENEMY_COUNT) + "\n")
                options.close()
                printText("Changes saved to options.txt. You must restart the program for changes to take effect.`"
                          "Press any key to continue. . .")
                instantInput()
                break
            
    
    # [4] Exit
    elif reply == 4:
        break
        
    '''
                         , 
                    ,.  | \ 
                   |: \ ; :\ 
                   :' ;\| ::\ 
                    \ : | `::\ 
                    _)  |   `:`. 
                  ,' , `.    ;: ; 
                ,' ;:  ;"'  ,:: |_ 
               /,   ` .    ;::: |:`-.__ 
            _,' _o\  ,::.`:' ;  ;   . ' 
        _,-'           `:.          ;""\, 
     ,-'                     ,:         `-;, 
     \,                       ;:           ;--._ 
      `.______,-,----._     ,' ;:        ,/ ,  ,` 
             / /,-';'  \     ; `:      ,'/,::.::: 
           ,',;-'-'_,--;    ;   :.   ,',',;:::::: 
          ( /___,-'     `.     ;::,,'o/  ,::::::: 
           `'             )    ;:,'o /  ;"-   -:: 
                          \__ _,'o ,'         ,:: 
                             ) `--'       ,..:::: 
          -woof-             ; `.        ,::::::: 
                              ;  ``::.    ::::::: 
    
    '''
