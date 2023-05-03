import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    print("Analyzing", arg)
    strong =[]
    weak = []
    names = []
    result = ""
    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    conn = sqlite3.connect('pokemon.sqlite')
    c = conn.cursor()
    c.execute("""
    SELECT p.id, p.name, t.name, a.against_bug, a.against_dark, a.against_dragon, a.against_electric, 
       a.against_fairy, a.against_fight, a.against_fire, a.against_flying, a.against_ghost, 
       a.against_grass, a.against_ground, a.against_ice, a.against_normal, a.against_poison, 
       a.against_psychic, a.against_rock, a.against_steel, a.against_water
    FROM pokemon_type AS pt
    JOIN pokemon AS p ON p.id = pt.pokemon_id
    JOIN type AS t ON t.id = pt.type_id
    JOIN against AS a ON a.type_source_id1 = t.id AND a.type_source_id2 = t.id
    WHERE p.id = ?;
        """, (arg,)) 
    
    results = c.fetchall()

    
    for row in results:
        names.append(row[2])
        counter = 3
        num = 0
        for x in range(18):
            #print(row[counter])
            if row[counter] < 1:
                strong.append(types[num])
             
                if types[num] in weak:
                    weak.remove(types[num])
                 
            
                counter += 1
                num +=1
            elif row[counter] > 1 and types[num] not in strong:
                weak.append(types[num])
            
                counter += 1
                num +=1
            else:
                counter += 1
                num +=1
    #result += row[1] + " () is strong against " + strong + " but weak against " + weak
    #print(row[1] + " () is strong against " + strong + " but weak against " + weak)
    print(row[1], end=" ")
    print(names, end="")
    print(" is strong against ", end="")
    print(strong, end="")
    print(" but weak against ", end="")
    print(weak)
    team.append(row[1])


    


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")
