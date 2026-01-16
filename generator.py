import pandas as pd
import random
import os
import string
from datetime import datetime, timedelta
import zipfile
from faker import Faker

# Use Filipino locale for more realistic names
fake = Faker('en_PH')

# Languages/Ethnicities in Governor Generoso, Davao Oriental (based on Wikipedia)
ETHNICITIES = [
    "Davawenyo", "Surigaonon", "Cebuano", "Sarangani", "Sangirese", 
    "Tagalog", "Maguindanao", "Manobo", "Mandaya", "Kalagan",
    "Sangil", "Tausug", "Maranao", "Bisaya/Binisaya", "Others"
]

# Religions in Governor Generoso, Davao Oriental (adjusted for Mindanao demographics)
RELIGIONS = [
    ("Roman Catholic", 0.70),
    ("Islam", 0.15),
    ("Iglesia ni Cristo", 0.03),
    ("Evangelical", 0.03),
    ("Seventh-day Adventist", 0.02),
    ("Bible Baptist Church", 0.02),
    ("United Church of Christ", 0.01),
    ("Jehovah's Witnesses", 0.01),
    ("Aglipayan", 0.01),
    ("Others", 0.02)
]

# Proper codes from the codes file
RELATIONSHIP_CODES = {
    1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06", 7: "07", 8: "08", 9: "09", 10: "10",
    11: "11", 12: "12", 13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18", 19: "19", 20: "20",
    21: "21", 22: "22", 23: "23", 24: "24", 25: "25", 26: "26"
}

EDUCATION_CODES = [
    "00000000", "01000000", "02000000", "02100000", "10000101", "10000102", "10000103", "10000104", "10000105",
    "10000106", "10000107", "10000108", "11000101", "11000102", "11000103", "11000104", "11000105", "11000108",
    "11000201", "11000202", "11000203", "11000301", "11000302", "20400101", "20400102", "20400103", "20400105",
    "21400101", "21400102", "21400103", "21400105", "21400201", "21400202", "21400203", "21400301", "21400302",
    "30400106", "30400107", "30400108", "30400109", "30400110", "30400111", "30400201", "30400203", "30400204",
    "30400205", "30400206", "30400207", "30400208", "30400301", "30400303", "30500006", "30500007", "30500008",
    "30500009", "30500010", "30500011", "40000001", "40000002", "40000003", "50000001", "50000002", "50000003",
    "60000001", "60000002", "60000003", "60000004", "60000005", "60000006", "70000010", "80000010"
]

REASON_NOT_ATTENDING_CODES = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "99"
]

REASON_NOT_LOOKING_CODES = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "99"
]

CAUSE_OF_DEATH_CODES = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "99"
]

# More proper codes
NUCLEAR_FAMILY_CODES = {
    1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06"
}

RELATIONSHIP_NUCLEAR_HEAD_CODES = {
    0: "00", 1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 
    6: "06", 7: "07", 8: "08", 9: "09", 10: "10"
}

OVerseas_FILIPINO_CODES = {
    1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"
}

INTERNAL_DISPLACEMENT_CODES = {
    1: "1", 2: "2", 3: "3", 4: "4", 5: "5"
}

NATURE_OF_EMPLOYMENT_CODES = {
    1: "1", 2: "2", 3: "3"
}

CLASS_OF_WORKER_CODES = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"
}

BASIS_OF_PAYMENT_CODES = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"
}

MEDICAL_TREATMENT_FACILITY_CODES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'Z']

REASON_NO_TREATMENT_CODES = [1, 2, 3, 4, 5, 6, 9]

WATER_SOURCE_CODES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 99]

DRINKING_COOKING_WATER_CODES = [11, 12, 13, 14, 21, 31, 32, 41, 42, 51, 61, 71, 72, 81, 91, 92, 99]

TOILET_FACILITY_CODES = [11, 12, 13, 14, 15, 21, 22, 23, 31, 41, 51, 71, 95, 99]

GARBAGE_DISPOSAL_CODES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'Z']

HANDWASHING_FACILITY_CODES = [1, 2, 3, 4, 5, 9]

HANDWASHING_MATERIAL_CODES = ['A', 'B', 'C', 'Z']

BUILDING_TYPE_CODES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

ROOF_MATERIAL_CODES = [1, 2, 3, 4, 5, 6, 7, 9]

WALL_MATERIAL_CODES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 99]

HOUSING_MATERIAL_CODES = [1, 2, 3, 4, 5, 6, 9]

TENURE_STATUS_CODES = [1, 2, 3, 4, 5, 6, 7]

FUEL_CODES = [1, 2, 3, 4, 5, 6, 9]

PUBLIC_SAFETY_CODES = [1, 2, 3, 4, 5, 8]

# Barangay population weights
barangay_weights = {
    "Anitap": 1405,
    "Manuel Roxas": 2665,
    "Don Aurelio Chicote": 2810,
    "Lavigan": 2661,
    "Luzon": 3045,
    "Magdug": 2414,
    "Monserrat": 2004,
    "Nangan": 5168,
    "Oregon": 1186,
    "Poblacion": 5692,
    "Pundaguitan": 2485,
    "Sergio Osmeña": 1973,
    "Surop": 2656,
    "Tagabebe": 2150,
    "Tamban": 1650,
    "Tandang Sora": 1557,
    "Tibanban": 10016,
    "Tiblawan": 4538,
    "Upper Tibanban": 1493,
    "Crispin Dela Cruz": 2323,
}

total_population = sum(barangay_weights.values())
target_households = 1300  # Target households for ~5000 rows
max_members_per_household = 6  # Max 6 people per household (average ~3.5)

def weighted_barangay_list(weights, total, target):
    records = {}
    for b, pop in weights.items():
        records[b] = int(round((pop / total) * target))
    diff = target - sum(records.values())
    if diff != 0:
        largest = max(records, key=records.get)
        records[largest] += diff
    return records

# Authentic Filipino surnames common in Mindanao
FILIPINO_SURNAMES = [
    "Santos", "Reyes", "Cruz", "Bautista", "Gonzales", "Garcia", "Martinez", "Rodriguez", "Lopez", "Gomez",
    "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Gonzalez", "Diaz", "Herrera", "Jimenez",
    "Moreno", "Munoz", "Alvarez", "Romero", "Gutierrez", "Ruiz", "Castillo", "Vargas", "Ramos", "Mendoza",
    "Aguilar", "Herrera", "Medina", "Castro", "Vargas", "Reyes", "Morales", "Ortiz", "Delgado", "Silva",
    "Molina", "Guerrero", "Estrada", "Vega", "Rojas", "Contreras", "Jimenez", "Espinoza", "Valencia", "Cabrera",
    "Mendoza", "Herrera", "Vargas", "Ramos", "Gutierrez", "Castillo", "Romero", "Alvarez", "Munoz", "Moreno",
    "Jimenez", "Herrera", "Rivera", "Flores", "Torres", "Ramirez", "Sanchez", "Perez", "Gomez", "Lopez",
    "Rodriguez", "Martinez", "Garcia", "Gonzales", "Bautista", "Cruz", "Reyes", "Santos", "Dela Cruz", "Dela Rosa"
]

