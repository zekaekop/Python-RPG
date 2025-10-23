import random

class StatsBounds:

    def statLimitMax(health_stat,health_max_stat,energy_stat,energy_stat_min):
        if health_stat < health_max_stat and energy_stat-energy_stat_min >= 0:
            return True # makes sure it doesnt go above health and below 0 for health and energy
        else:
            return False

    def incStat(stat,max_stat):
        for i in range(5):
            if stat < max_stat: # restores stats on regular attacks
                stat += 1
        return stat
    
    def decStat(stat,dec_stat):
        for i in range(dec_stat):
            if stat > 0: # reduces stats on regular attacks
                stat -= 1
        return stat

class Player:

    def __init__(self, stats, id):
        self.stats = stats
        self.player_health = stats["health"]
        self.player_max_health = stats["max_health"]
        self.player_name = stats["name"]
        self.player_strength = stats["strength"]
        self.player_energy = stats["energy"]
        self.player_max_energy = stats["max_energy"]
        self.player_id = id

    def attack(self, other_enemy, special):
        damage_delt = random.uniform(self.player_strength[0],self.player_strength[1])
        
        if special["healing"] == True and StatsBounds.statLimitMax(self.player_health,self.player_max_health,self.player_energy,10):
            if self.player_health < self.player_max_health:
                self.player_health += 15
                self.player_energy = StatsBounds.decStat(self.player_energy,10)
        else:
            if special["extra_damage"] == True and self.player_energy-5 >= 0: # has energy
                other_enemy.player_health -= (damage_delt + 7) # extra
                self.player_energy = StatsBounds.decStat(self.player_energy,5)
            else:
                other_enemy.player_health -= (damage_delt)
                self.player_energy = StatsBounds.incStat(self.player_energy,self.player_max_energy)

    
    
    def sayCombatLog(self, last_health, last_energy):
        print("<======================>")
        if self.player_health <= 0:
            print(self.player_name + " Health: 0" + 
            " (" + str(round((self.player_health - last_health))) + ")")
            print(self.player_name + " Energy: 0" + 
            " (" + str((round(self.player_energy - last_energy))) + ")")
        else:
            print(self.player_name + " Health: " + str(round(self.player_health)) + 
            " (" + str((round(self.player_health - last_health))) + ")")
            print(self.player_name + " Energy: " + str(round(self.player_energy)) + 
            " (" + str((round(self.player_energy - last_energy))) + ")")

    def sayStats(self):
        print("<======================>")
        print("Player ID: " + str(self.player_id) + " | " + str(level) + " Level") 
        print("<======================>")
        print("I am " + self.player_name)
        print("Health #> " + str(round(self.player_health)))
        print("Strength #> (" + str(round(self.player_strength[0])) + "-" + str(round(self.player_strength[1])) + ")")
        print("Energy #> " + str(round(self.player_energy)))
        print("<======================>")
        print("\n")

def user_attack(user_player):
    while True:
        user_choice = input("Commands(Help): ")
        print("\n")

        if user_choice.lower() == "help":
            print("\n")
            print("#> Info: to use them eighter type the index, the name or the first capital letters example(1,Special Attack,SA)")
            print("#> [1]Special Attack - +7 Base damage | -5 Energy")
            print("#> [2]Self Healing - +15 Health | -10 Energy")
            print("\n")
            print("#> Continue - Regular attack")
            print("#> Inspect - Current stats")
            print("\n")
            continue


        match(user_choice.lower()):
            case "0"|"inspect"|"i":
                user_player.sayStats()
            case "1"|"special attack"|"sa":
                print("#> Extra Damage")
                print("\n")
                return {"extra_damage" : True,
                        "healing" : False,}
            case "2"|"self healing"|"sh":
                print("#> Healing")
                print("\n")
                return {"extra_damage" : False,
                        "healing" : True,}
            case _:
                print("#> Attack")
                print("\n")
                return {"extra_damage" : False,
                        "healing" : False,}


global names 
names = ["Centaurs","Lynx","Cyclopes","Hydras","Phoenix","Ouroburo","Hero"]

def rngStats(power_scale):
    health = random.uniform(100,200)
    max_health = health

    energy = random.uniform(25,50)
    max_energy = energy

    strength_min = random.uniform(5,15)
    strength_max = random.uniform(strength_min+1,(strength_min*2))
    strength_range = [strength_min, strength_max]
    
    
    picked_name = random.randrange(0,len(names))
    name = names[picked_name]

    stats = {
            "health":health,
             "max_health":max_health,
             "name":name,
             "strength":strength_range,
             "energy":energy,
             "max_energy":max_energy
             }
    
    stats = increase_stats(stats, power_scale)
            
    return stats

def increase_stats(stats, power_scale):
    for stat,value in stats.items():
        if isinstance(value, float):
            stats[stat] = value * power_scale
    
    return stats

def combat(user_player,enemy_player,special):
    last_health_1 = user_player.player_health
    last_health_2 = enemy_player.player_health
    last_energy_1 = user_player.player_energy
    last_energy_2 = enemy_player.player_energy

    user_player.attack(enemy_player,special)
    enemy_player.attack(user_player,{"extra_damage" : False, "healing" : False,}) # for now the enemy has no special
    
    user_player.sayCombatLog(last_health_1,last_energy_1)
    enemy_player.sayCombatLog(last_health_2,last_energy_2)
    print("<======================>")




def Main():
    pickable_players = []
    spawn_player_count = 3

    global power_scale, scale, level # powerscale is the difficulty
    power_scale = 1.0
    scale = 0.2
    level = 1

    for id in range(spawn_player_count): # spawn players
        pickable_players.append(Player(rngStats(power_scale),id)) # rng = randomly generated

    for i in range(spawn_player_count): # list players to user
        pickable_players[i].sayStats()

    while True:
        user_picked_player = int(input("Choose your Player (ID): "))
        if user_picked_player < spawn_player_count and user_picked_player >= 0:
            break


    user_player = pickable_players[user_picked_player]
    print("\n") 
    
    while True:
        level += 1

        saved_player = (user_player.stats,user_player.player_id)

        scale += scale

        enemy_player = Player(rngStats(power_scale+scale),id) # increases the mobs health

        # we no longer use enemies from user choices
        # del pickable_players[user_picked_player] # deletes the picked player so the enemy doesnt get the same character
        #enemy_player = pickable_players[random.randrange(0,(spawn_player_count-1))]

        while True:

            if user_player.player_health > 0 and enemy_player.player_health > 0: # checks if the game is over
                special = user_attack(user_player)
                combat(user_player,enemy_player,special)
                print("\n")
            else:
                break

        if user_player.player_health > 0:
            print(user_player.player_name + "/User" + " Wins! (+1 Level)")
            print("\n")
            stats = increase_stats(saved_player[0],(power_scale+(scale-0.1)))
            user_player = Player(stats,saved_player[1])
            user_player.sayStats()
            
        else:
            print(enemy_player.player_name + "/Enemy" + " Wins!")
            break

if __name__ == "__main__":
    Main()