import random
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

def ai_tech_tree(ai_type):			# function to 
	switcher = {
		Race.Protoss: ai_townhall = UnitTypeId.NEXUS;
			ai_worker = UnitTypeId.PROBE,
		Race.Zerg: ai_townhall = UnitTypeId.HATCHERY;
			ai_worker = UnitTypeId.DRONE,
		Race.Terran: ai_townhall = UnitTypeId.COMMANDCENTER;
			ai_worker = UnitTypeId.SCV
	}
	return switcher.get(ai_race, "nothing")

ai_townhall = ai_tech_tree(ai_race)	# AI's townhall based on chosen race (ai_race)
ai_worker = ai_tech_tree(ai_race)	#  AI's worker based on chosen race (ai_race)"""

""" ai_race = Race.Protoss				# coded AI's race

def get_ai_townhall(ai_type):			# function to determine townhall type based on chosed race (ai_race)
	switcher = {
		Race.Protoss: UnitTypeId.NEXUS,
		Race.Zerg: UnitTypeId.HATCHERY,
		Race.Terran: UnitTypeId.COMMANDCENTER
	}
	return switcher.get(ai_race, "nothing")

def get_ai_worker(ai_type):			# function to determine townhall type based on chosed race (ai_race)
	switcher = {
		Race.Protoss: UnitTypeId.NEXUS,
		Race.Zerg: UnitTypeId.HATCHERY,
		Race.Terran: UnitTypeId.COMMANDCENTER
	}
	return switcher.get(ai_race, "nothing")

ai_townhall = get_ai_townhall(ai_race)	# AI's townhall
ai_worker = get_ai_worker(ai_race)		# AI's worker """

""" def ai_tech_tree(ai_type):			# function to 
	switcher = {
		Race.Protoss: setattr(UnitTypeId, NEXUS);
			ai_worker = UnitTypeId.PROBE,
		Race.Zerg: ai_townhall = UnitTypeId.HATCHERY;
			ai_worker = UnitTypeId.DRONE,
		Race.Terran: ai_townhall = UnitTypeId.COMMANDCENTER;
			ai_worker = UnitTypeId.SCV
	} """

