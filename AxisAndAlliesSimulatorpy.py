# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 15:31:52 2022

@author: mdavi
"""
import random as rand
from enum import Enum

class AttackType(Enum):
    LAND = 1
    SEA = 2
    AQUATIC_ASSAULT = 3

class unit:
    
    def dice(self):
        return rand.randint(1,7)
    
    def __init__(self, health=1, attackRate=1, defenseRate=1):
        self.health = health
        self.attackRate = attackRate
        self.defenseRate = defenseRate
        self.alive = True
        self.justDied = False
    
    def attack(self):
        if (not self.alive):
            return False
        return self.dice() <= self.attackRate
    
    def defend(self):
        if (not self.alive):
            if (self.justDied):
                self.justDied = False
                return self.dice() <= self.defenseRate
            return False
        return self.dice() <= self.defenseRate
    
    def hit(self):
        self.health -= 1
        if (self.alive):
            self.alive = self.health > 0
            if (not self.alive):
                self.justDied = True
    
    def isAlive(self):
        return self.alive
    
    def isJustDead(self):
        return self.justDied
    
class seaunit(unit):
    
    def __init__(self, health=1, attackRate=1, defenseRate =2):
        super().__init__(health=health, attackRate=attackRate, defenseRate=defenseRate)
        self.firstTurn = True
        
    def attack(self, attacktype):
        if (attacktype == AttackType.LAND):
            return False
        elif (attacktype == AttackType.AQUATIC_ASSAULT):
            return self.aquaticassault()
        else:
            return self.attack()
    
    def aquaticassault(self):
        if self.firstTurn:
            self.firstTurn = False
            return self.attack()
        return False
    
    def defend(self, attacktype):
        if (attacktype == AttackType.LAND):
            return False
        else:
            return super().defend()
     
        
class landunit(unit):
    def __init__(self, health=1, attackRate=1, defenseRate =2):
        super().__init__(health=health, attackRate=attackRate, defenseRate=defenseRate)
        
    def attack(self, attacktype):
        if (attacktype == AttackType.SEA):
            return False
        else:
            return super().attack()
    
    def defend(self, attacktype):
        if (attacktype == AttackType.SEA):
            return False
        else:
            return super().defend()
    
    
class airunit(unit):
    def __init__(self, health=1, attackRate=1, defenseRate =2):
        super().__init__(health=health, attackRate=attackRate, defenseRate=defenseRate)
        
    def attack(self, attacktype):
        return self.attack()
    
    def defend(self, attacktype):
        return self.defend()
        
class infantry(landunit):
    def __init__(self):
        super().__init__(health=1, defenseRate=2)
        
class infantryWithArt(landunit):
    def __init__(self):
        super().__init__(health=1, attackRate=2, defenseRate=2)
    
class artillery(landunit):
    def __init__(self):
        super().__init__(health=1, attackRate=2, defenseRate=2)
        
class tank(unit):
    def __init__(landunit):
        super().__init__(health=1, attackRate=3, defenseRate=3)

class antiaircraft(landunit):
    def __init__(self):
        super().__init__(health=1, attackRate=0, defenseRate=1)

class fighter(airunit):
    def __init__(self):
        super().__init__(health=1, attackRate=3, defenseRate=4)
        
class bomber(airunit):
    def __init__(self):
        super().__init__(health=1, attackRate=4, defenseRate=1)
        
class submarine(seaunit):
    def __init__(self):
        super().__init__(health=1, attackRate=2, defenseRate=1)
        self.firstTurn = True
    
    def sneakattack(self):
        if(self.firstTurn):
            self.firstTurn = False
            return self.dice() > self.attackRate
        return False
 
           
class destroyer(seaunit):
    def __init__(self):
        super().__init__(health=1, attackRate=2, defenseRate=2)

class cruiser(seaunit):
    def __init__(self):
        super().__init__(health=1, attackRate=3, defenseRate=3)

class aircraftCarrier(seaunit):
    def __init__(self):
        super().__init__(health=1, attackRate=1, defenseRate=2)
        
class battleship(seaunit):
    def __init__(self):
        super().__init__(health=2, attackRate=4, defenseRate=4)
        

class team:
    def __init__(self):
        self.troops = []
        
    def addTroop(self, troop:unit):
        self.troops.append(troop)
        
    def hasLivingTroops(self):
        for troop in self.troops:
            if troop.isAlive():
                return True
            
    def removeTroops(self, dead:int):
        for i in range(0, dead):
            for troop in self.troops:
                if troop.health > 1:
                    troop.hit()
            for troop in self.troops:
                if troop.isAlive():
                    troop.hit()
                    break

class defenders(team):
    def __init__(self):
        super().__init__()
        
    def defend(self, attacktype):
        hit = 0
        for troop in self.troops:
            if (troop.isAlive() or troop.isJustDead()):
                if (troop.defend(attacktype)): 
                    hit+= 1
        return hit
    
class attackers(team):
    def __init__(self):
        super().__init__()
        
    def attack(self, attacktype):
        hit = 0
        for troop in self.troops:
            if (troop.isAlive and isinstance(troop, submarine)):
                if (troop.sneakattack()):
                    hit += 1
            if (troop.isAlive()):
                if (troop.attack(attacktype)):
                    hit += 1
        return hit

def createAttackers(troops):
    attack = attackers()
    
    for troop in troops:
        attack.addTroop(troop())
    return attack
    
def createDefenders(troops):
    defend = defenders()
    
    for troop in troops:
        defend.addTroop(troop())
    return defend
    
def remaining(player:team):
    types = [infantry, infantryWithArt, artillery, tank, antiaircraft, fighter, bomber, submarine, destroyer, cruiser, aircraftCarrier, battleship]
    count = [0] * len(types)
    for i in range(0, len(types)):
        for troop in player.troops:
            if troop.isAlive() and isinstance(troop, types[i]):
                count[i] += 1
    return count
            
def generateTroops(infantries=0, artilleries=0, tanks=0, antiaircrafts=0, fighters=0,
                   bombers=0, submarines=0, destroyers=0, cruisers=0, aircraftCarriers=0, battleships=0):
    troops = []
    if (artilleries > 0): 
        troops += [infantryWithArt] * infantries
    else:
        troops += [infantry] * infantries 
    troops += [artillery] * artilleries
    troops += [tank] * tanks
    troops += [antiaircraft] * antiaircrafts
    troops += [fighter] * fighters
    troops += [bomber] * bombers
    troops += [submarine] * submarines
    troops += [destroyer] * destroyers
    troops += [cruiser] * cruisers
    troops += [aircraftCarrier] * aircraftCarriers
    troops += [battleship] * battleships
    return troops

def attackingArmy(infantries=0, artilleries=0, tanks=0, antiaircrafts=0, fighters=0,
                   bombers=0, submarines=0, destroyers=0, cruisers=0, aircraftCarriers=0, battleships=0):
    troops = []
    if (artilleries > 0): 
        troops += [infantryWithArt] * infantries
    else:
        troops += [infantry] * infantries 
    troops += [artillery] * artilleries
    troops += [tank] * tanks
    troops += [antiaircraft] * antiaircrafts
    troops += [fighter] * fighters
    troops += [bomber] * bombers
    troops += [submarine] * submarines
    troops += [destroyer] * destroyers
    troops += [cruiser] * cruisers
    troops += [aircraftCarrier] * aircraftCarriers
    troops += [battleship] * battleships
    return troops

def defendingArmy(infantries=0, artilleries=0, tanks=0, antiaircrafts=0, fighters=0,
                       bombers=0, submarines=0, destroyers=0, cruisers=0, aircraftCarriers=0, battleships=0):
    troops = []
    troops += [antiaircraft] * antiaircrafts
    troops += [bomber] * bombers
    troops += [submarine] * submarines
    troops += [infantry] * infantries
    troops += [artillery] * artilleries
    troops += [destroyer] * destroyers
    troops += [aircraftCarrier] * aircraftCarriers
    troops += [tank] * tanks
    troops += [cruiser] * cruisers
    troops += [fighter] * fighters
    troops += [battleship] * battleships
    return troops

    
def printResults(player, sims, wins, start, remain):
    print(player, "wins:", round(wins/sims * 100, 2), "%")
    for i in range(0, len(start)):
        if wins != 0:
            remain[i] = remain[i] / wins
    print(start)
    print(remain)

def singleGame(att, dfnd, attacktype):
    while att.hasLivingTroops() and dfnd.hasLivingTroops():
        killedByAttackers = att.attack(attacktype)
        dfnd.removeTroops(killedByAttackers)
        killedByDefenders = dfnd.defend(attacktype)
        att.removeTroops(killedByDefenders)

def simulator(sims, attTroops, defendTroops, attacktype=AttackType.LAND):
    attackwin = 0
    defendwin = 0
    attackstart = remaining(createAttackers(attTroops))
    defendstart = remaining(createDefenders(defendTroops))
    attackleft = [0] * len(attackstart)
    defendleft = [0] * len(defendstart)
    for i in range(0, sims):
        att = createAttackers(attTroops)
        defend = createDefenders(defendTroops)
        singleGame(att, defend, attacktype)
        if att.hasLivingTroops():
            attackwin += 1
            remain = remaining(att)
            for i in range(0, len(attackleft)):
                attackleft[i] += remain[i]
        if defend.hasLivingTroops():
            defendwin += 1
            remain = remaining(defend)
            for i in range(0, len(defendleft)):
                defendleft[i] += remain[i]
    printResults(player="Attacker", sims=sims, wins=attackwin, start=attackstart, remain=attackleft)
    printResults(player="Defender", sims=sims, wins=defendwin, start=defendstart, remain=defendleft)           