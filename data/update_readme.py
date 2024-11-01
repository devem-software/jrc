import json
from datetime import datetime


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
    readme_content = f"""# Partidos Liga de Rugby de Bogotá

## Base de datos de los partidos subidos a YouTube por la liga de rugby de Bogotá

### {last_update} Fue la última actualización: 

### {total_games} Partidos han sido jugados desde {start}: 

### {total_tournaments} Torneos se han jugados desde {start}
"""
    for torneo in torneos:
        readme_content += "\n - " + torneo

    readme_content += f"""

### Partidos por torneo desde {start} hasta el {end}
"""
    table = "|Torneo|Partidos|"
    table += "\n|:--|--:|"
    for tournament, count in games_per_tournament.items():
        table += f"\n|{tournament}| {count}|"
    readme_content += table
    readme_content += f"""

### {len(male_teams)} Equipos masculinos han participado desde {start}
"""
    for team in male_teams:
        readme_content += "\n - " + team

    readme_content += f"""

### {len(female_teams)} Equipos femeninos han participado desde {start}
"""
    for team in female_teams:
        readme_content += "\n - " + team

    readme_content += f"""
    
"""

    # Guardar la información en README.md
    with open("README.md", "w", encoding="utf8") as readme_file:
        readme_file.write(readme_content)


# Ejecuta la función para generar el README
generate_readme()