# Authentic Filipino first names - separated by gender
FILIPINO_MALE_NAMES = [
    "Jose", "Antonio", "Francisco", "Manuel", "Juan", "Pedro", "Luis", "Carlos", "Miguel",
    "Ramon", "Fernando", "Alberto", "Roberto", "Eduardo", "Ricardo", "Sergio", "Ruben", "Mario", "Rafael",
    "Angel", "Gabriel", "Samuel", "Daniel", "Isaac", "Elias", "Benjamin", "Nathaniel", "Sebastian",
    "Andres", "Alejandro", "Arturo", "Adrian", "Armando", "Augusto", "Alfredo", "Alfonso", "Amado", "Amador",
    "Bartolome", "Bernardo", "Bienvenido", "Bonifacio", "Benedicto", "Baltazar", "Basilio", "Braulio", "Bruno", "Buenaventura",
    "Cesar", "Cristobal", "Clemente", "Cornelio", "Cipriano", "Cirilo", "Celestino", "Cecilio", "Crispin", "Crisostomo",
    "Domingo", "Dionisio", "Damaso", "Delfin", "Demetrio", "Dionicio", "Diosdado", "Domingo", "Doroteo", "Dionisio",
    "Emilio", "Efren", "Eugenio", "Esteban", "Eulogio", "Evaristo", "Eligio", "Elpidio", "Eusebio", "Eduardo",
    "Felipe", "Felix", "Faustino", "Federico", "Fermin", "Florencio", "Fortunato", "Fulgencio", "Fidel", "Filemon",
    "Gregorio", "Guillermo", "Geronimo", "Gaudencio", "Gavino", "Gervasio", "Gilberto", "Gonzalo", "Gualberto", "Gualberto",
    "Hernando", "Hilario", "Honorio", "Hugo", "Humberto", "Hipolito", "Hermenegildo", "Hector", "Horacio", "Hilario",
    "Ignacio", "Isidro", "Ismael", "Ildefonso", "Inocencio", "Ireneo", "Isagani", "Isidoro", "Ivan", "Ildefonso",
    "Javier", "Joaquin", "Julio", "Julian", "Jorge", "Jesus", "Jeremias", "Jacinto", "Jose", "Juan",
    "Leonardo", "Lorenzo", "Leopoldo", "Luciano", "Lauro", "Luis", "Lazaro", "Lorenzo", "Luciano", "Lauro",
    "Marcelo", "Mariano", "Maximo", "Mateo", "Mauricio", "Melchor", "Modesto", "Marcos", "Martin", "Miguel",
    "Nicolas", "Narciso", "Nicanor", "Nestor", "Norberto", "Nicanor", "Narciso", "Nestor", "Norberto", "Nicolas",
    "Oscar", "Octavio", "Orlando", "Omar", "Oswaldo", "Olegario", "Onofre", "Orestes", "Oscar", "Octavio",
    "Pablo", "Patricio", "Pascual", "Pio", "Placido", "Ponciano", "Primitivo", "Prospero", "Pablo", "Patricio",
    "Quirino", "Quintin", "Quirino", "Quintin", "Quirino", "Quintin", "Quirino", "Quintin", "Quirino", "Quintin",
    "Rogelio", "Rolando", "Romulo", "Rufino", "Ruperto", "Reynaldo", "Rodolfo", "Rolando", "Romulo", "Rufino",
    "Salvador", "Simeon", "Silvestre", "Sergio", "Santiago", "Severino", "Silvino", "Sotero", "Salvador", "Simeon",
    "Tomas", "Teodoro", "Tiburcio", "Timoteo", "Telesforo", "Tirso", "Tomas", "Teodoro", "Tiburcio", "Timoteo",
    "Urbano", "Ulises", "Uriel", "Urbano", "Ulises", "Uriel", "Urbano", "Ulises", "Uriel", "Urbano",
    "Valentin", "Vicente", "Victor", "Virgilio", "Valeriano", "Venancio", "Vicente", "Victor", "Virgilio", "Valentin",
    "Wilfredo", "Wenceslao", "Wilfredo", "Wenceslao", "Wilfredo", "Wenceslao", "Wilfredo", "Wenceslao", "Wilfredo", "Wenceslao"
]

FILIPINO_FEMALE_NAMES = [
    "Maria", "Ana", "Carmen", "Rosa", "Isabel", "Teresa", "Dolores", "Pilar", "Concepcion", "Mercedes", "Josefa",
    "Elena", "Beatriz", "Alicia", "Monica", "Patricia", "Gloria", "Esperanza", "Victoria", "Amparo", "Consuelo",
    "Sofia", "Valentina", "Isabella", "Camila", "Valeria", "Ximena", "Daniela", "Natalia", "Gabriela", "Samantha",
    "Adela", "Adelina", "Adoracion", "Agnes", "Alejandra", "Alma", "Amalia", "Amelia", "Andrea", "Angela",
    "Angelica", "Angelina", "Anita", "Antonia", "Araceli", "Aurora", "Barbara", "Belinda", "Bernadette", "Bianca",
    "Blanca", "Caridad", "Carolina", "Catalina", "Cecilia", "Celeste", "Celia", "Clara", "Claudia", "Cristina",
    "Diana", "Dolores", "Dorothy", "Edith", "Elisa", "Elvira", "Emilia", "Emma", "Enriqueta", "Estela",
    "Esther", "Eugenia", "Eva", "Evangeline", "Felicia", "Fernanda", "Flora", "Francisca", "Gabriela", "Gina",
    "Gloria", "Graciela", "Guadalupe", "Herminia", "Imelda", "Ines", "Irene", "Iris", "Isabella", "Jacinta",
    "Jacqueline", "Jasmine", "Jennifer", "Jessica", "Jocelyn", "Josefina", "Juana", "Julia", "Juliana", "Julieta",
    "Katherine", "Kimberly", "Leticia", "Ligaya", "Lilia", "Liliana", "Lina", "Liza", "Lolita", "Lorena",
    "Lourdes", "Lucia", "Lucila", "Luisa", "Luz", "Lydia", "Magdalena", "Manuela", "Marcela", "Margarita",
    "Maria", "Mariana", "Marianne", "Maricel", "Maricris", "Marilou", "Marina", "Marissa", "Marlene", "Martha",
    "Martina", "May", "Melissa", "Michelle", "Milagros", "Minerva", "Miriam", "Monica", "Natalia", "Nelly",
    "Nena", "Nina", "Nora", "Norma", "Ofelia", "Olivia", "Ophelia", "Pamela", "Paula", "Paulina",
    "Perla", "Petra", "Philippa", "Priscilla", "Purificacion", "Rachel", "Raquel", "Rebecca", "Regina", "Remedios",
    "Renata", "Rita", "Roberta", "Rochelle", "Romina", "Rosa", "Rosalinda", "Rosario", "Rose", "Rosemarie",
    "Rosita", "Rowena", "Ruby", "Ruth", "Sabina", "Salome", "Sandra", "Sara", "Sarah", "Serafina",
    "Silvia", "Soledad", "Sonia", "Stella", "Susan", "Susana", "Sylvia", "Teresa", "Theresa", "Trinidad",
    "Ursula", "Valentina", "Vanessa", "Veronica", "Vicenta", "Vilma", "Virginia", "Vivian", "Wilhelmina", "Yolanda",
    "Zenaida", "Zoraida", "Adela", "Adelina", "Adoracion", "Agnes", "Alejandra", "Alma", "Amalia", "Amelia",
    "Andrea", "Angela", "Angelica", "Angelina", "Anita", "Antonia", "Araceli", "Aurora", "Barbara", "Belinda"
]

def random_filipino_surname():
    return random.choice(FILIPINO_SURNAMES)

def random_filipino_first_name(gender=None):
    """Generate gender-appropriate Filipino first name"""
    if gender == 1:  # Male
        return random.choice(FILIPINO_MALE_NAMES)
    elif gender == 2:  # Female
        return random.choice(FILIPINO_FEMALE_NAMES)
    else:
        # Fallback to random selection if gender not specified
        return random.choice(FILIPINO_MALE_NAMES + FILIPINO_FEMALE_NAMES)

def random_suffix(gender):
    """Generate suffix only for males (Jr., Sr., III, IV)"""
    if gender == 1:  # Male
        return random.choice(['Jr.', 'Sr.', 'III', 'IV', ''])
    else:  # Female
        return ''  # No suffix for females

def random_middle_name(exclude_surname):
    """Generate middle name (mother's maiden name) different from last name"""
    available_surnames = [s for s in FILIPINO_SURNAMES if s != exclude_surname]
    return random.choice(available_surnames)

def random_date():
    start = datetime(1940, 1, 1)
    end = datetime(2024, 5, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).date().isoformat()

def random_text(length=10):
    return fake.word().upper() if length <= 10 else fake.sentence(nb_words=3)

def random_code(n):
    return random.randint(1, n)

def random_multi_code(codes, count=3):
    return ','.join(random.sample(codes, min(count, len(codes))))

def random_float(a=0, b=100):
    return round(random.uniform(a, b), 2)

def random_int(a=0, b=100):
    return random.randint(a, b)

def realistic_age_distribution():
    """Generate realistic age distribution for Governor Generoso population"""
    # Age groups with weights based on typical rural Philippine demographics
    age_groups = [
        (0, 4, 0.12),      # 0-4 years: 12%
        (5, 14, 0.18),     # 5-14 years: 18%
        (15, 24, 0.16),    # 15-24 years: 16%
        (25, 34, 0.15),    # 25-34 years: 15%
        (35, 44, 0.13),    # 35-44 years: 13%
        (45, 54, 0.11),    # 45-54 years: 11%
        (55, 64, 0.08),    # 55-64 years: 8%
        (65, 100, 0.07)    # 65+ years: 7%
    ]
    
    # Select age group based on weights
    rand = random.random()
    cumulative = 0
    for min_age, max_age, weight in age_groups:
        cumulative += weight
        if rand <= cumulative:
            return random.randint(min_age, max_age)
    return random.randint(0, 100)

def realistic_marital_status(age, gender):
    """Generate realistic marital status based on age and gender"""
    if age < 15:
        return 1  # Single/never married
    elif age < 18:
        # 15-17: mostly single, some married (early marriage in rural areas)
        return 1 if random.random() < 0.85 else 2
    elif age < 25:
        # 18-24: mix of single and married
        if gender == 1:  # Male
            return 1 if random.random() < 0.60 else 2
        else:  # Female
            return 1 if random.random() < 0.45 else 2
    elif age < 35:
        # 25-34: mostly married
        return 1 if random.random() < 0.15 else 2
    elif age < 50:
        # 35-49: mostly married, some single
        return 1 if random.random() < 0.10 else 2
    elif age < 65:
        # 50-64: mostly married, some widowed
        rand = random.random()
        if rand < 0.05:
            return 1  # Single
        elif rand < 0.15:
            return 3  # Widowed
        else:
            return 2  # Married
    else:
        # 65+: mix of married and widowed
        rand = random.random()
        if rand < 0.30:
            return 3  # Widowed
        else:
            return 2  # Married

