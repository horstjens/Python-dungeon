import random


level1 = """
##################################################
#..$$.>..s...BBa.b.G.p.E.b.$$$.$K..r.$.h..c..#D..#
#...........................................##...#
#...........:....######D####.........:.......#...#
#...????.........#..$$$$$$.#.................#...#
##################################################"""

level2 = """
##################################################
#.....<...................#.........a....s..#....#
#........$$$$$$$$$........#................#.#...#
#.......................:.#.:................#...#
#>...............B........#.......B...KKK..##....#
##################################################
"""

level3 = """
##################################################
#.....###......####.......#.........a....s.###...#
#.....#..$$$$$$$$$#...............B.........##...#
#.....###......####.....:.#.:.....B..........#...#
#<........................#.......B........###...#
##################################################
"""





#        key :   name   hunger hp
food = {"a":("apple",5,0),
        "b":("banana",6,2),
        "p":("pork",9,0),
        "r":("rotten meat",4,-2),
        "c":("cake",17,0),
        "h":("big health potion",0,42)}



class Monster():
    number = 0
    zoo = {}
    
    def __init__(self, x=0, y=1, z=0, hp=10, name = "monster",
                 tohit = 0.5, evade = 0.25, maxdamage = 3, char="?"):
        self.hp = hp
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.tohit = tohit
        self.evade = evade
        self.maxdamage = maxdamage
        self.number = Monster.number
        Monster.number += 1
        Monster.zoo[self.number] = self
        self.char = char
    
    def report(self):
        return "monster: {} hp: {} tohit: {} ev: {} maxdmg: {}".format(self.name,  self.hp, self.tohit, self.evade, self.maxdamage)
    
    def move(self):
        return 0, 0
 
class Bunny(Monster):
    def __init__(self, posx, posy, posz):
        Monster.__init__(self, posx, posy, posz, 2, "Bunny", 0.6, 0.8, 1, "B")
    
class Dog(Monster):
    def __init__(self, posx, posy, posz):
        Monster.__init__(self, posx, posy, posz, 10, "Dog", 0.4, 0.35, 3, "G")
                
class Dragon(Monster):
    def __init__(self,posx, posy, posz):
        Monster.__init__(self, posx, posy, posz, 30, "Dragon", 0.25, 0.1, 22, "D")
         
    def move(self):
        return random.choice((-1,0,1)), random.choice((-1,0,1)) # the dragon moves or waits
        
class Duck(Monster):
    def __init__(self,posx, posy, posz):
        Monster.__init__(self,posx, posy, posz, 5, "Evil Duck", 0.47, 0.23, 2, "E")
        
class Kobold(Monster):
    def __init__(self,posx, posy, posz):
        Monster.__init__(self,posx, posy, posz, 3, "Kobold", 0.8, 0.01, 1, "K")
    
    def move(self):
        return random.choice((-1,0,0,0,1)), random.choice((-1,0,0,0,1)) # kobold jumps, sometimes
        

class Hero(Monster):
    def __init__(self,posx, posy, posz):
        Monster.__init__(self,posx, posy, posz, 10, "Hero", 0.7, 0.3, 7, "@")
        self.hunger = 0
        self.money = 0

def attack(angreifer, verteidiger):
    msg = ""
    msg += "{} is attacking {}!\n".format(angreifer.name, verteidiger.name)
    attack = random.random() # 0...1
    evade = random.random()
    damage = random.randint(1, angreifer.maxdamage)
    if attack < angreifer.tohit:
         msg += "Attack successfull!!\n"
         if evade < verteidiger.evade:
             msg += "but {} can evade!\n".format(verteidiger.name)
         else:
             msg += "{} make {} damage ({} hp left)".format(angreifer.name, damage, verteidiger.hp-damage)
             verteidiger.hp -= damage
    else:
         msg += "Attack failed!\n"
    return msg

