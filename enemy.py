#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gamelib import *
from item import *
from entity import Entity

class Enemy(Entity):
    def __init__(self):
        self.name = "NULL"
        self.sprite = ["```NULL```",
                       "``[][][]``",
                       "``[][][]``",
                       "``[][][]``"]
        self.MAXHP = 10
        self.HP = 10
        self.ATK = 5
        self.DEF = 5
        self.SPD = 5
        self.LCK = 2
        self.EXP = 10
    def introText(self):
        return "Something's wrong... You've come across NULL`"
    def drops(self, battleItems):
        if random() < 0.50: battleItems.append(Item())
    
    # Carries out any attack, and provides all necessary prompts and textboxes
    #       PLAYER - The game's current player
    #       ENEMY[] 'enemyList' - List of enemies
    #       GUI  'GUI' - The game's current GUI
    def handleAttack(self, player, enemyList, GUI):
        DMG = self.calculateAttackDamage(player, 1.0, True, True, True)
        
        player.takeDamage(DMG[0])
        message = ""
        
        # If the attack misses
        if DMG[3]:
            message = self.name + "'s attack missed!`"
        
        # If the attack was critical
        elif DMG[2]:
            message = "Critical hit!`"
        
        # If the attack defeated the player
        deathMessage = ""
        if player.HP == 0:
            deathMessage = "Holy crap! That " + self.name + " totally killed you!`"
        
        GUI.drawHealthAndPower(player, enemyList)
        GUI.printGUI()
        printText(message + "The " + self.name + " hit you for " + str(DMG[0]) + " damage!`" +  deathMessage + "" +
                  "Press any key to continue. . . ")
        instantInput()

class Spider(Enemy):
    def __init__(self):
        self.name = "Spider"
        self.sprite = ["Spider`",
                       "```````",
                       "```````",
                       "`╔D╗```"]
        self.MAXHP = randint(20,24)
        self.HP = self.MAXHP
        self.ATK = 5
        self.DEF = 3
        self.SPD = 3
        self.LCK = 2
        self.EXP = 18
    def introText(self):
        textList = ["Ew... It's a spider...`",
                    "A spider... Good god, that's a huge spider.`",
                    "A spider appears. What a hoser.`",
                    "A spider arrives. Why is it so big??`"]
        return choice(textList)
    def drops(self, battleItems):
        if random() < 0.25: battleItems.append(EggCracker())

class Bat(Enemy):
    def __init__(self):
        self.name = "Bat"
        self.sprite = ["``Bat``",
                       "```````",
                       "``>ï<``",
                       "```````"]
        self.MAXHP = randint(16,18)
        self.HP = self.MAXHP
        self.ATK = 4
        self.DEF = 2
        self.SPD = 10
        self.LCK = 3
        self.EXP = 12
    def introText(self):
        textList = ["It's a bat... Are they... always this bloodthirsty?`",
                    "A bat appears...`",
                    "A bat appears...`"]
        return choice(textList)
    def drops(self, battleItems):
        if random() < 0.20: battleItems.append(Grape())

class SpiderCultist(Enemy):
    def __init__(self):
        self.name = "Spider Cultist"
        self.sprite = ["`Cltst`",
                       "╔O╗````",
                       "`t`````",
                       "`^`````"]
        self.MAXHP = randint(24,30)
        self.HP = self.MAXHP
        self.ATK = 4
        self.DEF = 2
        self.SPD = 3
        self.LCK = 2
        self.EXP = 20
    def introText(self):
        textList = ["It's some kind... Spider Cultist`",
                    "It's some kind... Spider Cultist`",
                    "That guy's got a spider-shaped hat. Can't be a good sign`",
                    "That guy is crawling with spiders... Ew.`",]
        return choice(textList)

    def handleAttack(self, player, enemyList, GUI):
        if len(enemyList) == MAX_ENEMY_COUNT or randint(0,1) == 1:
            return super().handleAttack(player, enemyList, GUI)
        else:
            enemyList.append(Spider())
            GUI.drawEntity(enemyList)
            GUI.drawHealthAndPower(player, enemyList)
            GUI.printGUI()
            printText("The Spider Cultist summons a Spider to the fight`"
                      "Press any key to continue. . . ")
            instantInput()
    def drops(self, battleItems):
      if random() < 0.20: battleItems.append(AAABattery())

class SpiderLord(Enemy):
    def __init__(self):
        self.name = "Spider Lord"
        self.sprite = ["``Ä````",
                       "`╔D╗```",
                       "``╔D╗``",
                       "`╔D╗```"]
        self.MAXHP = 140
        self.HP = self.MAXHP
        self.ATK = 8
        self.DEF = 5
        self.SPD = 2
        self.LCK = 2
        self.EXP = 250
    def introText(self):
        return "Oh god... That is one ugly dude.`"

    def handleAttack(self, player, enemyList, GUI):
        if len(enemyList) == MAX_ENEMY_COUNT or randint(0,2) == 2:
            return super().handleAttack(player, enemyList, GUI)
        else:
            if randint(0,1) == 1:
                enemyList.append(SpiderCultist())
                GUI.drawEntity(enemyList)
                GUI.drawHealthAndPower(player, enemyList)
                GUI.printGUI()
                printText("The Spider Lord slowly raises his arms into the air...`"
                          ".  .  .`"
                          "Wait... He's just calling someone... He hung up?`"
                          "Suddenly, a Spider Cultist bursts through a door and joins the fight.`"
                          "Press any key to continue. . . ")
                instantInput()
                        
            else:
                enemyList.append(Spider())
                GUI.drawEntity(enemyList)
                GUI.drawHealthAndPower(player, enemyList)
                GUI.printGUI()
                printText("A horrendous crackle emanates from the center of the Spider Lord.`" +
                          "A nearby Spider seems to think it's reaaally sexy...`"
                          "It joins the fight.`"
                          "Press any key to continue. . . ")
                instantInput()

class AntHill(Enemy):
    def __init__(self):
        self.name = "Ant Hill"
        self.sprite = ["`Anthl`",
                       "```````",
                       "```````",
                       "```▒```"]
        self.MAXHP = randint(10,12)
        self.HP = self.MAXHP
        self.ATK = 5
        self.DEF = 3
        self.SPD = 3
        self.LCK = 2
        self.EXP = 12
    def introText(self):
        textList = ["Ants are bad :(`"]
        return choice(textList)
