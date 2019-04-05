# coding: utf-8
# Modules needed to run the program.
import math
import requests
import os
import codecs
import re
import time
import datetime
from itertools import repeat
from lxml import html

start_time = time.time()
# -------------------------------------------------------------------------------------------------------------------------------- #
#                                                  PokéScraper by /u/AgentKazy                                                     #
# -------------------------------------------------------------------------------------------------------------------------------- #
#                                              Special thanks to /u/KoenigDerLuegner                                               #
# -------------------------------------------------------------------------------------------------------------------------------- #
# Output directory, create if it doesn't exist.
outdir = os.path.dirname(os.path.abspath(__file__))+'\\PokeScraper' # Absolute path to PokeScraper folder. Same path as the script.
if not os.path.isdir(outdir): # If folder is missing...
    os.makedirs(outdir, exist_ok=True) # ...create folder...
    print('PokeScraper folder created because it was missing.') # ...and print that it was successfuly created.
# Output file, create if it doesn't exist.
output = outdir + '\\Resource.txt' # Absolute path to folder + file.
if not os.path.isfile(output): # If file is missing...
	open(output, 'x') # ...create file...
	print('File created at: ' + output) # ...and print that it was successfuly created.
# Open file.
f = codecs.open(output, 'w', 'utf-8') # Open file in 'Write mode' and 'UTF-8' encoding.
# -------------------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                                  #
# -------------------------------------------------------------------------------------------------------------------------------- #
# Create resource cell names.
f.write('Pokémon' + '\t' + 'Dex' + '\t' + 'Male' + '\t' + 'Female' + '\t' + 'Type 1' + '\t' + 'Type 2' + '\t' + 'Hatch Steps' + '\t' + 'Egg Group 1' + '\t' + 'Egg Group 2' + '\t' + 'Ability 1' + '\t' + 'Ability 2' + '\t' + 'Hidden Ability' + '\t' + 'Special Ability' + ('\t' + 'Egg Moves')*19 + '\t' + 'Egg Moves 1-String' + '\r\n')