def fight(angreifer, verteidiger):
    #battleround = 0
    while True:
        #battleround += 1
        #print("---------- Battle Round {} ----------".format(battleround))
        print(attack(angreifer, verteidiger))
        if verteidiger.hp < 1:
            print("{} wins!".format(angreifer.name))
            del Monster.zoo[verteidiger.number]
            break
        print(attack(verteidiger, angreifer))
        if angreifer.hp < 1:
            print("{} wins!".format(verteidiger.name))
            break
        input("press enter")
        break 

def teleport(x, y, distance=5):
    versuch = 0
    while versuch < 1000000:
        dx = random.randint(-distance, distance)
        dy = random.randint(-distance, distance)
        if (dx**2 + dy**2)**0.5 > distance:
            continue
        try:    
            if level[y+dy][x+dx] != ".":
                continue
        except:
            continue
            
        break
    else:
        dx = 0
        dy = 0
        print("no target for teleportation found")
    return x+dx, y+dy
        
        
    
    
    
    
    
        

def shop(customer):
    msg = "number  |  potion    | price\n"
    msg +="--------+------------+-------\n"
    store = {}
    for number in range(10):
        # number : ( name, effect, price )
        store[number] = ( random.choice(("health", "tohit", "evade", "food", "maxdamage")),
                          random.randint(-1, 5),
                          random.randint(4,44) )
        msg += "     {:>2} | {:<10} | {:>3}\n".format(number, store[number][0],
                                                store[number][2])
    print(msg)
    buy = input("enter number to buy")
    try:
        buy = int(buy)
    except:
        return
    price = store[buy][2]
    if customer.money >= price:
        customer.money -= price
    else:
        print("You can not afford this price")
        return
    # ---- potion effect ----
    print(customer.report())
    print("you drink the potion and you wait for the magic effect")
    effect = store[buy][1]
    potion = store[buy][0]
    if effect == 0:
        print("the potion was rotten and has no effect at all")
    elif effect < 0:
        print("the potion was cursed and has a negative effect!")
    else:
        print("the potion works! You feel better")
    if potion == "health":
        customer.hp += effect
    elif potion == "tohit":
        customer.tohit += effect / 100
    elif potion == "evade":
        customer.evade += effect / 100
    elif potion == "food":
        customer.hunger -= effect
    elif potion == "maxdamage":
        customer.maxdamage += effect     
    print(customer.report())
        
        
        
    
     
                                        
                                                

# ------ generiere monster -------
hero = Hero(1,1,0)

levels = []
for z, levelstring in enumerate((level1, level2, level3)):
    
    level = []
    for line in levelstring.split():
        level.append(list(line))
        

    for y, line in enumerate(level):
        for x, char in enumerate(line):
            if char in "GDEKB":
                level[y][x] = "."
                if char == "G":
                    Dog(x,y,z)
                elif char == "D":
                    Dragon(x,y,z)
                elif char == "E":
                    Duck(x,y,z)
                elif char == "K":
                    Kobold(x,y,z)
                elif char == "B":
                    Bunny(x,y,z)
    
    levels.append(level)

