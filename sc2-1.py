from sc2.bot_ai import BotAI  # parent class MyBot inherits from (part of BurnySC2)
from sc2.data import Difficulty, Race  # difficulty & race for bots
from sc2.main import run_game  # function that facilitates running the agents in games
from sc2.player import Bot, Computer  # wrapper defining if agent is newly coded AI or computer player
from sc2 import maps  # method for loading maps
from sc2.ids.unit_typeid import UnitTypeId  # allows access to unit type IDs

""" ai_race = Race.Protoss				# coded AI's race
comp_race = Race.Zerg				# computer's race
game_diff = Difficulty.Hard			# computer palyer's difficulty
game_map = "2000AtmospheresAIE"		# map to play on

def ai_tech_tree(ai_race):			# function to 
	switcher = {
		Race.Protoss: ai_townhall = UnitTypeId.NEXUS;
			UnitTypeId.PROBE;
		Race.Zerg: UnitTypeId.HATCHERY,
		Race.Terran: UnitTypeId.COMMANDCENTER
	}
	return switcher.get(ai_race, "nothing")

ai_townhall = townhall_type(ai_race)	# AI's townhall based on chosen race (ai_race)
ai_worker = UnitTypeId.PROBE """

ai_race = Race.Protoss				# coded AI's race

def ai_tech_tree(ai_race):			# function to 
	switcher = {
		Race.Protoss: UnitTypeId.NEXUS;
			UnitTypeId.PROBE;
		Race.Zerg: UnitTypeId.HATCHERY,
		Race.Terran: UnitTypeId.COMMANDCENTER
	}
	return switcher.get(ai_race, "nothing")

ai_townhall = townhall_type(ai_race)

class MyBot(BotAI): # inherits from BotAI
	async def on_step(self, iteration: int): # method called every step of the game
		print(f"{iteration}, n_workers: {self.workers.amount}, n_idle_workers: {self.workers.idle.amount},", \
			f"minerals: {self.minerals}, gas: {self.vespene}, cannons: {self.structures(UnitTypeId.PHOTONCANNON).amount},", \
			f"pylons: {self.structures(UnitTypeId.PYLON).amount}, nexus: {self.structures(UnitTypeId.NEXUS).amount}", \
			f"gateways: {self.structures(UnitTypeId.GATEWAY).amount}, cybernetics cores: {self.structures(UnitTypeId.CYBERNETICSCORE).amount}", \
			f"stargates: {self.structures(UnitTypeId.STARGATE).amount}, voidrays: {self.units(UnitTypeId.VOIDRAY).amount}, supply: {self.supply_used}/{self.supply_cap}")
		
		# begin logic
		if self.townhalls:  # does AI have a townhall?
			nexus = self.townhalls.random  # select random AI-owned townhall
			if nexus.is_idle and self.can_afford(UnitTypeId.PROBE):  # is AI's townhall idle and can AI afford a probe?
				nexus.train(UnitTypeId.PROBE)  # train a probe
			
			elif not self.structures(UnitTypeId.PYLON) and self.already_pending(UnitTypeId.PYLON) == 0: # if AI doesn't have a pylon
				if self.can_afford(UnitTypeId.PYLON):  # and AI can afford one
					await self.build(UnitTypeId.PYLON, near=nexus)  # build a pylon near AI's nexus

			elif self.structures(UnitTypeId.PYLON).amount < 5:  # if AI has less than five pylons
				if self.can_afford(UnitTypeId.PYLON):
					# build from the closest pylon toward the enemy
					target_pylon = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0])  # find closest pylon to enemy start location
                    # build as far away from target_pylon as possible:
					pos = target_pylon.position.towards(self.enemy_start_locations[0], random.randrange(8, 15))
					await self.build(UnitTypeId.PYLON, near=pos)  # build a pylon near the position
		
		else:
			if self.can_afford(UnitTypeId.NEXUS):  # can AI afford to buld townhall?
				await self.expand_now()  # if so, build one

run_game(  # function that runs the game.
    maps.get("2000AtmospheresAIE"), # get map to use
    [Bot(Race.Protoss, MyBot()), # runs bot with selected AI race passing MyBot as bot object 
     Computer(Race.Zerg, Difficulty.Hard)], # runs a pre-made computer agent as Zerg race with difficulty of hard
    realtime = False, # When set to True, the agent is limited in how long each step can take to process
)

