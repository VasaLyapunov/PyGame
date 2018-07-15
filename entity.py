#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gamelib import *

class Entity:

    def __init__(self):

        self.EXP = 0

        self.sprite = ["NULL ENTIT"]

        self.MAXHP = 0
        self.HP = 0
        self.MAXPWR = 0
        self.PWR = 0
        self.ATK = 0
        self.DEF = 0
        self.SPD = 0
        self.LCK = 0
        
    # Takes away 'DMG[0]' amount of health. If health drop below 0, it's set to 0
    #       INT  DMG[0] - Amount of health removed
    #       BOOL DMG[1] - Was the hit piercing?
    #       BOOL DMG[2] - Was the hit critical?
    #       BOOL DMG[3] - Did the hit miss?
    def takeDamage(self, DMG):
        self.HP -= DMG
        if self.HP < 0:
            self.HP = 0
    
    
    
    # Calculates the amount of damage based on 'self's attack. Optionally also uses 'self's luck, 'target's defense, everyone's 'target's speed
    #       ENTITY 'target' - Entity that is under attack
    #       FLT  'multiplier' - Multiplies damage
    #       BOOL 'useDEF' - Calculates using 'target's defense if True (piercing)
    #       BOOL 'useLCK' - Calculates using 'self's luck if True (critical)
    #       BOOL 'useSPD' - Calculates using 'self' and target's speed if True (miss)
    def calculateAttackDamage(self, target, multiplier, useDEF, useLCK, useSPD):
        DMG = [0,0,0,0]
        
        # Calculates damage, with or without target defense
        DEF = target.DEF
        if not useDEF:
            DEF = 0
            DMG[1] = True
        vary = int(self.ATK/5.0)
        DMG[0] = self.ATK - DEF + randint(vary*-1,vary)
        DMG[0] = int(DMG[0]*multiplier)
        
        # If luck is being used, try doubling the damage dealt
        if useLCK:
            if randint(1,100) <= self.LCK:
                DMG[0] = DMG[0]*2
                DMG[2] = True
                
        # If speed is being used, see if the attack missed
        if useSPD:
            relativeSPD = target.SPD - self.SPD + 5
            if relativeSPD < 0:
                relSPD = 0
            if randint(1,100) <= relativeSPD:
                DMG[0] = 0
                DMG[3] = True
        
        # If less than 1 damage is dealt, set damage dealt to 1 (Provided that this wasn't a miss!)
        if DMG[0] < 1 and not DMG[3]:
            DMG[0] = 1
            
        return DMG
    
    # Restores HP of entity while making sure it does not surpass MAXHP
    #       INT 'HPamount' - How much HP to restore
    # Returns how much HP was actually restored 
    def restoreHP(self, HPamount):
        HPinitial = self.HP
        if HPamount + self.HP > self.MAXHP:
            self.HP = self.MAXHP
        else:
            self.HP = self.HP + HPamount
        return self.HP - HPinitial
    
    
    
    
