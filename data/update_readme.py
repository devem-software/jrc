import json
from datetime import datetime


def generate_readme(filename="partidos"):
    # Cargar los datos de los partidos desde el archivo JSON
    with open(f"data/{filename}.json", "r", encoding="utf8") as file:
        data = json.load(file)

    # Obtener información para el README
    last_update = data["info"]["last_update"]
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

### Última actualización
{last_update}

### Partidos totales jugados
{total_games}

### Torneos totales jugados
{total_tournaments}

### Partidos por torneo
"""
    for tournament, count in games_per_tournament.items():
        readme_content += f"- {tournament}: {count} partidos\n"

    readme_content += f"""

### Cantidad y lista de equipos masculinos
{len(male_teams)} equipos:
{'\n - '.join(sorted(male_teams))}

### Cantidad y lista de equipos femeninos
{len(female_teams)} equipos:
{'\n - '.join(sorted(female_teams))}
"""

    # Guardar la información en README.md
    with open("README.md", "w", encoding="utf8") as readme_file:
        readme_file.write(readme_content)


# Ejecuta la función para generar el README
generate_readme()