def realistic_gender_distribution():
    """Generate realistic gender distribution for rural areas (slightly more males)"""
    # Rural areas often have slightly more males due to migration patterns
    return 1 if random.random() < 0.52 else 2  # 52% male, 48% female

def realistic_education_level(age):
    """Generate realistic education levels for rural Mindanao"""
    if age < 6:
        return "00000000"  # No grade completed
    elif age < 12:
        # Elementary age - some dropouts
        if random.random() < 0.15:  # 15% dropout rate
            return "00000000"  # No grade completed
        else:
            return random.choice(["01000000", "02000000", "02100000", "10000101", "10000102", "10000103", "10000104", "10000105"])
    elif age < 18:
        # High school age - higher dropout rate
        if random.random() < 0.25:  # 25% dropout rate
            return random.choice(["00000000", "10000101", "10000102", "10000103", "10000104", "10000105"])
        else:
            return random.choice(["11000101", "11000102", "11000103", "11000104", "11000105", "11000108", "11000201", "11000202", "11000203"])
    elif age < 25:
        # Young adults - mix of high school and college
        if random.random() < 0.40:  # 40% only high school
            return random.choice(["11000101", "11000102", "11000103", "11000104", "11000105", "11000108", "11000201", "11000202", "11000203"])
        else:
            return random.choice(["20400101", "20400102", "20400103", "20400105", "21400101", "21400102", "21400103", "21400105"])
    else:
        # Adults - mostly high school or elementary
        if random.random() < 0.30:  # 30% college level
            return random.choice(["20400101", "20400102", "20400103", "20400105", "21400101", "21400102", "21400103", "21400105", "30400106", "30400107", "30400108"])
        elif random.random() < 0.60:  # 30% high school
            return random.choice(["11000101", "11000102", "11000103", "11000104", "11000105", "11000108", "11000201", "11000202", "11000203"])
        else:  # 40% elementary
            return random.choice(["10000101", "10000102", "10000103", "10000104", "10000105", "10000106", "10000107", "10000108"])

def realistic_employment_status(age, gender):
    """Generate realistic employment status for rural Governor Generoso"""
    if age < 15:
        return 2  # Not in labor force (too young)
    elif age < 18:
        # 15-17: mostly not working, some working
        return 1 if random.random() < 0.20 else 2
    elif age < 25:
        # 18-24: mix of working and not working
        if gender == 1:  # Male
            return 1 if random.random() < 0.70 else 2
        else:  # Female
            return 1 if random.random() < 0.50 else 2
    elif age < 35:
        # 25-34: mostly working
        return 1 if random.random() < 0.85 else 2
    elif age < 50:
        # 35-49: mostly working
        return 1 if random.random() < 0.90 else 2
    elif age < 65:
        # 50-64: mostly working, some retired
        return 1 if random.random() < 0.75 else 2
    else:
        # 65+: mostly not working
        return 1 if random.random() < 0.30 else 2

def realistic_occupation(age, gender):
    """Generate realistic occupations for Governor Generoso (farming, fishing, mining)"""
    if age < 15:
        return ""
    
    # Occupation weights based on local economy
    occupations = [
        ("Farming", 0.35),      # 35% - agriculture
        ("Fishing", 0.20),      # 20% - fishing
        ("Mining", 0.10),       # 10% - mining
        ("Construction", 0.08), # 8% - construction
        ("Transport", 0.05),    # 5% - transportation
        ("Retail", 0.05),       # 5% - retail
        ("Government", 0.04),   # 4% - government
        ("Education", 0.03),    # 3% - education
        ("Healthcare", 0.03),   # 3% - healthcare
        ("Others", 0.07)        # 7% - others
    ]
    
    # Select occupation based on weights
    rand = random.random()
    cumulative = 0
    for occupation, weight in occupations:
        cumulative += weight
        if rand <= cumulative:
            return occupation
    return "Others"

def realistic_housing_materials():
    """Generate realistic housing materials for Governor Generoso (2nd municipal income class)"""
    # 2nd municipal income class - better materials than typical rural areas
    roof_materials = [
        (1, 0.35),  # Galvanized iron/aluminum - 35% (higher due to income class)
        (2, 0.20),  # Nipa - 20%
        (3, 0.15),  # Cogon - 15%
        (4, 0.10),  # Bamboo - 10%
        (5, 0.08),  # Wood - 8%
        (6, 0.10),  # Concrete - 10%
        (7, 0.02)   # Others - 2%
    ]
    
    wall_materials = [
        (1, 0.25),  # Concrete - 25% (higher due to income class)
        (2, 0.20),  # Wood - 20%
        (3, 0.20),  # Bamboo - 20%
        (4, 0.15),  # Nipa - 15%
        (5, 0.15),  # Galvanized iron - 15%
        (6, 0.03),  # Others - 3%
        (7, 0.02)   # Not stated - 2%
    ]
    
    # Select materials based on weights
    roof_rand = random.random()
    wall_rand = random.random()
    
    roof_cumulative = 0
    wall_cumulative = 0
    
    roof_material = 1
    wall_material = 1
    
    for material, weight in roof_materials:
        roof_cumulative += weight
        if roof_rand <= roof_cumulative:
            roof_material = material
            break
    
    for material, weight in wall_materials:
        wall_cumulative += weight
        if wall_rand <= wall_cumulative:
            wall_material = material
            break
    
    return roof_material, wall_material

def realistic_water_sanitation():
    """Generate realistic water and sanitation for rural Governor Generoso"""
    # Water sources more common in rural areas
    water_sources = [
        (1, 0.05),   # Piped into dwelling - 5%
        (2, 0.10),   # Piped into yard - 10%
        (3, 0.20),   # Public tap - 20%
        (4, 0.25),   # Deep well - 25%
        (5, 0.15),   # Shallow well - 15%
        (6, 0.10),   # Spring - 10%
        (7, 0.10),   # Rainwater - 10%
        (8, 0.05)    # Others - 5%
    ]
    
    # Toilet facilities more basic in rural areas
    toilet_facilities = [
        (11, 0.05),  # Flush to sewer - 5%
        (12, 0.15),  # Flush to septic - 15%
        (13, 0.10),  # Flush to pit - 10%
        (14, 0.20),  # Pit latrine - 20%
        (15, 0.15),  # Composting toilet - 15%
        (21, 0.10),  # Bucket - 10%
        (22, 0.10),  # Hanging toilet - 10%
        (23, 0.10),  # Others - 10%
        (31, 0.05)   # No facility - 5%
    ]
    
    # Select based on weights
    water_rand = random.random()
    toilet_rand = random.random()
    
    water_cumulative = 0
    toilet_cumulative = 0
    
    water_source = 1
    toilet_facility = 11
    
    for source, weight in water_sources:
        water_cumulative += weight
        if water_rand <= water_cumulative:
            water_source = source
            break
    
    for facility, weight in toilet_facilities:
        toilet_cumulative += weight
        if toilet_rand <= toilet_cumulative:
            toilet_facility = facility
            break
    
    return water_source, toilet_facility

def realistic_rural_vehicles_appliances():
    """Generate realistic vehicle and appliance counts for Governor Generoso (2nd municipal income class, 31.52% poverty)"""
    # Based on 2nd municipal income class and 31.52% poverty incidence
    # Higher income than typical rural areas, but still significant poverty
    return {
        # Appliances (2nd municipal income class - better than typical rural)
        'refrigerator': random_int(0, 1) if random.random() < 0.85 else 0,  # 85% have refrigerator (necessity)
        'aircon': random_int(0, 1) if random.random() < 0.25 else 0,  # 25% have aircon (2nd income class)
        'washing_machine': random_int(0, 1) if random.random() < 0.40 else 0,  # 40% have washing machine
        'stove': random_int(1, 2) if random.random() < 0.95 else 0,  # 95% have stove (necessity)
        'radio': random_int(0, 2) if random.random() < 0.75 else 0,  # 75% have radio (0-2)
        'tv': random_int(0, 2) if random.random() < 0.90 else 0,  # 90% have TV (0-2) - common
        'stereo': random_int(0, 1) if random.random() < 0.40 else 0,  # 40% have stereo
        'landline': random_int(0, 1) if random.random() < 0.30 else 0,  # 30% have landline
        'cellphone_keypad': random_int(0, 3) if random.random() < 0.90 else 0,  # 90% have basic phones (0-3)
        'cellphone_smart': random_int(0, 2) if random.random() < 0.75 else 0,  # 75% have smartphones (0-2)
        'tablet': random_int(0, 1) if random.random() < 0.25 else 0,  # 25% have tablets
        'computer': random_int(0, 1) if random.random() < 0.35 else 0,  # 35% have computers
        
        # Vehicles (2nd municipal income class - better than typical rural)
        'car': random_int(0, 1) if random.random() < 0.35 else 0,  # 35% have cars (2nd income class)
        'van': random_int(0, 1) if random.random() < 0.10 else 0,  # 10% have vans
        'jeep': random_int(0, 1) if random.random() < 0.15 else 0,  # 15% have jeeps
        'truck': random_int(0, 1) if random.random() < 0.25 else 0,  # 25% have trucks (business/farming)
        'motorcycle': random_int(0, 2) if random.random() < 0.80 else 0,  # 80% have motorcycles (0-2)
        'ebike': random_int(0, 1) if random.random() < 0.15 else 0,  # 15% have e-bikes
        'tricycle': random_int(0, 1) if random.random() < 0.40 else 0,  # 40% have tricycles
        'bicycle': random_int(0, 2) if random.random() < 0.50 else 0,  # 50% have bicycles (0-2)
        'pedicab': random_int(0, 1) if random.random() < 0.08 else 0,  # 8% have pedicabs
        'motorboat': random_int(0, 1) if random.random() < 0.35 else 0,  # 35% have motorboats (fishing/coastal)
        'nonmotorboat': random_int(0, 2) if random.random() < 0.50 else 0,  # 50% have non-motor boats (0-2)
    }

