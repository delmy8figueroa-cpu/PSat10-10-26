class Pupil:
    def __init__(self, Name, Age):
        self.Name = Name
        self.Age = Age

pupils = []

def print_class(pupils):
    for pupil in pupils:
        print(pupil.Name, "-", pupil.Age)
    print("\n")

def find_eldest(pupils):
    Eldest_Pupil = Pupil("", 0)
    for pupil in pupils:
        if pupil.Age > Eldest_Pupil.Age:
            Eldest_Pupil.Age = pupil.Age
            Eldest_Pupil.Name = pupil.Name
    return Eldest_Pupil

def get_average(pupils):  # La función se llama get_average
    sum = 0
    for pupil in pupils:
        sum += pupil.Age
    sum /= len(pupils)
    return sum

with open("my_class.txt", "r") as file:
    for line in file:
        line = line.strip() # Limpieza para evitar saltos de línea molestos
        if not line:
            continue
        data = line.split(" ")
        pupil = Pupil(data[0], int(data[1]))
        pupils.append(pupil)

print_class(pupils)
Eldest_Pupil = find_eldest(pupils)  # Corregido: antes decía Eldst_Pupil
Average_Age = get_average(pupils)   # Corregido: antes decía get_average_age

# Corregido: la variable interna de la función no existía afuera, ahora usa Eldest_Pupil
print("Estudiante mayor:", Eldest_Pupil.Name, " . ", Eldest_Pupil.Age, "\nEdad promedio en el grupo:", Average_Age)
