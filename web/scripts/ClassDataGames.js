export default class ClassDataGames {
    constructor() {
        this.path; // Ruta donde se encuentra la data de la aplicación
        this.data; // Data obtenida directamente desde partidos.json
        this.games; // Juegos extraídos desde data
        this.filtered; // Luego de aplicados los filtros a games se almacena en filtered
        this.compiled; // Se almacena toda la información organizada para ser usada en la web
        this.local_storage_key = "games";
    }
    set_path(path) {
        this.path = path;
    }
    async load_data() {
        //       const stored_data = localStorage.getItem(this.local_storage_key)
        //         if (stored_data !== undefined || stored_data !== null) {
        //             this.data = JSON.parse(stored_data)
        //         } else {
        try {
            const response = await fetch(this.path);

            if (!response.ok)
                throw new Error(`Error al cargar el archivo desde ${path}`);
            this.data = await response.json();
            this.compiled = {
                games: this.data.games,
                teams: this.data.info.teams,
                tournaments: this.data.info.tournaments,
                categories: this.data.info.categories,
                years: this.data.info.years,
                modalities: this.data.info.modalities,
                femaleteams : this.get_teams("F"),
                maleteams : this.get_teams("M")
            };

            localStorage.setItem(
                this.local_storage_key,
                JSON.stringify(this.data)
            );
        } catch (error) {
            console.error(error);
        }
        // }
    }
    async get_data() {
        return await this.data;
    }
    async get_compiled_data() {
        return await this.compiled;
    }

    get_games(data = []) {
        return data.length === 0 ? this.data["games"] : data;
    }

    get_item(item, data = []) {
        const result = [
            ...new Set(
                (data.length === 0 ? this.data["games"] : data).map(
                    e => e[item]
                )
            )
        ];
        return result;
    }

    get_array_item(item = "", data = []) {
        let teams = new Set();
        const filter =
            item === "ALL" ? data : data.filter(c => c["category"] === item);
        filter.forEach(t => t.teams.forEach(e => teams.add(e)));
        return [...teams];
    }

    get_teams(item = "", data = []) {
        const category =
            item.toUpperCase() === "M"
                ? "M"
                : item.toUpperCase() === "F"
                ? "F"
                : "ALL";
        const result = this.get_array_item(
            category,
            data.length === 0 ? this.data["games"] : data
        );
        return result;
    }

    get_tournaments(data = []) {
        return this.get_item("tournament", data);
    }

    get_years(data = []) {
        return this.get_item("year", data);
    }

    get_categories(data = []) {
        return this.get_item("category", data);
    }

    get_modalities(data = []) {
        return this.get_item("modality", data);
    }
}