def realistic_household_relationship(age, member_index, household_size):
    """Generate realistic household relationships based on age and position"""
    if member_index == 0:  # First member is usually head
        if age >= 18:
            return 1  # Head
        else:
            return 2  # Spouse (if under 18, might be child acting as head)
    elif member_index == 1 and age >= 18:
        # Second member, if adult, likely spouse
        return 2  # Spouse
    elif age < 18:
        # Children
        if age < 5:
            return 3  # Child
        elif age < 15:
            return 4  # Child
        else:
            return 5  # Child
    else:
        # Other adults
        if random.random() < 0.3:
            return 6  # Parent
        elif random.random() < 0.5:
            return 7  # Sibling
        else:
            return 8  # Other relative

# A. Core Demographic Characteristics
def generate_section_A(households):
    fields = [
        "barangay", "household_id", "member_id", "last_name", "first_name", "suffix", "middle_name",
        "relationship", "gender", "birthday", "age", "local_civil_registry", "marital_status",
        "ethnicity", "religion", "can_read_write", "highest_grade_completed"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            members = random_int(1, max_members_per_household)
            
            # Generate household surname (most members will share this)
            household_surname = random_filipino_surname()
            mother_maiden_name = random_middle_name(household_surname)  # Mother's maiden name for middle names
            
            for m in range(members):
                member_id = f"{household_id}-{m+1}"
                age = realistic_age_distribution()
                # Generate birthday based on age
                birth_year = 2024 - age
                birthday = f"{birth_year}-{random_int(1,12):02d}-{random_int(1,28):02d}"
                gender = realistic_gender_distribution()
                relationship_code = realistic_household_relationship(age, m, members)
                relationship = RELATIONSHIP_CODES[relationship_code]
                local_civil_registry = random.choice([1,2,8])
                marital_status = realistic_marital_status(age, gender)
                ethnicity = random_ethnicity()
                religion = random_religion()
                can_read_write = random_code(2) if age >= 5 else ''
                highest_grade_completed = realistic_education_level(age)
                
                # Name generation with household logic
                if m == 0:  # First member (usually head) gets household surname
                    last_name = household_surname
                elif m == 1 and relationship_code == 2:  # Spouse might keep their surname or take household surname
                    last_name = household_surname if random.random() < 0.70 else random_filipino_surname()
                elif relationship_code in [6, 7, 8]:  # Other relatives might have different surnames
                    last_name = household_surname if random.random() < 0.60 else random_filipino_surname()
                else:  # Children get household surname
                    last_name = household_surname
                
                first_name = random_filipino_first_name(gender)
                middle_name = mother_maiden_name if relationship_code in [3, 4, 5] else random_middle_name(last_name)
                suffix = random_suffix(gender)
                
                row = [
                    barangay, household_id, member_id,
                    last_name, first_name, suffix, middle_name,
                    relationship, gender, birthday, age,
                    local_civil_registry, marital_status, ethnicity, religion,
                    can_read_write, highest_grade_completed
                ]
                rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/A_Core_Demographic_Characteristics.csv", index=False)
    return df

# B. Other Demographic Characteristics
def generate_section_B(households):
    fields = [
        "barangay", "household_id", "member_id", "nuclear_family", "relationship_nuclear_head",
        "national_id_issued", "philsys_card_number", "solo_parent", "solo_parent_id", "senior_citizen_id",
        "pregnant", "lactating", "disability", "pwd_id", "type_of_disability",
        "seeing", "hearing", "walking", "remembering", "self_caring", "communication"
    ]
    disability_codes = list('ABCDEFGZ')
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            members = random_int(1, max_members_per_household)
            for m in range(members):
                member_id = f"{household_id}-{m+1}"
                age = realistic_age_distribution()
                # Generate birthday based on age
                birth_year = 2024 - age
                birthday = f"{birth_year}-{random_int(1,12):02d}-{random_int(1,28):02d}"
                gender = realistic_gender_distribution()
                nuclear_family = NUCLEAR_FAMILY_CODES[random_int(1,6)]
                relationship_nuclear_head = RELATIONSHIP_NUCLEAR_HEAD_CODES[random_int(0,10)]
                national_id_issued = random.choice([1,2,8])
                philsys_card_number = f"{random_int(1000000000000000,9999999999999999):016d}"
                solo_parent = random.choice([1,2,8])
                solo_parent_id = random.choice([1,2,8])
                senior_citizen_id = random.choice([1,2,8]) if age >= 60 else ''
                pregnant = random_code(2) if gender == 2 and age > 10 else ''
                lactating = random_code(2) if gender == 2 and age > 10 else ''
                disability = random_code(2)
                pwd_id = random_code(2)
                type_of_disability = random_multi_code(disability_codes) if disability == 1 else ''
                seeing = random_code(4) if age >= 5 else ''
                hearing = random_code(4) if age >= 5 else ''
                walking = random_code(4) if age >= 5 else ''
                remembering = random_code(4) if age >= 5 else ''
                self_caring = random_code(4) if age >= 5 else ''
                communication = random_code(4) if age >= 5 else ''
                row = [
                    barangay, household_id, member_id,
                    nuclear_family, relationship_nuclear_head, national_id_issued, philsys_card_number,
                    solo_parent, solo_parent_id, senior_citizen_id, pregnant, lactating,
                    disability, pwd_id, type_of_disability,
                    seeing, hearing, walking, remembering, self_caring, communication
                ]
                rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/B_Other_Demographic_Characteristics.csv", index=False)
    return df

# C. Migration
def generate_section_C(households):
    fields = [
        "barangay", "household_id", "member_id", "filipino_citizen", "overseas_filipino",
        "other_location_resided", "province_moved", "city_moved", "barangay_moved",
        "month_year_moved", "province_from", "city_from", "barangay_from", "internal_displacement"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            members = random_int(1, max_members_per_household)
            for m in range(members):
                member_id = f"{household_id}-{m+1}"
                age = realistic_age_distribution()
                # Generate birthday based on age
                birth_year = 2024 - age
                birthday = f"{birth_year}-{random_int(1,12):02d}-{random_int(1,28):02d}"
                filipino_citizen = random_code(3)
                overseas_filipino = OVerseas_FILIPINO_CODES[random_int(1,7)] if age >= 15 else ''
                other_location_resided = random_code(2)
                province_moved = f"{random_int(100,999):03d}" if other_location_resided == 1 else ''
                city_moved = f"{random_int(100,999):03d}" if other_location_resided == 1 else ''
                barangay_moved = f"{random_int(100,999):03d}" if other_location_resided == 1 else ''
                month_year_moved = f"{random_int(1,12):02d}-{random_int(2000,2024)}" if other_location_resided == 1 else ''
                province_from = f"{random_int(100,999):03d}" if other_location_resided == 1 else ''
                city_from = f"{random_int(100,999):03d}" if other_location_resided == 1 else ''
                barangay_from = f"{random_int(100,999):03d}" if other_location_resided == 1 else ''
                internal_displacement = INTERNAL_DISPLACEMENT_CODES[random_int(1,5)]
                row = [
                    barangay, household_id, member_id,
                    filipino_citizen, overseas_filipino,
                    other_location_resided, province_moved, city_moved, barangay_moved,
                    month_year_moved, province_from, city_from, barangay_from, internal_displacement
                ]
                rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/C_Migration.csv", index=False)
    return df

# D. Education
# Realistic skills training options
SKILLS_TRAINING_LIST = [
    "Fishing Techniques", "Fish Processing", "Boat Operation", "Net Making", "Aquaculture",
    "Coconut Processing", "Rice Farming", "Vegetable Growing", "Livestock Raising",
    "Mining Safety", "Heavy Equipment Operation", "Welding", "Carpentry", "Driving",
    "Computer Literacy", "Dressmaking", "Tailoring", "Food Processing", "Beauty Care",
    "Electrical Installation", "Plumbing", "Automotive Servicing", "Baking", "Masonry",
    "Electronics Repair", "Housekeeping", "Cookery", "Barista Training", "HVAC Servicing", "Agricultural Training"
]

def random_skills_training():
    # 15% chance to have a value, else blank
    if random.random() < 0.15:
        return random.choice(SKILLS_TRAINING_LIST)
    return ''

def generate_section_D(households):
    fields = [
        "barangay", "household_id", "member_id", "attended_school", "school_attending", "current_grade_year",
        "reason_not_attending", "tvet_graduate", "tvet_student", "skills_training"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            members = random.randint(1, max_members_per_household)
            for m in range(members):
                member_id = f"{household_id}-{m+1}"
                age = realistic_age_distribution()
                # Generate birthday based on age
                birth_year = 2024 - age
                birthday = f"{birth_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
                attended_school = random_code(2) if age >= 3 else ''
                school_attending = random_code(3) if age >= 3 else ''
                current_grade_year = random.choice(EDUCATION_CODES) if age >= 3 else ''
                reason_not_attending = random.choice(REASON_NOT_ATTENDING_CODES) if attended_school == 2 and age >= 3 else ''
                tvet_graduate = random_code(2) if age >= 15 else ''
                tvet_student = random_code(2) if age >= 15 else ''
                skills_training = random_skills_training() if age >= 15 else ''
                row = [
                    barangay, household_id, member_id,
                    attended_school, school_attending, current_grade_year,
                    reason_not_attending, tvet_graduate, tvet_student, skills_training
                ]
                rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/D_Education.csv", index=False)
    return df

# E. Economic Characteristics
def generate_section_E(households):
    fields = [
        "barangay", "household_id", "member_id", "worked_last_week", "job_last_week", "work_prov", "work_city",
        "primary_occupation", "industry", "nature_of_employment", "class_of_worker", "basis_of_payment",
        "other_job", "worked_hours", "want_more_hours", "farmer", "fisher", "looking_for_work",
        "reason_not_looking", "availability_for_work", "willing_to_work"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            members = random_int(1, max_members_per_household)
            for m in range(members):
                member_id = f"{household_id}-{m+1}"
                age = realistic_age_distribution()
                # Generate birthday based on age
                birth_year = 2024 - age
                birthday = f"{birth_year}-{random_int(1,12):02d}-{random_int(1,28):02d}"
                gender = realistic_gender_distribution()
                worked_last_week = realistic_employment_status(age, gender) if age >= 5 else ''
                job_last_week = random_code(3) if age >= 5 and worked_last_week == 1 else ''
                work_prov = f"{random_int(100,999):03d}" if age >= 5 and worked_last_week == 1 else ''
                work_city = f"{random_int(100,999):03d}" if age >= 5 and worked_last_week == 1 else ''
                occupation = realistic_occupation(age, gender)
                primary_occupation = f"{random_int(100000,999999):06d}" if age >= 5 and worked_last_week == 1 else ''
                industry = f"{random_int(10000,99999):05d}" if age >= 5 and worked_last_week == 1 else ''
                nature_of_employment = NATURE_OF_EMPLOYMENT_CODES[random_int(1,3)] if age >= 5 and worked_last_week == 1 else ''
                class_of_worker = CLASS_OF_WORKER_CODES[random_int(0,6)] if age >= 5 and worked_last_week == 1 else ''
                basis_of_payment = BASIS_OF_PAYMENT_CODES[random_int(0,7)] if age >= 5 and worked_last_week == 1 else ''
                other_job = random_code(2) if age >= 5 and worked_last_week == 1 else ''
                worked_hours = random_int(20, 60) if age >= 5 and worked_last_week == 1 else ''
                want_more_hours = random_code(2) if age >= 5 and worked_last_week == 1 else ''
                farmer = 1 if occupation == "Farming" else 2 if age >= 5 else ''
                fisher = 1 if occupation == "Fishing" else 2 if age >= 5 else ''
                looking_for_work = 1 if worked_last_week == 2 and age >= 15 else 2 if age >= 5 else ''
                reason_not_looking = random.choice(REASON_NOT_LOOKING_CODES) if looking_for_work == 2 and age >= 5 else ''
                availability_for_work = random_code(2) if looking_for_work == 1 and age >= 5 else ''
                willing_to_work = random_code(2) if age >= 5 else ''
                row = [
                    barangay, household_id, member_id,
                    worked_last_week, job_last_week, work_prov, work_city,
                    primary_occupation, industry, nature_of_employment, class_of_worker, basis_of_payment,
                    other_job, worked_hours, want_more_hours, farmer, fisher, looking_for_work,
                    reason_not_looking, availability_for_work, willing_to_work
                ]
                rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/E_Economic_Characteristics.csv", index=False)
    return df

# F. Health
def generate_section_F(households):
    fields = [
        "barangay", "household_id", "any_sick", "got_treatment", "where_treated", "reason_no_treatment", 
        "opt_measured", "child_death", "age_of_death", "cause_of_death"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            any_sick = random_code(2)
            got_treatment = random_code(2) if any_sick == 1 else ''
            where_treated = random.choice(MEDICAL_TREATMENT_FACILITY_CODES) if any_sick == 1 and got_treatment == 1 else ''
            reason_no_treatment = random.choice(REASON_NO_TREATMENT_CODES) if any_sick == 1 and got_treatment == 2 else ''
            opt_measured = random_code(2)
            child_death = random_code(2)
            age_of_death = random.randint(1,60) if child_death == 1 else ''
            cause_of_death = random.choice(CAUSE_OF_DEATH_CODES) if child_death == 1 else ''
            row = [
                barangay, household_id, any_sick, got_treatment, where_treated, reason_no_treatment, 
                opt_measured, child_death, age_of_death, cause_of_death
            ]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/F_Health.csv", index=False)
    return df

# G. Food Security
def generate_section_G(households):
    fields = [
        "barangay", "household_id", "worried_food", "unable_eat_healthy", "few_kinds_food", 
        "skipped_meal", "ate_less", "ran_out_food", "hungry_no_eat", "one_day_no_eat"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            row = [barangay, household_id] + [random_code(2) for _ in range(8)]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/G_Food_Security.csv", index=False)
    return df

# H. Assistance from abroad
def generate_section_H(households):
    fields = ["barangay", "household_id", "received_assistance"]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            row = [barangay, household_id, random_code(2)]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/H_Assistance_Abroad.csv", index=False)
    return df

# I. Financial account
def generate_section_I(households):
    fields = ["barangay", "household_id", "financial_accounts"]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            accounts = random.choice(['A','B','C','D','E','F','G','Y','Z'])
            row = [barangay, household_id, accounts]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/I_Financial_Account.csv", index=False)
    return df

# J. Disaster preparedness
# Realistic other shock events
OTHER_SHOCK_LIST = [
    "Typhoon", "Landslide", "Flooding", "Storm Surge", "Pandemic", 
    "Armed Conflict", "Crop Disease", "Animal Disease", "Drought", "Extreme Heat",
    "Forest Fire", "Mining Accident", "Oil Spill", "Earthquake", "Tsunami",
    "Volcanic Activity", "Pest Infestation", "Power Outage", "Water Shortage", "Fire"
]

def random_other_shock():
    # 12% chance to have a value, else blank
    if random.random() < 0.12:
        return random.choice(OTHER_SHOCK_LIST)
    return ''

def generate_section_J(households):
    fields = [
        "barangay", "household_id", "typhoon", "power_outage", "drought", "rain_flood", 
        "erosion", "earthquake", "fire", "crop_pests", "livestock_pests", 
        "stored_crop_pests", "crop_failed", "livestock_died", "mining_pollution", 
        "building_collapsed", "price_increase", "political_conflict", "death_member", 
        "illness_member", "other_shock", "know_evac_area", "contact_lgu"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            shocks = [random.randint(0,10) for _ in range(18)]
            other_shock = random_other_shock()
            know_evac_area = random_code(2)
            contact_lgu = random_code(2)
            row = [barangay, household_id] + shocks + [other_shock, know_evac_area, contact_lgu]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/J_Disaster_Preparedness.csv", index=False)
    return df

# K. Internet Access
def generate_section_K(households):
    fields = ["barangay", "household_id", "access_internet", "internet_for_all", "type_connection"]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            # Lower internet access in rural areas
            access_internet = 1 if random.random() < 0.40 else 2  # 40% have internet access
            internet_for_all = 1 if access_internet == 1 and random.random() < 0.60 else 2  # 60% of those with access have it for all
            # More basic connection types in rural areas
            connection_types = ['A', 'B', 'C', 'D']  # A=Mobile, B=Fixed, C=Public, D=Others
            type_connection = random.choice(connection_types) if access_internet == 1 else 'D'
            row = [barangay, household_id, access_internet, internet_for_all, type_connection]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/K_Internet_Access.csv", index=False)
    return df

# L. Public Safety
def generate_section_L(households):
    fields = ["barangay", "household_id", "walk_safe_night"]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            row = [barangay, household_id, random.choice(PUBLIC_SAFETY_CODES)]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/L_Public_Safety.csv", index=False)
    return df

# M. Social Protection
def generate_section_M(households):
    fields = [
        "barangay", "household_id", "sss_member", "gsis_member", "philhealth_member", "other_medical_member",
        "sss_received", "gsis_received", "philhealth_received", "other_medical_received",
        "4ps_member", "socpen_member", "aics_member", "walang_gutom_member", 
        "education_assist_member", "employment_assist_member", "other_program_member",
        "4ps_received", "socpen_received", "aics_received", "walang_gutom_received",
        "education_assist_received", "employment_assist_received", "other_program_received", "pantawid_id"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            # Social programs based on 2nd municipal income class and 31.52% poverty
            sss_member = 1 if random.random() < 0.35 else 2  # 35% SSS membership (2nd income class)
            gsis_member = 1 if random.random() < 0.20 else 2  # 20% GSIS membership (government workers)
            philhealth_member = 1 if random.random() < 0.85 else 2  # 85% PhilHealth membership
            other_medical_member = 1 if random.random() < 0.15 else 2  # 15% other medical
            sss_received = 1 if sss_member == 1 and random.random() < 0.70 else 2
            gsis_received = 1 if gsis_member == 1 and random.random() < 0.80 else 2
            philhealth_received = 1 if philhealth_member == 1 and random.random() < 0.60 else 2
            other_medical_received = 1 if other_medical_member == 1 and random.random() < 0.50 else 2
            # 4Ps participation based on 31.52% poverty incidence
            pantawid_id = f"{random_int(1000000000000000000,9999999999999999999):019d}" if random.random() < 0.32 else ''  # 32% 4Ps participation
            # Other programs with realistic rural participation
            other_values = [random_code(2) for _ in range(14)]  # Keep other programs random for now
            row = [barangay, household_id, sss_member, gsis_member, philhealth_member, other_medical_member,
                   sss_received, gsis_received, philhealth_received, other_medical_received] + other_values + [pantawid_id]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/M_Social_Protection.csv", index=False)
    return df

# N. Water, Sanitation, and Hygiene
def generate_section_N(households):
    fields = [
        "barangay", "household_id", "main_water_source", "main_drinking_water", "main_cooking_water",
        "location_water_source", "minutes_collect_water", "member_fetch_water", "distance_water_source",
        "toilet_facility", "location_toilet", "shared_toilet", "open_to_public", "garbage_disposal",
        "handwashing_facility", "water_availability", "soap_availability", "handwashing_material"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            water_source, toilet_facility = realistic_water_sanitation()
            main_water_source = water_source
            main_drinking_water = random.choice(DRINKING_COOKING_WATER_CODES)
            main_cooking_water = random.choice(DRINKING_COOKING_WATER_CODES)
            location_water_source = random_code(3)
            minutes_collect_water = random_int(0, 30) if water_source in [3,4,5,6,7] else 0  # More realistic collection time
            member_fetch_water = random_code(6)
            distance_water_source = random_int(0, 5) if water_source in [3,4,5,6,7] else 0  # Shorter distances
            toilet_facility = toilet_facility
            location_toilet = random_code(3)
            shared_toilet = 1 if toilet_facility in [11,12,13] else 2  # More shared facilities
            open_to_public = random_code(2)
            garbage_disposal = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'Z'])  # More varied disposal
            handwashing_facility = random.choice([1,2,3,4,5,9])  # More basic facilities
            water_availability = 1 if water_source in [1,2,3] else 2  # Less reliable water
            soap_availability = 1 if random.random() < 0.70 else 2  # 70% have soap
            handwashing_material = random.choice(['A', 'B', 'C', 'Z'])
            row = [
                barangay, household_id, main_water_source, main_drinking_water, main_cooking_water,
                location_water_source, minutes_collect_water, member_fetch_water, distance_water_source,
                toilet_facility, location_toilet, shared_toilet, open_to_public, garbage_disposal,
                handwashing_facility, water_availability, soap_availability, handwashing_material
            ]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/N_Water_Sanitation_Hygiene.csv", index=False)
    return df

# O. Housing Characteristics
def generate_section_O(households):
    fields = [
        "barangay", "household_id", "building_type", "num_floors", "roof_material", "wall_material", 
        "housing_material", "floor_area", "num_bedrooms", "tenure_status", "date_construction", 
        "electricity", "lighting_fuel", "cooking_fuel", "num_refrigerator", "num_aircon", 
        "num_washing_machine", "num_stove", "num_radio", "num_tv", "num_stereo", 
        "num_landline", "num_cellphone_keypad", "num_cellphone_smart", "num_tablet", 
        "num_computer", "num_car", "num_van", "num_jeep", "num_truck", "num_motorcycle", 
        "num_ebike", "num_tricycle", "num_bicycle", "num_pedicab", "num_motorboat", "num_nonmotorboat"
    ]
    rows = []
    for barangay, count in households.items():
        for h in range(count):
            household_id = f"{barangay[:3].upper()}-{h+1:04d}"
            building_type = random.choice([1,2,3,4,5,6,7,8,9,10])  # More single-family homes
            num_floors = 1 if random.random() < 0.75 else random_int(1,2)  # 75% single floor (2nd income class)
            roof_material, wall_material = realistic_housing_materials()
            housing_material = random.choice([1,2,3,4,5,6,9])  # Better materials due to income class
            floor_area = round(random.uniform(30.0, 150.0), 2)  # Larger houses (2nd income class)
            num_bedrooms = random_int(1, 5)  # More bedrooms (2nd income class)
            tenure_status = random.choice([1,2,3,4,5,6,7])  # More varied tenure
            date_construction = f"{random_int(1980,2024)}-{random_int(1,12):02d}"  # More recent construction
            electricity = 1 if random.random() < 0.90 else 2  # 90% have electricity (2nd income class)
            lighting_fuel = 1 if electricity == 1 else random.choice([2,3,4,5,6,9])  # Electric or alternatives
            cooking_fuel = random.choice([1,2,3,4,5,6,9])  # More varied cooking fuels
            
            # Generate realistic vehicle and appliance counts for rural province
            items = realistic_rural_vehicles_appliances()
            
            row = [
                barangay, household_id, building_type, num_floors, roof_material, wall_material, housing_material,
                floor_area, num_bedrooms, tenure_status, date_construction, electricity, lighting_fuel, cooking_fuel,
                items['refrigerator'], items['aircon'], items['washing_machine'], items['stove'], 
                items['radio'], items['tv'], items['stereo'], items['landline'], items['cellphone_keypad'], 
                items['cellphone_smart'], items['tablet'], items['computer'], items['car'], items['van'], 
                items['jeep'], items['truck'], items['motorcycle'], items['ebike'], items['tricycle'], 
                items['bicycle'], items['pedicab'], items['motorboat'], items['nonmotorboat']
            ]
            rows.append(row)
    df = pd.DataFrame(rows, columns=fields)
    df.to_csv("cbms_csv/O_Housing_Characteristics.csv", index=False)
    return df



# Generate code legend CSVs
def generate_code_legends():
    # Relationship codes legend
    relationship_legend = [
        ["01", "Household Head"],
        ["02", "Spouse"],
        ["03", "Son/Daughter"],
        ["04", "Son/Daughter-in-law"],
        ["05", "Grandson/Granddaughter"],
        ["06", "Father/Mother"],
        ["07", "Father/Mother-in-law"],
        ["08", "Brother/Sister"],
        ["09", "Brother/Sister-in-law"],
        ["10", "Nephew/Niece"],
        ["11", "Uncle/Aunt"],
        ["12", "Cousin"],
        ["13", "Other Relative"],
        ["14", "Non-relative"],
        ["15", "Domestic Helper"],
        ["16", "Boarder"],
        ["17", "Other Non-relative"],
        ["18", "Adopted Child"],
        ["19", "Step Child"],
        ["20", "Foster Child"],
        ["21", "Common Law Spouse"],
        ["22", "Same Sex Partner"],
        ["23", "Other"],
        ["24", "Not Stated"],
        ["25", "Unknown"],
        ["26", "Refused to Answer"]
    ]
    
    df_rel = pd.DataFrame(relationship_legend, columns=["code", "description"])
    df_rel.to_csv("cbms_csv/legend_relationship_codes.csv", index=False)
    
    # Education codes legend
    education_legend = [
        ["00000000", "No Grade Completed"],
        ["01000000", "Preschool"],
        ["02000000", "Kindergarten"],
        ["02100000", "Special Education"],
        ["10000101", "Grade 1"],
        ["10000102", "Grade 2"],
        ["10000103", "Grade 3"],
        ["10000104", "Grade 4"],
        ["10000105", "Grade 5"],
        ["10000106", "Grade 6"],
        ["10000107", "Grade 7"],
        ["10000108", "Grade 8"],
        ["11000101", "First Year High School"],
        ["11000102", "Second Year High School"],
        ["11000103", "Third Year High School"],
        ["11000104", "Fourth Year High School"],
        ["11000105", "High School Graduate"],
        ["11000108", "High School Level"],
        ["11000201", "First Year College"],
        ["11000202", "Second Year College"],
        ["11000203", "Third Year College"],
        ["11000301", "Fourth Year College"],
        ["11000302", "College Graduate"],
        ["20400101", "Post Baccalaureate Certificate"],
        ["20400102", "Post Baccalaureate Diploma"],
        ["20400103", "Master's Degree"],
        ["20400105", "Doctorate Degree"],
        ["21400101", "Post Secondary Certificate"],
        ["21400102", "Post Secondary Diploma"],
        ["21400103", "Associate Degree"],
        ["21400105", "Bachelor's Degree"],
        ["21400201", "Post Secondary Certificate"],
        ["21400202", "Post Secondary Diploma"],
        ["21400203", "Associate Degree"],
        ["21400301", "Post Secondary Certificate"],
        ["21400302", "Post Secondary Diploma"],
        ["30400106", "Post Secondary Certificate"],
        ["30400107", "Post Secondary Diploma"],
        ["30400108", "Associate Degree"],
        ["30400109", "Bachelor's Degree"],
        ["30400110", "Master's Degree"],
        ["30400111", "Doctorate Degree"],
        ["30400201", "Post Secondary Certificate"],
        ["30400203", "Post Secondary Diploma"],
        ["30400204", "Associate Degree"],
        ["30400205", "Bachelor's Degree"],
        ["30400206", "Master's Degree"],
        ["30400207", "Doctorate Degree"],
        ["30400208", "Post Secondary Certificate"],
        ["30400301", "Post Secondary Diploma"],
        ["30400303", "Associate Degree"],
        ["30500006", "Post Secondary Certificate"],
        ["30500007", "Post Secondary Diploma"],
        ["30500008", "Associate Degree"],
        ["30500009", "Bachelor's Degree"],
        ["30500010", "Master's Degree"],
        ["30500011", "Doctorate Degree"],
        ["40000001", "Post Secondary Certificate"],
        ["40000002", "Post Secondary Diploma"],
        ["40000003", "Associate Degree"],
        ["50000001", "Post Secondary Certificate"],
        ["50000002", "Post Secondary Diploma"],
        ["50000003", "Associate Degree"],
        ["60000001", "Post Secondary Certificate"],
        ["60000002", "Post Secondary Diploma"],
        ["60000003", "Associate Degree"],
        ["60000004", "Bachelor's Degree"],
        ["60000005", "Master's Degree"],
        ["60000006", "Doctorate Degree"],
        ["70000010", "Post Secondary Certificate"],
        ["80000010", "Post Secondary Diploma"]
    ]
    
    df_edu = pd.DataFrame(education_legend, columns=["code", "description"])
    df_edu.to_csv("cbms_csv/legend_education_codes.csv", index=False)
    
    # Nuclear family codes legend
    nuclear_family_legend = [
        ["01", "Nuclear Family 1"],
        ["02", "Nuclear Family 2"],
        ["03", "Nuclear Family 3"],
        ["04", "Nuclear Family 4"],
        ["05", "Nuclear Family 5"],
        ["06", "Nuclear Family 6"]
    ]
    
    df_nuc = pd.DataFrame(nuclear_family_legend, columns=["code", "description"])
    df_nuc.to_csv("cbms_csv/legend_nuclear_family_codes.csv", index=False)
    
    # Relationship to nuclear head codes legend
    nuclear_head_legend = [
        ["00", "Nuclear Family Head"],
        ["01", "Spouse"],
        ["02", "Son/Daughter"],
        ["03", "Son/Daughter-in-law"],
        ["04", "Grandson/Granddaughter"],
        ["05", "Father/Mother"],
        ["06", "Brother/Sister"],
        ["07", "Other Relative"],
        ["08", "Non-relative"],
        ["09", "Other"],
        ["10", "Not Stated"]
    ]
    
    df_nuc_head = pd.DataFrame(nuclear_head_legend, columns=["code", "description"])
    df_nuc_head.to_csv("cbms_csv/legend_nuclear_head_codes.csv", index=False)
    
    # Overseas Filipino codes legend
    overseas_legend = [
        ["1", "Overseas Filipino Worker"],
        ["2", "Overseas Filipino Student"],
        ["3", "Overseas Filipino Immigrant"],
        ["4", "Overseas Filipino Tourist"],
        ["5", "Overseas Filipino Business Person"],
        ["6", "Other Overseas Filipino"],
        ["7", "Not Applicable"]
    ]
    
    df_overseas = pd.DataFrame(overseas_legend, columns=["code", "description"])
    df_overseas.to_csv("cbms_csv/legend_overseas_filipino_codes.csv", index=False)
    
    # Internal displacement codes legend
    displacement_legend = [
        ["1", "Natural Disaster"],
        ["2", "Armed Conflict"],
        ["3", "Development Project"],
        ["4", "Other"],
        ["5", "Not Applicable"]
    ]
    
    df_disp = pd.DataFrame(displacement_legend, columns=["code", "description"])
    df_disp.to_csv("cbms_csv/legend_displacement_codes.csv", index=False)
    
    # Employment codes legend
    employment_legend = [
        ["1", "Regular/Permanent"],
        ["2", "Contractual/Fixed Term"],
        ["3", "Casual/Seasonal"]
    ]
    
    df_emp = pd.DataFrame(employment_legend, columns=["code", "description"])
    df_emp.to_csv("cbms_csv/legend_employment_codes.csv", index=False)
    
    # Class of worker codes legend
    worker_class_legend = [
        ["0", "Private Household"],
        ["1", "Private Establishment"],
        ["2", "Government/Corporation"],
        ["3", "Self-employed"],
        ["4", "Employer"],
        ["5", "Unpaid Family Worker"],
        ["6", "Other"]
    ]
    
    df_worker = pd.DataFrame(worker_class_legend, columns=["code", "description"])
    df_worker.to_csv("cbms_csv/legend_worker_class_codes.csv", index=False)
    
    # Basis of payment codes legend
    payment_legend = [
        ["0", "Paid in Cash"],
        ["1", "Paid in Kind"],
        ["2", "Commission"],
        ["3", "Piece Rate"],
        ["4", "Hourly Rate"],
        ["5", "Daily Rate"],
        ["6", "Weekly Rate"],
        ["7", "Monthly Rate"]
    ]
    
    df_pay = pd.DataFrame(payment_legend, columns=["code", "description"])
    df_pay.to_csv("cbms_csv/legend_payment_codes.csv", index=False)
    
    # Medical treatment facility codes legend
    medical_legend = [
        ["A", "Public Hospital"],
        ["B", "Private Hospital"],
        ["C", "Public Health Center"],
        ["D", "Private Clinic"],
        ["E", "Barangay Health Station"],
        ["F", "Rural Health Unit"],
        ["G", "Medical Mission"],
        ["H", "Traditional Healer"],
        ["I", "Pharmacy"],
        ["J", "Dental Clinic"],
        ["K", "Optical Clinic"],
        ["L", "Laboratory"],
        ["M", "X-ray Facility"],
        ["N", "Rehabilitation Center"],
        ["O", "Mental Health Facility"],
        ["P", "Maternity Home"],
        ["Q", "Birthing Home"],
        ["R", "Ambulance Service"],
        ["S", "Home Care"],
        ["T", "Other"],
        ["Z", "Not Specified"]
    ]
    
    df_med = pd.DataFrame(medical_legend, columns=["code", "description"])
    df_med.to_csv("cbms_csv/legend_medical_facility_codes.csv", index=False)
    
    # Water source codes legend
    water_legend = [
        ["1", "Piped Water into Dwelling"],
        ["2", "Piped Water into Yard/Plot"],
        ["3", "Piped Water to Neighbor"],
        ["4", "Public Tap/Standpipe"],
        ["5", "Tubewell/Borehole"],
        ["6", "Protected Dug Well"],
        ["7", "Unprotected Dug Well"],
        ["8", "Protected Spring"],
        ["9", "Unprotected Spring"],
        ["10", "Rainwater Collection"],
        ["99", "Not Stated"]
    ]
    
    df_water = pd.DataFrame(water_legend, columns=["code", "description"])
    df_water.to_csv("cbms_csv/legend_water_source_codes.csv", index=False)
    
    # Toilet facility codes legend
    toilet_legend = [
        ["11", "Flush to Sewer System"],
        ["12", "Flush to Septic Tank"],
        ["13", "Flush to Open Drain"],
        ["14", "Flush to Other"],
        ["15", "Flush, Don't Know Where"],
        ["21", "Pit Latrine with Slab"],
        ["22", "Pit Latrine without Slab"],
        ["23", "Composting Toilet"],
        ["31", "Hanging Toilet"],
        ["41", "Bucket Toilet"],
        ["51", "Other"],
        ["71", "No Toilet Facility"],
        ["95", "Not Stated"],
        ["99", "Unknown"]
    ]
    
    df_toilet = pd.DataFrame(toilet_legend, columns=["code", "description"])
    df_toilet.to_csv("cbms_csv/legend_toilet_codes.csv", index=False)
    
    # Building type codes legend
    building_legend = [
        ["1", "Single House"],
        ["2", "Duplex"],
        ["3", "Row House"],
        ["4", "Apartment"],
        ["5", "Condominium"],
        ["6", "Tenement"],
        ["7", "Commercial/Industrial"],
        ["8", "Institutional Living Quarter"],
        ["9", "Other"],
        ["10", "Not Stated"]
    ]
    
    df_building = pd.DataFrame(building_legend, columns=["code", "description"])
    df_building.to_csv("cbms_csv/legend_building_type_codes.csv", index=False)
    
    # Roof material codes legend
    roof_legend = [
        ["1", "Galvanized Iron/Aluminum"],
        ["2", "Tile"],
        ["3", "Concrete"],
        ["4", "Wood"],
        ["5", "Cogon/Nipa/Anahaw"],
        ["6", "Asbestos"],
        ["7", "Other"],
        ["9", "Not Stated"]
    ]
    
    df_roof = pd.DataFrame(roof_legend, columns=["code", "description"])
    df_roof.to_csv("cbms_csv/legend_roof_material_codes.csv", index=False)
    
    # Wall material codes legend
    wall_legend = [
        ["1", "Concrete/Brick/Stone"],
        ["2", "Wood"],
        ["3", "Galvanized Iron/Aluminum"],
        ["4", "Bamboo/Sawali/Cogon"],
        ["5", "Asbestos"],
        ["6", "Glass"],
        ["7", "Bark"],
        ["8", "Makeshift/Salvaged Materials"],
        ["9", "Other"],
        ["10", "No Walls"],
        ["11", "Not Stated"],
        ["12", "Unknown"],
        ["99", "Not Applicable"]
    ]
    
    df_wall = pd.DataFrame(wall_legend, columns=["code", "description"])
    df_wall.to_csv("cbms_csv/legend_wall_material_codes.csv", index=False)
    
    # Tenure status codes legend
    tenure_legend = [
        ["1", "Owned, Being Amortized"],
        ["2", "Owned, Fully Paid"],
        ["3", "Rented"],
        ["4", "Rent Free with Consent of Owner"],
        ["5", "Rent Free without Consent of Owner"],
        ["6", "Not Stated"],
        ["7", "Other"]
    ]
    
    df_tenure = pd.DataFrame(tenure_legend, columns=["code", "description"])
    df_tenure.to_csv("cbms_csv/legend_tenure_codes.csv", index=False)
    
    # Fuel codes legend
    fuel_legend = [
        ["1", "Electricity"],
        ["2", "LPG/Natural Gas"],
        ["3", "Kerosene"],
        ["4", "Charcoal"],
        ["5", "Firewood"],
        ["6", "Other"],
        ["9", "Not Stated"]
    ]
    
    df_fuel = pd.DataFrame(fuel_legend, columns=["code", "description"])
    df_fuel.to_csv("cbms_csv/legend_fuel_codes.csv", index=False)
    
    # Public safety codes legend
    safety_legend = [
        ["1", "Very Safe"],
        ["2", "Safe"],
        ["3", "Neither Safe nor Unsafe"],
        ["4", "Unsafe"],
        ["5", "Very Unsafe"],
        ["8", "Don't Know"]
    ]
    
    df_safety = pd.DataFrame(safety_legend, columns=["code", "description"])
    df_safety.to_csv("cbms_csv/legend_public_safety_codes.csv", index=False)
    
    # Reason not attending school codes legend
    reason_school_legend = [
        ["01", "Too Young to Go to School"],
        ["02", "Illness/Disability"],
        ["03", "Too Far from School"],
        ["04", "High Cost of Education"],
        ["05", "Early Marriage"],
        ["06", "Family Problems"],
        ["07", "Other Family Reasons"],
        ["08", "Not Interested"],
        ["09", "Looking for Work"],
        ["10", "Found Work"],
        ["11", "Housekeeping"],
        ["12", "Other Personal Reasons"],
        ["13", "School Not Available"],
        ["14", "School Destroyed"],
        ["15", "School Closed"],
        ["16", "Other School Reasons"],
        ["17", "Other"],
        ["18", "Not Stated"],
        ["99", "Unknown"]
    ]
    
    df_reason = pd.DataFrame(reason_school_legend, columns=["code", "description"])
    df_reason.to_csv("cbms_csv/legend_reason_not_attending_codes.csv", index=False)
    
    # Reason not looking for work codes legend
    reason_work_legend = [
        ["01", "Believes No Work Available"],
        ["02", "Waiting for Results of Previous Application"],
        ["03", "Temporary Illness/Disability"],
        ["04", "Bad Weather"],
        ["05", "Waiting for Rehire"],
        ["06", "Too Young/Old"],
        ["07", "Other Personal Reasons"],
        ["08", "Housekeeping"],
        ["09", "Going to School"],
        ["10", "Retired"],
        ["99", "Not Stated"]
    ]
    
    df_work_reason = pd.DataFrame(reason_work_legend, columns=["code", "description"])
    df_work_reason.to_csv("cbms_csv/legend_reason_not_looking_codes.csv", index=False)
    
    # Cause of death codes legend
    cause_death_legend = [
        ["01", "Natural Causes"],
        ["02", "Accident"],
        ["03", "Illness/Disease"],
        ["04", "Complications at Birth"],
        ["05", "Malnutrition"],
        ["06", "Infection"],
        ["07", "Congenital Anomaly"],
        ["08", "Other Medical"],
        ["09", "Other"],
        ["10", "Not Stated"],
        ["99", "Unknown"]
    ]
    
    df_death = pd.DataFrame(cause_death_legend, columns=["code", "description"])
    df_death.to_csv("cbms_csv/legend_cause_of_death_codes.csv", index=False)
    
    # Garbage disposal codes legend
    garbage_legend = [
        ["A", "Collected by Regular Truck Service"],
        ["B", "Collected by Private Company"],
        ["C", "Burned"],
        ["D", "Buried"],
        ["E", "Composted"],
        ["F", "Fed to Animals"],
        ["G", "Thrown into River/Stream"],
        ["H", "Thrown into Sea"],
        ["I", "Thrown in Street/Open Space"],
        ["Z", "Other"]
    ]
    
    df_garbage = pd.DataFrame(garbage_legend, columns=["code", "description"])
    df_garbage.to_csv("cbms_csv/legend_garbage_disposal_codes.csv", index=False)
    
    # Handwashing facility codes legend
    handwash_legend = [
        ["1", "Fixed Facility Used by Household"],
        ["2", "Fixed Facility Shared with Other Households"],
        ["3", "Mobile Facility"],
        ["4", "No Facility"],
        ["5", "Other"],
        ["9", "Not Stated"]
    ]
    
    df_handwash = pd.DataFrame(handwash_legend, columns=["code", "description"])
    df_handwash.to_csv("cbms_csv/legend_handwashing_facility_codes.csv", index=False)
    
    # Handwashing material codes legend
    handwash_material_legend = [
        ["A", "Soap and Water"],
        ["B", "Water Only"],
        ["C", "Other"],
        ["Z", "Not Stated"]
    ]
    
    df_handwash_mat = pd.DataFrame(handwash_material_legend, columns=["code", "description"])
    df_handwash_mat.to_csv("cbms_csv/legend_handwashing_material_codes.csv", index=False)
    
    print("Code legend CSVs generated successfully!")

def weighted_random_choice(choices):
    population, weights = zip(*choices)
    return random.choices(population, weights=weights, k=1)[0]

def random_religion():
    return weighted_random_choice(RELIGIONS)

def random_ethnicity():
    return random.choice(ETHNICITIES)

def zip_csvs(zip_name="cbms_csv.zip", folder="cbms_csv"):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('.csv'):
                    zipf.write(os.path.join(root, file), arcname=file)

if __name__ == "__main__":
    os.makedirs("cbms_csv", exist_ok=True)
    households = weighted_barangay_list(barangay_weights, total_population, target_households)
    
    # Generate all sections
    generate_section_A(households)
    generate_section_B(households)
    generate_section_C(households)
    generate_section_D(households)
    generate_section_E(households)
    generate_section_F(households)
    generate_section_G(households)
    generate_section_H(households)
    generate_section_I(households)
    generate_section_J(households)
    generate_section_K(households)
    generate_section_L(households)
    generate_section_M(households)
    generate_section_N(households)
    generate_section_O(households)
    
    # Generate code legends
    generate_code_legends()
    
    # Create zip file
    zip_csvs()
    print("All CSVs and code legends generated and zipped to cbms_csv.zip")
    
    # Original CSVs
    csv_files = [
        "A_Core_Demographic_Characteristics.csv",
        "B_Other_Demographic_Characteristics.csv", 
        "C_Migration.csv",
        "D_Education.csv",
        "E_Economic_Characteristics.csv",
        "F_Health.csv",
        "G_Food_Security.csv",
        "H_Assistance_Abroad.csv",
        "I_Financial_Account.csv",
        "J_Disaster_Preparedness.csv",
        "K_Internet_Access.csv",
        "L_Public_Safety.csv",
        "M_Social_Protection.csv",
        "N_Water_Sanitation_Hygiene.csv",
        "O_Housing_Characteristics.csv"
    ]