def main(): # Define main() function.
	# Link to Pokémon's Serebii page.
	url = "https://www.serebii.net/pokedex-sm/{0:0>3}.shtml" # ':0>3' Adds leading zeros if number has less than 3 characters. https://pyformat.info/
	special = ["001"] # List of Pokémon to test.
	# Using a range starting in 1 and ending in 809.
	for i in range(1, 810): # Loop main() for every number in the range.
		dex = ('{:0>3}'.format(i)) # Get value of the range that is in position 'i'.
		newurl = url.format(dex) # Format new url using value from list 'special'.
		# Get page for the Pokémon.
		page = requests.get(newurl) # Request the url's page...
		tree = html.fromstring(page.content) # Get the page content into a tree format.
		# -------------------------------------------------------------------------------------------------------------------------------- #
		#                                                                                                                                  #
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Gather Pokémon's information using XPath.
		name = tree.xpath('//div[@id="menu"]//td[contains(@class, "tooltabhead") and contains(text(), "Name")]//ancestor::table[@class="tooltab"]//tr/td[@class="tooltabcon"]/text()')[0] # Name.
		formNames = tree.xpath('//td[contains(text(), "Alternate Forms")]//ancestor::table[@class="dextable"]//tr/td[@class="fooinfo"]/table/tr/td[@class="pkmn"]/b/text()') # List of form names.
		malePercent = tree.xpath('number(substring-before(//font[text()="♂"]/../following-sibling::td/text(), "%"))') # Male Ratio %.
		types = tree.xpath('//td[@class="cen"]/a/img[contains(@src, "type")]/@alt') # Types.
		if types: type1 = ((types[0].replace('-type', '')).capitalize()) # Print [Type1] without '-type' and capitalized.
		if types: type2 = ((types[1].replace('-type', '')).capitalize() if len(types) >= 2 else '----') # [Type 2] if it has 2 types, without '-type' and capitalized, else prints '----' for [Type 2].
		hatchSteps = tree.xpath('//table[2]/tr[2]/td[2]/font/div[2]/div/table/tr[4]/td[5]/text()')[0] # Hatch Steps required to hatch egg.
		eggGroups = tree.xpath('//form[@name="breed" or @name="breed2"]/select/option[1]/text()') # Egg Groups.
		allabilities = tree.xpath('//table[@class="dextable"][2]/tr/td[@class="fooinfo"]/a[contains(@href, "abilitydex")][not(preceding-sibling::b)]//b/text()') # Ability list.
		abilities = ["Compound Eyes" if x=="Compoundeyes" else "Lightning Rod" if x=="Lightningrod" else x for x in allabilities]
		allhiddenAbility = tree.xpath('//table[@class="dextable"]/tr/td[@class="fooinfo"]//b[text()="Hidden Ability" or text()="Dream World Ability"]/following-sibling::a[contains(@href, "abilitydex")][not(preceding-sibling::b[contains(text(),"Alola")])]/b/text()') # Hidden Ability.
		hiddenAbility = ["Compound Eyes" if x=="Compoundeyes" else "Lightning Rod" if x=="Lightningrod" else x for x in allhiddenAbility]
		allalolaHA = tree.xpath('//table[@class="dextable"]/tr/td[@class="fooinfo"]/b[text()="Hidden Ability" or text()="Dream World Ability"]/following-sibling::b[contains(text(),"Alola")]//following-sibling::b[text()="Hidden Ability"]//following-sibling::a[contains(@href, "abilitydex")]/b/text()') # Alola Hidden Ability.
		alolaHA = ["Compound Eyes" if x=="Compoundeyes" else "Lightning Rod" if x=="Lightningrod" else x for x in allalolaHA]
		specialAbility = tree.xpath('//table[@class="dextable"]/tr/td[@class="fooinfo"]//b[text()="Special Ability"]/following-sibling::a[position()=1]/b/text()') # Special Ability.
		# Hardcoded, no real need for this XPath... genderDif = tree.xpath('//table[@class="dextable"]/tr/td[@class="fooevo"][text()="Gender Differences"]') # Gender Differences.
		# -------------------------------------------------------------------------------------------------------------------------------- #
		#                                                                                                                                  #
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Mega evolutions.
		megaEvo = tree.xpath('count(//table[@class="dextable"]/tr/td[@class="fooevo"]/font/b[contains(text(), "Mega Evolution")][not(ancestor::li[(contains(@title,"Go"))])])') # Mega Evolution.
		# Mega evolution types.
		megaTypesX = tree.xpath('//td[contains(@class,"fooinfo") and contains(text(), "Mega") and contains(text(), "X")][not(ancestor::li[(contains(@title,"Go"))])]//following-sibling::td[@class="cen"][1]/a/img[contains(@src, "type")]/@src') # Mega X types.
		if megaTypesX: typeX1 = (((megaTypesX[0].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize()) # Print [Type1] without '-type' and capitalized.
		if megaTypesX: typeX2 = (((megaTypesX[1].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize() if len(megaTypesX) >= 2 else '----') # [Type 2] if it has 2 types, without '/pokedex-bw/type/' and '.gif' and capitalized, else prints '----' for [Type 2].
		megaTypesY = tree.xpath('//td[contains(@class,"fooinfo") and contains(text(), "Mega") and contains(text(), "Y")][not(ancestor::li[(contains(@title,"Go"))])]//following-sibling::td[@class="cen"][1]/a/img[contains(@src, "type")]/@src') # Mega Y types.
		if megaTypesY: typeY1 = (((megaTypesY[0].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize()) # Print [Type1] without '-type' and capitalized.
		if megaTypesY: typeY2 = (((megaTypesY[1].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize() if len(megaTypesY) >= 2 else '----') # [Type 2] if it has 2 types, without '/pokedex-bw/type/' and '.gif' and capitalized, else prints '----' for [Type 2].
		megaTypesAll = tree.xpath('//td[contains(@class,"fooinfo") and contains(text(), "Mega")][not(ancestor::li[(contains(@title,"Go"))])]//following-sibling::td[@class="cen"][1]/a/img[contains(@src, "type")]/@src') # Mega types.
		if megaTypesAll: megaType1 = (((megaTypesAll[0].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize()) # Print [Type1] without '-type' and capitalized.
		if megaTypesAll: megaType2 = (((megaTypesAll[1].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize() if len(megaTypesAll) >= 2 else '----') # [Type 2] if it has 2 types, without '/pokedex-bw/type/' and '.gif' and capitalized, else prints '----' for [Type 2].
		# Mega evolution abilities.
		allmegaAbilities = tree.xpath('//td[@class="fooevo"]/font/b[contains(text(), "Mega Evolution")][not(ancestor::li[(contains(@title,"Go"))])]//ancestor::table[@class="dextable"]/following-sibling::table[@class="dextable"][position()=1]/tr/td[@class="fooleft"]/a[contains(@href, "abilitydex")]/b/text()')
		megaAbilities = ["Compound Eyes" if x=="Compoundeyes" else "Lightning Rod" if x=="Lightningrod" else x for x in allmegaAbilities]
		if megaAbilities: megaAbility1 = megaAbilities[0]
		if megaAbilities: megaAbility2 = megaAbilities[1] if len(megaAbilities) == 2 else '----'
		# -------------------------------------------------------------------------------------------------------------------------------- #
		#                                                                                                                                  #
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Ultra Burst.
		ultraEvo = tree.xpath('count(//table[@class="dextable"]/tr/td[@class="fooevo"]/font/b[contains(text(), "Ultra Burst")][not(ancestor::li[(contains(@title,"Go"))])])') # Ultra Burst.
		# Ultra Burst types.
		ultraTypesAll = tree.xpath('//td[contains(@class,"fooinfo") and contains(text(), "Ultra")][not(ancestor::li[(contains(@title,"Go"))])]//following-sibling::td[@class="cen"][1]/a/img[contains(@src, "type")]/@src') # Ultra types.
		if ultraTypesAll: ultraType1 = (((ultraTypesAll[0].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize()) # Print [Type1] without '-type' and capitalized.
		if ultraTypesAll: ultraType2 = (((ultraTypesAll[1].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize() if len(ultraTypesAll) >= 2 else '----') # [Type 2] if it has 2 types, without '/pokedex-bw/type/' and '.gif' and capitalized, else prints '----' for [Type 2].
		# Ultra Burst abilities.
		ultraAbilities = tree.xpath('//td[@class="fooevo"]/font/b[contains(text(), "Ultra Burst")][not(ancestor::li[(contains(@title,"Go"))])]//ancestor::table[@class="dextable"]/following-sibling::table[@class="dextable"][position()=1]/tr/td[@class="fooleft"]/a[contains(@href, "abilitydex")]/b/text()')
		if ultraAbilities: ultraAbility1 = ultraAbilities[0]
		if ultraAbilities: ultraAbility2 = ultraAbilities[1] if len(ultraAbilities) == 2 else '----'
		# -------------------------------------------------------------------------------------------------------------------------------- #
		#                                                                                                                                  #
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Primal Reversion.
		primalEvo = tree.xpath('count(//table[@class="dextable"]/tr/td[@class="fooevo"]/font/b[contains(text(), "Primal Reversion")][not(ancestor::li[(contains(@title,"Go"))])])') # Primal Reversion.
		# Primal Reversion types.
		primalTypesAll = tree.xpath('//td[contains(@class,"fooinfo") and contains(text(), "Primal")][not(ancestor::li[(contains(@title,"Go"))])]//following-sibling::td[@class="cen"][1]/a/img[contains(@src, "type")]/@src') # Primal types.
		if primalTypesAll: primalType1 = (((primalTypesAll[0].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize()) # Print [Type1] without '-type' and capitalized.
		if primalTypesAll: primalType2 = (((primalTypesAll[1].replace('/pokedex-bw/type/', '')).replace('.gif', '')).capitalize() if len(primalTypesAll) >= 2 else '----') # [Type 2] if it has 2 types, without '/pokedex-bw/type/' and '.gif' and capitalized, else prints '----' for [Type 2].
		# Primal Reversion abilities.
		primalAbilities = tree.xpath('//td[@class="fooevo"]/font/b[contains(text(), "Primal Reversion")][not(ancestor::li[(contains(@title,"Go"))])]//ancestor::table[@class="dextable"]/following-sibling::table[@class="dextable"][position()=1]/tr/td[@class="fooleft"]/a[contains(@href, "abilitydex")]/b/text()')
		if primalAbilities: primalAbility1 = primalAbilities[0]
		if primalAbilities: primalAbility2 = primalAbilities[1] if len(primalAbilities) == 2 else '----'
		# -------------------------------------------------------------------------------------------------------------------------------- #
		#                                                                                                                                  #
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Egg moves.
		eggmovesAlola = tree.xpath('//td[contains(text(), "Egg Moves")]//ancestor::table[@class="dextable"][1]//img[@alt="Alola Form"]//ancestor::tr[1]//a[contains(@href, "attackdex")]/text()') # Alolan forms egg moves.
		eggmovesAlola.sort() # Sort the Alolan egg moves list.
		if (len(eggmovesAlola) < 1): # If the Pokémon does not have Alolan Egg Moves.
			eggmoves = tree.xpath('//td[contains(text(), "Egg Moves")]//ancestor::table[@class="dextable"][1]//a[contains(@href, "attackdex")]/text()') # Normal egg moves.
			eggmoves.sort() # Sort the normal egg moves list.
		else:
			eggmoves = tree.xpath('//td[contains(text(), "Egg Moves")]//ancestor::table[@class="dextable"][1]//img[@alt="Normal"]//ancestor::tr[1]/td[@class="fooinfo"]/a[contains(@href, "attackdex")]/text()') # Normal egg moves for Pokémon with Alolan Forms.
			eggmoves.sort() # Sort the normal egg moves list.
		# Set egg moves lists to 19 elements.
		normalEM = eggmoves + ['']*(19 - len(eggmoves)) # Append [BLANK] to list so it has 19 elements.
		alolanEM = eggmovesAlola + ['']*(19 - len(eggmovesAlola)) # Append [BLANK] to list so it has 19 elements.
		# Set normal egg moves One-String.
		if (len(eggmoves) >= 1): # If eggmoves has at least 1 value.
			normalEMstring = '|' + '|'.join(map(str,eggmoves)) + '|' # Create a One-String with all egg moves.
		else:
			normalEMstring = ''
		# Set alolan egg moves One-String.
		if (len(eggmovesAlola) >= 1): # If eggmovesAlola has at least 1 value.
			alolaEMstring = '|' + '|'.join(map(str,eggmovesAlola)) + '|' # Create a One-String with all Alolan egg moves.
		else:
			alolaEMstring = ''
		# -------------------------------------------------------------------------------------------------------------------------------- #
		#                                                                                                                                  #
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Print all gathered information. \r\n is needed to insert a new line into file because of UTF-8.
		print('Dex: ' + dex)
		print('Name: ' + name)
		# Print Gender differences.
		if math.isnan(malePercent): # If malePercent XPath doesn't lead to a number, it's Genderless.
			maleRatio = '○'
			femaleRatio = '○'
			print('Male: ' + maleRatio)
			print('Female: ' + femaleRatio)
		else:
			maleRatio = '♂ ' + '%g' % malePercent + '%' # '%g' Floating point exponential format (lowercase), if exponent is greater than -4 or less than precision.
			femaleRatio = '♀ ' + '%g' % float('%.2f' % (100 - malePercent)) + '%' # Convert '100 - malePercent' to float and '%.2f' rounds to 2 decimals.
			print('Male: ' + maleRatio)
			print('Female: ' + femaleRatio)
			# f.write(maleRatio + '\r\n')
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Print Types if Pokémon doesn't have alternate forms.
		if len(formNames) == 0: # If Pokémon has no alternate forms.
			print('Type 1: ' + type1) # Print [Type1]. 
			print('Type 2: ' + type2) # Print [Type2].
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Print Hatch Steps.
		print('Hatch Steps:', hatchSteps)
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Print Egg Groups.
		if (len(eggGroups) >= 1): # If it has at least 1 egg group...
			egg1 = eggGroups[0]
			print('Egg Group 1: ' + egg1)
			if (len(eggGroups) == 2): # If it has 2 egg groups...
				egg2 = eggGroups[1]
				print('Egg Group 2: ' + egg2)
			else: # If it doesn't have a second egg group...
				egg2 = '----'
				print('Egg Group 2: ----')
		else: # If it does not have any ggg groups...
			egg1 = 'Undiscovered'
			egg2 = '----'
			print('Egg Group 1: ' + egg1)
			print('Egg Group 2: ' + egg2)
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Abilities.
		# Normal Abilities.
		if (len(abilities) >= 1): # If it has at least 1 ability...
			ability1 = abilities[0]
			if (len(abilities) == 2): # If it has 2 abilities...
				ability2 = abilities[1]
			else: # If it doesn't have a second ability...
				ability2 = '----'
		# Hidden Ability
		if (len(hiddenAbility) >= 1): # If at least one Hidden Ability exists.
			hAbility = hiddenAbility[0]
		else:
			hAbility = '----'
		# Special Ability
		if (len(specialAbility) >= 1): # If at least one Special Ability exists.
			sAbility = specialAbility[0]
		else:
			sAbility = '----'
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Print Egg Moves and/or Egg Moves Alola.
		print('Egg Moves:' + ' ' + '\t'.join(map(str,normalEM))) # Print normal Egg moves, as one string, separated by [TAB].
		if len(eggmovesAlola) >= 1: # If it has an Alolan form with Egg Moves...
			print('Egg Moves (Alola):' + ' ' + '\t'.join(map(str,alolanEM))) # ...print Alolan Egg Moves, as one string, separated by [TAB].
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Gender differences, Mega Evolutions and Pokémon with no forms.
		genderSprites = ["449", "450", "521", "592", "593", "668"] # Hippopotas, Hippowdon, Unfezant, Frillish, Jellicent, Pyroar. (Meowstic below is a special case.)
		primalPokemon = ["382", "383"] # Kyogre and Groudon
		if len(formNames) == 0: # If Pokémon has no alternate forms.
			if dex in genderSprites: # If 'dex' is contained on 'genderSprites' list.
				f.write(name + ' ♂' + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + type1 + '\t' + type2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
				f.write(name + ' ♀' + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + type1 + '\t' + type2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
			elif dex == '678': # Meowstic has 2 hidden abilities.
				f.write(name + ' ♂' + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + type1 + '\t' + type2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
				f.write(name + ' ♀' + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + type1 + '\t' + type2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hiddenAbility[1] + '\t' + sAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
			elif dex == '201': # If Pokémon is Unown.
				alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '?'] # Unown Alphabet.
				for i in range(len(alphabet)): # For each letter in alphabet.
					f.write(name + ' ' + alphabet[i] + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + type1 + '\t' + type2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
			else: # If only has a normal form with no differences and it's not Unown.
				f.write(name + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + type1 + '\t' + type2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
			# Pokémon has mega evolution.
			if megaEvo == 2: # If Pokémon has 2 mega evolutions.
				noAbility = '----' # No ability 2, hidden ability or special ability.
				f.write('Mega ' + name + ' X' + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + typeX1 + '\t' + typeX2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + megaAbility1 + '\t' + noAbility + '\t' + noAbility + '\t' + noAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
				f.write('Mega ' + name + ' Y' + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + typeY1 + '\t' + typeY2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + megaAbility2 + '\t' + noAbility + '\t' + noAbility + '\t' + noAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
			elif megaEvo == 1: # If Pokémon has 1 mega evolutions.
				noAbility = '----' # No ability 2, hidden ability or special ability.
				f.write('Mega ' + name + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + megaType1 + '\t' + megaType2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + megaAbility1 + '\t' + noAbility + '\t' + noAbility + '\t' + noAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
			elif dex in primalPokemon: # Pokémon has Primal Reversion
				noAbility = '----' # No ability 2, hidden ability or special ability.
				f.write('Primal ' + name + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + primalType1 + '\t' + primalType2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + primalAbility1 + '\t' + primalAbility2 + '\t' + noAbility + '\t' + noAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
			
			print('Ability 1: ' + ability1)
			print('Ability 2: ' + ability2)
			print('Hidden Ability: ' + hAbility)
			print('Special Ability: ' + sAbility)
			if len(megaAbilities) >=1: print('Mega Abilities: ' + megaAbility1 + '\t' + megaAbility2)
			if len(primalAbilities) >=1: print('Primal Abilities: ' + primalAbility1 + '\t' + primalAbility2)
			print('')
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Pikachu, because hats don't have egg moves, so print normal form before hat forms.
		if dex == '025':
			f.write(name + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + type1 + '\t' + type2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# Print Forms and Types.
		if dex == '493': # Arceus, a special case.
				for a in range(len(formNames)):
					arceusAlt = (re.sub(r"(-type|Normal)", r"", formNames[a])).capitalize() # Remove words from Arceus' name.
					arceusType = (re.sub(r"(-type)", r"", formNames[a])).capitalize() # Remove words from Arceus' type.
					print((name + '-' + arceusAlt).rstrip('-') + ': ' + arceusType) # Strip name from residual '-' at the end, after capitalization.
					f.write((name + '-' + arceusAlt).rstrip('-') + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + arceusType + '\t' + '----' + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
		elif dex == '773': # Silvally, a special case.
				for s in range(len(formNames)):
					silvallyAlt = (re.sub(r"(Type: |Normal)", r"", formNames[s])).capitalize() # Remove words from Silvally's name.
					silvallyType = (re.sub(r"(Type: )", r"", formNames[s])).capitalize() # Remove words from Silvally's type.
					print((name + '-' + silvallyAlt).rstrip('-') + ': ' + silvallyType) # Strip name from residual '-' at the end, after capitalization.
					f.write((name + '-' + silvallyAlt).rstrip('-') + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + silvallyType + '\t' + '----' + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
		elif len(formNames) >= 1: # If Pokémon has forms.
			for j in range(len(formNames)):
				# Start by defining the egg moves.
				if j == 0: # The first form.
					altString = normalEMstring # One-string = normal EM's.
				else:
					if (len(eggmovesAlola) >= 1): # If eggmovesAlola has at least 1 value.
						altString = alolaEMstring # One-string = alola EM's.
					else:
						altString = normalEMstring # One-string = normal EM's.
				
				# Remove words from form name.
				altName = re.sub(r"(Rotom| Style|-Striped| Mode| Forme| Form| Sea|Kyurem|Incarnate|Greninja| Pattern| Flower| Trim| Size|Hoopa | Core|Necrozma|Magearna| Color|Standard|Normal|Aria| Cloak|Plant|Altered|Land|Overcast|Ordinary|Natural|Neutral|Confined|Solo|Disguised|Shield|Average|50%)", r"", formNames[j])
				allformAbility = tree.xpath('//table[@class="dextable"]/tr/td[@class="fooinfo"]//b[contains(text(), "' + altName + '")]/following-sibling::a[contains(@href, "abilitydex")][not(preceding-sibling::b[position()=1 and text()="Hidden Ability"])]/b/text()') # Get form abilities
				formAbility = ["Compound Eyes" if x=="Compoundeyes" else "Lightning Rod" if x=="Lightningrod" else x for x in allformAbility]
				
				# Define the abilities (starting with special cases).
				if dex == '487': # Giratina
					if j == 1: # The second form.
						hAbility = '----'
				elif dex == '550': # Basculin
					if j == 0: # The first form.
						ability1 = abilities[0] # Set 'ability1' to ability 1.
						ability2 = abilities[2] # Set 'ability2' to ability 3.
					elif j == 1: # The second form.
						ability1 = abilities[1] # Set 'ability1' to ability 2.
						ability2 = abilities[2] # Set 'ability2' to ability 3.
				elif dex == '641': # Tornadus
					if j == 1: # The second form.
						ability1 = formAbility[0] # Set 'ability1' to form ability 1.
						hAbility = '----'
				elif dex == '642': # Thundurus
					if j == 1: # The second form.
						ability1 = formAbility[0] # Set 'ability1' to ability 1.
						hAbility = '----'
				elif dex == '645': # Landorus
					if j == 1: # The second form.
						ability1 = formAbility[0] # Set 'ability1' to ability 1.
						hAbility = '----'
				elif dex == '646': # Zygarde
					if j == 0: # The first form.
						ability1 = abilities[0] # Set 'ability1' to form ability 1.
					elif j == 1: # The second form.
						ability1 = formAbility[0] # Set 'ability1' to form ability 1.
					elif j == 2: # The third form.
						ability1 = formAbility[0] # Set 'ability1' to form ability 1.
				elif dex == '658': # Greninja
					if j == 1: # The second form.
						ability1 = formAbility[0] # Set 'ability1' to form ability 1.
						hAbility = '----'
				elif dex == '718': # Zygarde
					if j == 2: # The third form.
						formAbility = tree.xpath('//table[@class="dextable"]/tr/td[@class="fooinfo"]//b[contains(text(), "Other")]/following-sibling::a[position()=1 or position()=2][not(b/text()="Hidden")]/b/text()') # Get form abilities
						ability1 = formAbility[0] # Set 'ability1' to form ability 1.
				elif dex == '745': # Lycanroc
					if j == 1: # The second form.
						ability1 = formAbility[0] # Set 'ability1' to form ability 1.
						ability2 = formAbility[1] # Set 'ability2' to form ability 2.
						hAbility = hiddenAbility[3]
						sAbility = '----'
					elif j == 2: # The third form.
						ability1 = formAbility[0] # Set 'ability1' to form ability 1.
						ability2 = '----'
						hAbility = '----'
						sAbility = '----'
				elif (len(formAbility) >= 1) and altName: # If Pokémon has at least 1 form ability and the form name exists...
					ability1 = formAbility[0] # Set 'ability1' to form ability 1.
					if (len(formAbility) == 2): # If Pokémon has 2 form abilities.
						ability2 = formAbility[1] # Set 'ability2' to form ability 2.
					else:
						ability2 = '----'
				
				# Remove egg moves from Pikachu with hats.
				if dex == '025': # Pikachu
					altString = ''
					normalEM = [''] * 19
					alolanEM = [''] * 19
				
				# If form is Alolan, change to alolan egg moves and alola hidden ability if it has one, else the hidden ability is blank.
				if altName == 'Alola':
					allEggMoves = alolanEM
					if len(alolaHA) >=1:
						hAbility = alolaHA[0]
					else:
						hAbility = '----'
				else:
					allEggMoves = normalEM
				
				# Define the forms types.
				if types: # If all forms have the same types and a table of types doesn't exist.
					if dex == '658' and j == 1: # Greninja-Ash can't breed and male ratio is 100% male.
						maleRatio = '♂ 100%'
						femaleRatio = '♀ 0%'
					
					f.write((name + '-' + altName).rstrip('-') + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + type1.rstrip('\"') + '\t' + type2.rstrip('\"') + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,allEggMoves)) + '\t' + altString + '\r\n') # Print to file.
					print((name + '-' + altName).rstrip('-') + ': ' + type1.rstrip('\"') + '\t' + type2.rstrip('\"')) # Name-Form: [Type 1] (+ [Type 2] if it has more than 1 type).
					print('Ability 1: ' + ability1)
					print('Ability 2: ' + ability2)
					print('Hidden Ability: ' + hAbility)
					print('Special Ability: ' + sAbility)
					print('')
				else: # If forms have different types.
					if (dex == '479' and j > 0): # Rotom Types are not in order, so search based on 'altName'
						altTypes = tree.xpath('//td[@class="cen"]/table/tr/td[contains(text(), "' + altName + '")]/following-sibling::td/a/img[contains(@src, "type")]/@alt')
					else:
						altTypes = tree.xpath('//td[@class="cen"]/table/tr[' + str(j + 1) + ']/td/a/img[contains(@src, "type")]/@alt') # Get types list.
					altType1 = (altTypes[0].replace('-type', '')).capitalize()
					altType2 = ((altTypes[1].replace('-type', '')).capitalize() if len(altTypes) >= 2 else '----')
					f.write((name + '-' + altName).rstrip('-') + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + altType1.rstrip('\"') + '\t' + altType2.rstrip('\"') + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ability1 + '\t' + ability2 + '\t' + hAbility + '\t' + sAbility + '\t' + '\t'.join(map(str,allEggMoves)) + '\t' + altString + '\r\n') # Print to file.
					print((name + '-' + altName).rstrip('-') + ': ' + altType1.strip('\"') + '\t' + altType2.strip('\"')) # Name-Form: [Type 1] (+ [Type 2] if it has more than 1 type).
					print('Ability 1: ' + ability1)
					print('Ability 2: ' + ability2)
					print('Hidden Ability: ' + hAbility)
					print('Special Ability: ' + sAbility)
					if len(ultraAbilities) >=1: print('Ultra Ability: ' + ultraAbility1 + '\t' + ultraAbility2)
					print('')
		
		if dex == '800': # Necrozma's Ultra Burst, weird placement, I know.
			noAbility = '----' # No ability 2, hidden ability or special ability.
			f.write('Ultra ' + name + '\t' + dex + '\t' + maleRatio + '\t' + femaleRatio + '\t' + ultraType1 + '\t' + ultraType2 + '\t' + hatchSteps + '\t' + egg1 + '\t' + egg2 + '\t' + ultraAbility1 + '\t' + noAbility + '\t' + noAbility + '\t' + noAbility + '\t' + '\t'.join(map(str,normalEM)) + '\t' + normalEMstring + '\r\n') # Print to file.
		# -------------------------------------------------------------------------------------------------------------------------------- #
		# print('\n\n') # Print 2 new lines.

if __name__ == '__main__': # If running program is the main program and is not called by another program...
	main() # Run the main() function.

print('Scraping complete. File output: ' + output)
f.close() # Close file.

end_time = time.time()
print('Scraping execution time: ' + str(datetime.timedelta(seconds=int(end_time - start_time))))
os.system('start ' + outdir)