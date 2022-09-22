# CLASES
class Clothing:
    def __init__(self, number):
        self.number = number
        self.incompatibles = {}
        self.washing_time = 0

    def add_incompatible(self, clothing_to_add: "Clothing"):
        self.incompatibles[clothing_to_add.number] = clothing_to_add

    def __str__(self):
        return str(self.number)

class Washing:
    def __init__(self, clothing: Clothing):
        self.clothings = [clothing]
        self.washing_time = clothing.washing_time

    def add_clothing(self, new_clothing: Clothing):
        if any(new_clothing in x.incompatibles for x in self.clothings):
            return False
        self.clothings.append(new_clothing)
        if new_clothing.washing_time > self.washing_time:
            self.washing_time = new_clothing.washing_time
        return True

    def can_add_clothing(self, new_clothing: Clothing):
        if any(new_clothing.number in clothing.incompatibles for clothing in self.clothings):
            return False
        return True

    def __contains__(self, key):
        return key in self.clothings

# FUNCIONES
def add_clothing_to_solution(solution: list, new_clothing: Clothing):
    center = 0
    while center < len(solution) and solution[center].washing_time >= new_clothing.washing_time:
        center += 1
    index = center - 1
    while index >= 0 and not solution[index].can_add_clothing(new_clothing):
        index -= 1
    if index < 0:
        index = center
        while index < len(solution) and not solution[index].can_add_clothing(new_clothing):
            index += 1
    if index >= len(solution) or not solution[index].add_clothing(new_clothing):
        solution.append(Washing(new_clothing))

def calculate_solution(solution):
    total_washing_time = 0
    for washing in solution:
        total_washing_time += washing.washing_time
    return total_washing_time

# RESOLUCION
file = open("problema.txt", "r+")
clothings_graph = {}
for current_line in file:
    if current_line[0] == 'p':
        n = int(current_line.split(' ')[2])
        for i in range(n):
            clothings_graph[i + 1] = Clothing(i + 1)
    elif current_line[0] == 'n':
        clothings_graph[int(current_line.split(' ')[1])].washing_time = int(current_line.split(' ')[2])
    elif current_line[0] == 'e':
        clothings_graph[int(current_line.split(' ')[1])].add_incompatible(clothings_graph[int(current_line.split(' ')[2])])
        clothings_graph[int(current_line.split(' ')[2])].add_incompatible(clothings_graph[int(current_line.split(' ')[1])])

all_incompatibles = []
for i in clothings_graph:   # obtengo los grafos que tengan los vertices completamente conectados entre si (todos incompatibles entre si)
    for j in clothings_graph[i].incompatibles:
        all_incompatibles_to_add = [clothings_graph[i], clothings_graph[j]]
        for k in clothings_graph[j].incompatibles:
            if all(k in clothings_graph[clothing.number].incompatibles for clothing in all_incompatibles_to_add):
                all_incompatibles_to_add.append(clothings_graph[k])
        all_incompatibles_to_add.sort(key = lambda washing: washing.number)
        if all(all_incompatibles_to_add != incompatibles for incompatibles in all_incompatibles):
            all_incompatibles.append(all_incompatibles_to_add)

for incompatibles in all_incompatibles:
    incompatibles.sort(key = lambda washing: washing.washing_time, reverse = True)  # ordeno de descendentemente por tiempo de lavado
all_incompatibles.sort(key = len, reverse = True)   # ordeno de descendentemente por cantidad de incompatibles

solutions = []
index = 0
current_solution_size = len(all_incompatibles[index])
best_solution_size = current_solution_size
longest_incompatibles = []
while index < len(all_incompatibles): # se queda con los all_incompatibles que tengan la mayor cantidad de vertices
    longest_incompatibles.append([clothing for clothing in all_incompatibles[index]])
    solutions.append([Washing(clothing) for clothing in all_incompatibles[index]])
    index += 1

for incompatibles in longest_incompatibles:
    incompatibles.sort(key = lambda clothing: clothing.washing_time, reverse = True)
    incompatibles.sort(key = lambda clothing: len(clothing.incompatibles), reverse = True)
longest_incompatibles.sort(key = lambda incompatible: sum([clothing.washing_time for clothing in incompatible]), reverse = True)
longest_incompatibles.sort(key = lambda incompatible: sum([len(clothing.incompatibles) for clothing in incompatible]), reverse = True)

incompatibles = []
for incompatible in longest_incompatibles:
    incompatibles.extend(incompatible)

to_add = []
already_added = {}
for incompatible in incompatibles:
    if incompatible not in already_added:
        already_added[incompatible] = True
        to_add.append(incompatible)

for solution in solutions:
    for incompatible in to_add:
        if all(incompatible not in washing for washing in solution):
            add_clothing_to_solution(solution, incompatible)
            solution.sort(key = lambda washing: len(washing.clothings), reverse = True)
            solution.sort(key = lambda washing: washing.washing_time, reverse = True)

clothings_to_add = [a for b, a in clothings_graph.items()]
clothings_to_add.sort(key = lambda clothing: clothing.washing_time, reverse = True)
clothings_to_add.sort(key = lambda clothing: len(clothing.incompatibles), reverse = True)
for solution in solutions:
    for clothing in clothings_to_add:
        if all(clothing not in washing for washing in solution):
            add_clothing_to_solution(solution, clothing)
            solution.sort(key = lambda washing: len(washing.clothings), reverse = True)
            solution.sort(key = lambda washing: washing.washing_time, reverse = True)

best_solution = solutions[0]
best_solution_time = calculate_solution(best_solution)
for solution in solutions:
    if calculate_solution(solution) < best_solution_time:
        best_solution = solution
        best_solution_time = calculate_solution(best_solution)

result = open("entrega.txt", "w+")
current_washing = 1
for washing in best_solution:
    for clothing in washing.clothings:
        result.write(f"{clothing.number} {current_washing}\n")
    current_washing += 1