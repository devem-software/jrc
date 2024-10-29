import { data_flating, get_data_from_json } from './functions.js'

export default class DataGamesClass {
    constructor() {
        this.Categories
        this.Data
        this.Femaleteams
        this.Filtered = []
        this.Games
        this.Maleteams
        this.Modalities
        this.Teams
        this.Tournaments
        this.Years
        this.Fompiled
    }

    async init() {
        try {
            this.Data = await get_data_from_json('../../data/partidos.json')
            this.set_Games()
            this.set_Item('Modalities', 'modality')
            this.set_Item('Categories', 'category')
            this.set_Item('Years', 'year')
            this.set_Item('Tournaments', 'tournament')
            await this.set_Teams()
            await this.set_Teams('FEMENINO')
            await this.set_Teams('MASCULINO')
            this.Filtered = this.Games
        } catch (error) {
            console.error(error)
        }
    }

    async set_Games() {
        if (this.Data && this.Data.games) {
            this.Games = this.Data.games
        } else {
            throw new Error('Games data not available')
        }
    }

    async set_Item(key, value) {
        if (this.Games) {
            let data = await this.Data
            this[key] = await data_flating(data.games, value)
        } else {
            throw new Error(`Error, ${value}`)
        }
    }

    async set_Teams(category = '') {
        let errmsg =
            'Invalid category, only "MASCULINO" or "FEMENINO" is accepted'
        if (!Array.isArray(this.Games)) {
            throw new Error('Games data not loaded properly')
        }

        if (category === 'MASCULINO' || category === 'FEMENINO') {
            let teams = [
                ...new Set(
                    this.Games.filter(
                        game => game.category === category
                    ).flatMap(game => game.teams)
                )
            ]
            if (category === 'MASCULINO') {
                this.MaleTeams = teams
            } else if (category === 'FEMENINO') {
                this.FemaleTeams = teams
            } else {
                throw new Error(errmsg)
            }
        } else if (category === '') {
            // Si no hay categoría, devuelve todos los equipos
            this.Teams = [...new Set(this.Games.flatMap(game => game.teams))]
        } else {
            throw new Error(errmsg)
        }
    }

    async compiled_data() {}

    set_Filtered(
        filters = {
            tournament: '',
            year: '',
            category: '',
            modality: '',
            team: ''
        }
    ) {
        let filtered = this.Games
        if (filters.tournament) {
            filtered = filtered.filter(
                game => game.tournament === filters.tournament
            )
        }
        if (filters.year) {
            filtered = filtered.filter(game => game.year === filters.year)
        }
        if (filters.category) {
            filtered = filtered.filter(
                game => game.category === filters.category
            )
        }
        if (filters.modality) {
            filtered = filtered.filter(
                game => game.modality === filters.modality
            )
        }

        this.Filtered = filtered
    }
    get_Filtered() {
        return this.Filtered
    }

    get_All_Data() {
        return {
            Tournaments: this.Tournaments,
            Years: this.Years,
            Categories: this.Categories,
            Modalities: this.Modalities,
            Teams: this.Teams,
            FemaleTeams: this.FemaleTeams,
            MaleTeams: this.MaleTeams
        }
    }

    get_Data(item = '') {
        let data = []
        if (item === '') {
            data = this.Data
        } else {
            data = this[item]
        }
        return data
    }

    get_Games() {
        return this.Games
    }

    get_Item(item) {
        return this[item]
    }

    get_Teams(category = '') {
        if (category === 'MASCULINO' || category === 'FEMENINO') {
            return category === 'MASCULINO' ? this.MaleTeams : this.FemaleTeams
        }
        return this.Teams
    }
}
