import json
from datetime import datetime


def generate_table(array, columns, header):
    tabla_md = ""
    filas = [array[i : i + columns] for i in range(0, len(array), columns)]

    # Encabezados de las columnas
    encabezados = "| " + " | ".join([header] * columns) + " |"
    separador = "|" + "----|" * columns
    tabla_md += encabezados + "\n" + separador + "\n"

    # Añadir las filas
    for fila in filas:
        tabla_md += "| " + " | ".join(f"{elem}" for elem in fila) + " |\n"

    return tabla_md


def generate_readme(filename="partidos"):
    # Cargar los datos de los partidos desde el archivo JSON
    with open(f"data/{filename}.json", "r", encoding="utf8") as file:
        data = json.load(file)

    # Obtener información para el README
    last_update = data["info"]["last_update"]
    start = data["info"]["period"][1]
    end = data["info"]["period"][0]
    total_games = len(data["games"])
    torneos = set(game["tournament"] for game in data["games"] if game["tournament"])
    total_tournaments = len(torneos)

    # Contar partidos por torneo
    games_per_tournament = {}
    for game in data["games"]:
        tournament = game["tournament"]
        if tournament:
            games_per_tournament[tournament] = (
                games_per_tournament.get(tournament, 0) + 1
            )

    # Listar equipos masculinos y femeninos
    male_teams = set()
    female_teams = set()
    for game in data["games"]:
        # Aquí asumimos que las categorías "masculino" y "femenino" están en `game["category"]`
        if game["category"] == "MASCULINO":
            male_teams.update(game["teams"])
        elif game["category"] == "FEMENINO":
            female_teams.update(game["teams"])

    # Formato para el archivo README.md
    readme_content = f"""
# 🏉 LIGA DE RUGBY DE BOGOTÁ <BR/>🏃‍➡️ PARTIDOS JUGADOS

### 🗃️ Base de datos de los partidos subidos a YouTube <br/> por la liga de rugby de Bogotá desde {start}

## ⏱️Ultima actualización

### 🗓️ {last_update} 

### 💪{total_games} Partidos han sido jugados

---

## Partidos por torneo desde {start} hasta el {end}
"""
    table = "|Torneo|Partidos|"
    table += "\n|:--|--:|"
    for tournament, count in games_per_tournament.items():
        table += f"\n|{tournament}| {count}|"
    readme_content += table
    readme_content += f"""

---

## 👩‍🧑🏽‍👧🏻 Equipos participantes en los torneos

### {len(male_teams)} Equipos masculinos han participado desde {start}

<details>
<summary>🙎‍♂️ Click para ver los equipos masculinos</summary>
<br/>

"""
    readme_content += generate_table(list(male_teams), 3, "")

    readme_content += f"""

</details>

### {len(female_teams)} Equipos femeninos han participado desde {start}

<details>
<summary>🙎‍♀️ Click para ver los equipos femeninos</summary>
<br/>

"""
    readme_content += generate_table(list(female_teams), 3, "")

    readme_content += f"""

</details>
<br/>
<br/>

---

# 🐆 JAGUARES EN LA LIGA
"""

    # Guardar la información en README.md
    with open("README.md", "w", encoding="utf8") as readme_file:
        readme_file.write(readme_content)


# Ejecuta la función para generar el README
generate_readme()