# ------------ main loop -------------
while hero.hp > 0 and hero.hunger < 1000:
    level = levels[hero.z]
    for y, line in enumerate(level):
         for x, char in enumerate(line):
            for number in Monster.zoo:
                monster = Monster.zoo[number]
                if monster.x == x and monster.y == y and monster.z == hero.z:
                    print(monster.char, end="")
                    break
            else:
                print(char, end = "")
         print() # end of line
    hero.hunger += 1
    print("pos:", hero.x, hero.y, hero.z)
    command=input("Hunger: {} Money: {} HP: {},your command?".format(hero.hunger, hero.money, hero.hp))
    dx = 0
    dy = 0
    if command == "quit" or command == "exit" :
        break
    elif command == "a":
        dx = -1
    elif command == "d":
        dx = 1
    elif command == "w":
        dy = -1
    elif command == "s":
        dy = 1
    elif command == "D":
        dx = 2
    elif command == "A":
        dx = -2
    elif command == "superjump":
        dx = 10
    elif command == "superbackjump":
        dx = -10
    elif command == "randomjump":
        dx = random.randint(-10, 10)
    # --------legal move? ---------
    if hero.x + dx < 0 or hero.x + dx >= len(line) or hero.y < 0 or hero.y > len(level):
        print("You can not leave the level")
        dx = 0
        dy = 0
    elif level[hero.y + dy][hero.x + dx] == "#":
        dx = 0
        dy = 0
        print("You can not go through a wall")
    else:
        for monster in Monster.zoo.values():
            if monster.number == hero.number:
                continue
            elif monster.z != hero.z:
                continue
            elif monster.x == hero.x + dx and monster.y == hero.y + dy:
                if dx > 1 or dx < -1 or dy > 1 or dy < -1:
                    print("you can not jump into a monster")
                    dx = 0
                    dy = 0
                    break
                print("Kampf gegen " + monster.report())
                fight(hero, monster)
                if monster.hp < 1:
                    hero.money += random.randint(0,10)
                dx = 0
                dy = 0
                break
        else:
            hero.x += dx
            hero.y += dy
        
    # ----------Auswertung----------
    stuff = level[hero.y][hero.x]
    # ------ Rätselkiste ---- 
    if stuff == "?":
        print("you discovered a question box")
        skill = input("how hard?(1-9) 1=very easy, 9=very hard")
        if skill not in "123456789" or len(skill) != 1:
            print("stupid answer ---> very hard question!")
            skill = 11
        else:
            skill = int(skill)
        a = random.randint(1,skill)
        b = random.randint(1, skill)
        c = a * b
        answer = input("what is {} x {}?".format(a,b))
        try:
            answer = int(answer)
        except:
            answer = -1
        if answer == c:
            print("Bravo, correct!")
        else:
            print("Very bad. Very, very bad!")
        
        
    # ------ teleport --------
    if stuff == ":":
        hero.x, hero.y = teleport(hero.x, hero.y)
    # ------ stair down --------
    if stuff == ">":
        climb = input("do you want to climb down? (yes or no)")
        if climb == "yes":
            hero.z += 1
            continue
    # ------ stair up --------
    if stuff == "<":
        climb = input("do you want to climb up ? (yes or no)")
        if climb == "yes":
            hero.z -= 1
            continue
        
    # ------ food and money ------
    if stuff in food:
        print("You eat : ", food[stuff][0])
        hero.hunger -= food[stuff][1]
        hero.hp += food[stuff][2]
        level[hero.y][hero.x] = "."
    elif stuff == "$":
        print("You found money!")
        hero.money += random.randint(1, 20)
        level[hero.y][hero.x] = "."
    # -------- shop --------
    if stuff == "s":
        shop(hero)
    # -------- moving monsters -----
    print("the monsters are moving!")
    for monster in Monster.zoo.values():
        if monster.number == hero.number:
            continue 
        if monster.z != hero.z:
            continue
        dx, dy = monster.move()
        if dx == 0 and dy == 0:
            continue
        if monster.x + dx < 0 or monster.x + dx > len(line) or monster.y + dy < 0 or monster.y+dy >len(level):
            dx = 0
            dy = 0
        elif level[monster.y+dy][monster.x+dx] == "#":
            dx = 0
            dy = 0
        for monster2 in Monster.zoo.values():
            if monster2.number == monster.number:
                continue
            if monster2.z != hero.z:
                continue
            if monster.x + dx == monster2.x and monster.y+dy == monster2.y:
                dx = 0
                dy = 0
                if monster2.number == hero.number:
                    print("Angriff von wanderndem Monster")
                    fight(monster, hero)
                break
        monster.x += dx
        monster.y += dy
    
    
    
   




