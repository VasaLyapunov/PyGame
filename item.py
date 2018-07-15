from gamelib import *

class Item():
    def __init__(self):
        self.name = "NULL name"
        self.description = "NULL description"
        self.useText = "NULL useText"
    
    def use(self, player, enemyList, GUI):
        printText("You inspect the item carefully, but you cannot find a use for it...")



class EggCracker(Item):
    def __init__(self):
        self.name = "Egg Cracker"
        self.description = ("Restores 15 HP.`"
                            "`"
                            "Appears to have once been a proper egg, but years of solitude have caused it to dry into a crispy cracker.")
        self.useText = "You eat the Egg Cracker. It's not half bad."
    
    def use(self, player, enemyList, GUI):
        HPdifference = player.restoreHP(15)
        GUI.drawHealthAndPower(player, enemyList)
        GUI.printGUI()
        printText(self.useText + "`"
                  "You were healed for " + str(HPdifference) + " health!")


class Grape(Item):
    def __init__(self):
        self.name = "Grape"
        self.description = ("Restores 1 HP.`"
                            "`"
                            "A single grape.")
        self.useText = "You eat the grape. It's kinda sour."
    
    def use(self, player, enemyList, GUI):
        HPdifference = player.restoreHP(1)
        GUI.drawHealthAndPower(player, enemyList)
        GUI.printGUI()
        printText(self.useText + "`"
                  "You were healed for " + str(HPdifference) + " health!")


class AAABattery(Item):
    def __init__(self):
        self.name = "AAA Battery"
        self.description = ("Restores 5 PWR."
                            "`"
                            "The most basic battery around")
        self.useText = ("You take the old battery out of your pocket.`"
                        "Get this garbage out of here.`"
                        "You replace it with your brand new AAA bettery")
    
    def use(self, player, enemyList, GUI):
        PWRdifference = player.restorePWR(5)
        GUI.drawHealthAndPower(player, enemyList)
        GUI.printGUI()
        printText(self.useText + "`"
                  "You regained " + str(PWRdifference) + " power!")