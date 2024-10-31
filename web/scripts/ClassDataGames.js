export default class ClassDataGames {
    constructor() {
        this.path // Ruta donde se encuentra la data de la aplicación
        this.data // Data obtenida directamente desde partidos.json
        this.games // Juegos extraídos desde data
        this.filtered // Luego de aplicados los filtros a games se almacena en filtered
        this.compiled // Se almacena toda la información organizada para ser usada en la web
        this.local_storage_key = 'games'
    }
    set_path(path) {
        this.path =  path
       
    }
    async load_data() {
        const stored_data = localStorage.getItem(this.local_storage_key)
        if (stored_data !== undefined || stored_data !== null) {
            this.data = JSON.parse(stored_data)
 console.log(this.path)
        } else {
            try {
               console.log(this.path)
                const response = await fetch(this.path)
                if (!response.ok)
                    throw new Error(`Error al cargar el archivo desde ${path}`)
                this.data = await response.json
                console.log(this.data)
                localStorage.setItem(
                    this.local_storage_key,
                    JSON.stringify(this.data)
                )
            } catch (error) {
                console.error(error)
            }
        }
    }
    async get_data() {
        return await this.data
    }

    get_games(data = []) {
        return data.length === 0 ? this.data['games'] : data
    }

    get_item(item, data = []) {
        const result = [
            ...new Set(
                (data.length === 0 ? this.data['games'] : data).map(
                    e => e[item]
                )
            )
        ]
        return result
    }

    get_array_item(item = '', data = []) {
        let teams = new Set()
        const filter =
            item === 'ALL' ? data : data.filter(c => c['category'] === item)
        filter.forEach(t => t.teams.forEach(e => teams.add(e)))
        return [...teams]
    }

    get_teams(item = '', data = []) {
        const category =
            item.toUpperCase() === 'M'
                ? 'MASCULINO'
                : item.toUpperCase() === 'F'
                ? 'FEMENINO'
                : 'ALL'
        const result = this.get_array_item(
            category,
            data.length === 0 ? this.data['games'] : data
        )
        return result
    }

    get_tournaments(data = []) {
        return this.get_item('tournament', data)
    }

    get_years(data = []) {
        return this.get_item('year', data)
    }

    get_categories(data = []) {
        return this.get_item('category', data)
    }

    get_modalities(data = []) {
        return this.get_item('modality', data)
    }
}
