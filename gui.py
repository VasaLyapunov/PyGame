#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gamelib import *

class GUIclass:
    
    # GUIclass contructor
    #       INT  'world' - The current world to display
    #
    # PRECNT: 'world' must be a valid index in 'worldList', defined below
    def __init__(self, world):
        # Presets for the current world are contained in 'worldList[]'
        self.worldList = [ ["==================================================",
                            "--------------------------------------------------",
                            "                                                  ",
                            "                                                  ",
                            "__________________________________________________"] ]
        
        # The actual current state of the GUI is stored in 'layers[]'
        self.world = world
        self.layers = []
        for i in range(0,5):
            layer = ""
            self.layers.append("")
            self.eraseLayer(i)
    
    
    
    # Clears the console and prints whatever is currently in the GUI in the correct format
    def printGUI(self):
        clear()
        
        # Generates and prints the roof of the GUI   ie. "╔══════════╗"
        top = "╔"
        for i in range(0, GUI_LENGTH):
            top += "═"
        print(top + "╗")
        
        # Generates and prints the inside of the GUI ie. "║  ╔D╗     ║"
        for layer in self.layers:
            print("║" + layer + "║")
        
        # Generates and prints the roof of the GUI   ie. "╚══════════╝"
        bot = "╚"
        for i in range(0,GUI_LENGTH):
            bot += "═"
        print(bot + "╝")



    # Provides flavor text for the current location based on the world variant
    def getIdleText(self):

        # Retreives the current area's list of idle text variants
        idleTextList = []
        if self.world == 0:
            idleTextList = ["It's eerily quiet in the room.",
                            "The room is covered in a thick layer of dust.",
                            "It smells like old people.",
                            "The room is painfully bland.",
                            "Until now, you didn't know a room could look this plain.",
                            "Sure is quiet...",
                            "You don't know who built this place... But they sure were pretty bad at it.",
                            "You feel kind of like taking a nap."]
                            
        return (choice(idleTextList))
    
    
    
    # Modifies the layer in 'self.layers[]' at 'layerIndex' to contain the passed 'string', starting at 'startingIndex'
    #       INT  'layerIndex' - The index of the layer on which 'string' is drawn on
    #       STR  'string' - The string that is drawn onto the passed given layer
    #       INT  'startingIndex' - The index on the passed layer on which the 'string' will start on
    #
    # PRECNT: 'layerIndex' must be a valid index of 'self.layers[]'
    # PRECNT: 'startingIndex' + the length of 'string' must not exceed the final index of the layer at 'layerIndex'
    def drawLayerSection(self, layerIndex, string, startingIndex):
        self.layers[layerIndex] = self.layers[layerIndex][:startingIndex] + string + self.layers[layerIndex][startingIndex + len(string):]
    
    
    
     # Resets the specifie section of the specified layer to it's blank variant, leaving only the background
    #       INT  'layerIndex' - The index of the layer to reset
    #       INT  'sectionLength' - Length of the section to erase
    #       INT  'startingIndex' - The index on the passed layer on which the the erasing will begin
    #
    # PRECNT: 'layerIndex' must be a valid index of 'self.layers[]'
    # PRECNT: 'startingIndex' + 'sectionLength' must not exceed the final index of the layer at 'layerIndex'
    def eraseLayerSection(self, layerIndex, sectionLength, startingIndex):
        replacementString = self.worldList[self.world][layerIndex][startingIndex:startingIndex + sectionLength]
        while len(replacementString) < sectionLength:
            replacementString += self.worldList[self.world][layerIndex][:sectionLength - len(replacementString)]
        self.layers[layerIndex] = self.layers[layerIndex][:startingIndex] + replacementString + self.layers[layerIndex][startingIndex + sectionLength:]
        
    
    
    # Resets the specified layer to it's blank variant, leaving only the background
    #       INT  'layerIndex' - The index of the layer to reset
    #
    # PRECNT: 'layerIndex' must be a valid index of 'self.layers[]'
    def eraseLayer(self, layerIndex):
        layer = ""
        # If 'GUI_LENGTH' is set to be longer than preset in 'worldList[]', then it is the full preset is copied to the current 'layer' being generated
        for j in range(0,int(GUI_LENGTH/50)):
            layer += self.worldList[self.world][layerIndex]
        # Part of the preset in 'worldList[]' is appended to the current 'layer', bringing its total length up to 'GUI_LENGTH'
        layer += self.worldList[self.world][layerIndex][:GUI_LENGTH % 50]
        self.layers[layerIndex] = layer
    
    
    
    # Draws the enemy or the player in their corresponding locations
    #       PLAYER 'entity' - Player object
    #           OR
    #       ENEMY[] 'entity' - List of Enemies 
    def drawEntity(self, entity):
        # Drawing enemies
        if isinstance(entity, list):
            for e in range(0, len(entity)): # Loop through all enemies
                for i in range(0,4):           # Loop through each sprite layer in the current enemy
                    newLayer = ""
                    for j in range(0,len(entity[e].sprite[i])): # Loop through all characters in the current sprite layer
                        if entity[e].sprite[i][j] == "`":
                            newLayer += self.layers[i+1][GUI_ENEMY_INDEX + j + e*GUI_ENTITY_SPACE]
                        else:
                            newLayer += entity[e].sprite[i][j]
                    self.drawLayerSection(i+1, newLayer, GUI_ENEMY_INDEX + e*GUI_ENTITY_SPACE)
        # Drawing player
        else:
            for i in range(0,3): # Loop through each sprite layer in the player
                newLayer = ""
                for j in range(0, len(entity.sprite[i])): # Loop through all characters in the current sprite layer
                    if entity.sprite[i][j] == "`":
                        newLayer += self.layers[i+2][GUI_PLAYER_INDEX + j]
                    else:
                        newLayer += entity.sprite[i][j]
                self.drawLayerSection(i+2, newLayer, GUI_PLAYER_INDEX)
    
    
    
    # Draws the health and power of both the player and all enemies
    #   PLAYER 'player' - The player
    #   ENEMY[] 'enemyList' - The list of enemies
    def drawHealthAndPower(self, player, enemyList):
        self.eraseHealthAndPower()
        # Draw enemy health
        for e in range(0, len(enemyList)): # Loops through all enemies
            health = str(enemyList[e].HP) + "/" + str(enemyList[e].MAXHP)
            self.drawLayerSection(0, health, GUI_ENEMY_INDEX + e*GUI_ENTITY_SPACE)
        # Draw player health
        health = str(player.HP) + "/" + str(player.MAXHP)
        self.drawLayerSection(0, health, GUI_PLAYER_INDEX)
        # Draw player power
        power = str(player.PWR) + "/" + str(player.MAXPWR)
        self.drawLayerSection(1, power, GUI_PLAYER_INDEX)
    
    
    
    # Resets the health layer (0) and the power section (first part of layer 1) to their blank variants
    def eraseHealthAndPower(self):
        self.eraseLayer(0)
        self.eraseLayerSection(1, 12, 0)
    
    
    
    # Replaces each enemy drawing with the current world's background
    def eraseEnemies(self):
        for i in range(0,5):
            self.eraseLayerSection(i, GUI_LENGTH - GUI_ENEMY_INDEX, GUI_ENEMY_INDEX)

    
    
    # Draws each enemy's index
    #   ENEMY[] 'enemyList' - The list of enemies
    # Note: To erase indexes, eraseHealthAndPower() works just fine
    def drawEnemyIndex(self, enemyList):
        self.eraseHealthAndPower()
        for e in range(0,len(enemyList)):
            index = "[" + str(e+1) + "]"
            self.drawLayerSection(0, index, GUI_ENEMY_INDEX + e*GUI_ENTITY_SPACE)