class MyBot(BotAI): # inherits from BotAI
	async def on_step(self, iteration: int): # method called every step of the game
		print(f"{iteration}, n_workers: {self.workers.amount}, n_idle_workers: {self.workers.idle.amount},", \
			f"minerals: {self.minerals}, gas: {self.vespene}, cannons: {self.structures(UnitTypeId.PHOTONCANNON).amount},", \
			f"pylons: {self.structures(UnitTypeId.PYLON).amount}, nexus: {self.structures(UnitTypeId.NEXUS).amount}", \
			f"gateways: {self.structures(UnitTypeId.GATEWAY).amount}, cybernetics cores: {self.structures(UnitTypeId.CYBERNETICSCORE).amount}", \
			f"stargates: {self.structures(UnitTypeId.STARGATE).amount}, voidrays: {self.units(UnitTypeId.VOIDRAY).amount}, supply: {self.supply_used}/{self.supply_cap}")
		
		# begin logic
		await self.distribute_workers() # put idle workers to work

		if self.townhalls:  # does AI have a townhall?
			nexus = self.townhalls.random  # select random AI-owned townhall
			
			# if AI has less than 10 voidrays, build one:
			if self.structures(UnitTypeId.VOIDRAY).amount < 10 and self.can_afford(UnitTypeId.VOIDRAY):
				for sg in self.structures(UnitTypeId.STARGATE).ready.idle:
					if self.can_afford(UnitTypeId.VOIDRAY):
						sg.train(UnitTypeId.VOIDRAY)

			# leave room to build void rays:
			supply_remaining = self.supply_cap - self.supply_used
			if nexus.is_idle and self.can_afford(UnitTypeId.PROBE) and supply_remaining > 4 and self.units(UnitTypeId.PROBE).amount < 26:
				nexus.train(UnitTypeId.PROBE)
			
			# if AI has less than 5 Pylons, build one close to nexus:
			elif not self.structures(UnitTypeId.PYLON) and self.already_pending(UnitTypeId.PYLON) == 0: # if AI doesn't have a pylon
				if self.can_afford(UnitTypeId.PYLON):  # and AI can afford one
					await self.build(UnitTypeId.PYLON, near = nexus)  # build a pylon near AI's nexus

			# if AI has less than 5 Cybernetics cores, build one close to nexus:
			elif self.structures(UnitTypeId.PYLON).amount < 5:  # if AI has less than five pylons
				if self.can_afford(UnitTypeId.PYLON): # and AI can afford one
					# build from the closest pylon toward the enemy
					target_pylon = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0])  # find closest pylon to enemy start location
					# build as far away from target_pylon as possible:
					#pos = target_pylon.position.towards(self.enemy_start_locations[0], random.randrange(8, 15))
					await self.build(UnitTypeId.PYLON, near = nexus)  # build a pylon near the position

			# if AI has one or less assimilators, build one close to nexus:
			elif self.structures(UnitTypeId.ASSIMILATOR).amount <= 1:
				for nexus in self.structures(UnitTypeId.NEXUS):
					vespenes = self.vespene_geyser.closer_than(15, nexus)
					for vespene in vespenes:
						if self.can_afford(UnitTypeId.ASSIMILATOR) and not self.already_pending(UnitTypeId.ASSIMILATOR):
							await self.build(UnitTypeId.ASSIMILATOR, vespene)
							
			# if AI doesn't have a forge, build one close to nexus:
			elif not self.structures(UnitTypeId.FORGE):  # if AI doesn't have a forge:
				if self.can_afford(UnitTypeId.FORGE):  # and AI can afford one:
					# build one near the Pylon that is closest to the nexus:
					await self.build(UnitTypeId.FORGE, near = self.structures(UnitTypeId.PYLON).closest_to(nexus)) # if so, 

			# if AI has less than three canons, build one close to nexus:
			elif self.structures(UnitTypeId.FORGE).ready and self.structures(UnitTypeId.PHOTONCANNON).amount < 3: # if AI has Forge and less than 3 cannons
				if self.can_afford(UnitTypeId.PHOTONCANNON):  # can AI afford a cannon?
					await self.build(UnitTypeId.PHOTONCANNON, near = nexus)  # if so, build one near the nexus
		
			# if AI doesn't have a gateway, build one close to nexus:
			elif not self.structures(UnitTypeId.GATEWAY):
				if self.can_afford(UnitTypeId.GATEWAY):
					await self.build(UnitTypeId.GATEWAY, near = self.structures(UnitTypeId.PYLON).closest_to(nexus))
			
			# if AI doesn't have a cyber core, build one close to a pylon near nexus:
			elif not self.structures(UnitTypeId.CYBERNETICSCORE):
				if self.can_afford(UnitTypeId.CYBERNETICSCORE):
					await self.build(UnitTypeId.CYBERNETICSCORE, near = self.structures(UnitTypeId.PYLON).closest_to(nexus))

			# if AI doesn't have a stargate, build one close to a pylon near nexus:
			elif not self.structures(UnitTypeId.STARGATE):
				if self.can_afford(UnitTypeId.STARGATE):
					await self.build(UnitTypeId.STARGATE, near = self.structures(UnitTypeId.PYLON).closest_to(nexus))

			# if AI has less than 10 Pylons, build one close to nexus:
			elif self.structures(UnitTypeId.PYLON).amount < 10:  # if AI has less than ten pylons
				if self.can_afford(UnitTypeId.PYLON): # and AI can afford one
					# build from the closest pylon toward the enemy
					target_pylon = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0])  # find closest pylon to enemy start location
					# build as far away from target_pylon as possible:
					pos = target_pylon.position.towards(self.enemy_start_locations[0], random.randrange(8, 15))
					await self.build(UnitTypeId.PYLON, near = pos)  # build a pylon near the position

		else:
			if self.can_afford(UnitTypeId.NEXUS):  # can AI afford to buld townhall?
				await self.expand_now()  # if so, build one

		# if AI has more than 3 voidrays, attack! prioritize units over buildings!
		if self.units(UnitTypeId.VOIDRAY).amount >= 3:
			# prioritize attacking known enemy units:
			if self.enemy_units:
				for vr in self.units(UnitTypeId.VOIDRAY).idle:
					vr.attack(random.choice(self.enemy_units))
			# then attack known enemy buildings:
			elif self.enemy_structures:
				for vr in self.units(UnitTypeId.VOIDRAY).idle:
					vr.attack(random.choice(self.enemy_structures))

			# otherwise attack enemy starting position
			else:
				for vr in self.units(UnitTypeId.VOIDRAY).idle:
					vr.attack(self.enemy_start_locations[0])

run_game(  # function that runs the game.
	maps.get("2000AtmospheresAIE"), # get map to use
	[Bot(Race.Protoss, MyBot()), # runs bot with selected AI race passing MyBot as bot object 
	 Computer(Race.Zerg, Difficulty.Hard)], # runs a pre-made computer agent as Zerg race with difficulty of hard
	realtime = False, # When set to True, the agent is limited in how long each step can take to process
)

