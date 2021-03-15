import json

filetje = open("json.json")
# Open hem volledig
data = json.load(filetje)
filetje.close()
print("-------------------------Alle data--------------------------------------------")
print(data)

# Haal de informatie over de forward en reverse eruit
print("------------------------Alleen forward----------------------------------------")
print(data['header']['forward_sequentie']) 
print("------------------------Alleen reverse----------------------------------------")
print(data['header']['reverse_sequentie'])

# Haal alleen de reverse sequentie op
print("------------------------Sequentie---------------------------------------------")
print(data['header']['forward_sequentie']['sequentie'])

# En zo kan dit met alles in het bestand gedaan worden

print("------------------------Aan het toevoegen-------------------------------------")
print(data['header']['forward_sequentie']['sequentie'])
data['header']['forward_sequentie']['sequentie'] += "KIP"
print(data['header']['forward_sequentie']['sequentie'])
filetje = open("json.json", "w")

json.dump(data, filetje) 