import ClassDataGames from './ClassDataGames.js'
import ClassRender from './ClassRender.js'
import ClassUtils from './ClassUtils.js'

const dg = new ClassDataGames()
const render = new ClassRender()
const utils = new ClassUtils()

// dg.set_path('../data/partidos.json')
await dg.set_path(
    'https://raw.githubusercontent.com/devem-software/jrc/refs/heads/main/data/optimized_partidos.json'
)
await dg.load_data()

const data = await dg.get_compiled_data()
const games = data.games
const tournaments = data.tournaments
const years = data.years
const categories = data.categories
const modalities = data.modalities
const teams = data.teams
const femaleteams = dg.femaleteams
const maleteams = dg.maleteams
const filters = document.querySelector('.app__filters_controls')

const add_filter = async (data, data_optional, label_text, id, styles) => {
    data = await Object.keys(data)
    filters.append(
        render.selector({
            data,
            data_optional,
            label_text,
            id,
            styles
        })
    )
}

const class_selector = 'app__filters_controls--control'

add_filter(years, ['TODOS'], 'AÑOS', 'years', class_selector)

add_filter(
    tournaments,
    ['TODOS'],
    'COMPETENCIAS',
    'tournaments',
    class_selector
)

add_filter(categories, ['TODAS'], 'CATEGORIAS', 'categories', class_selector)

add_filter(modalities, ['TODAS'], 'MODALIDADES', 'modalities', class_selector)

add_filter(teams, ['TODOS'], 'EQUIPOS', 'teams', class_selector)

add_filter(
    maleteams,
    ['TODOS'],
    'EQUIPOS MASCULINOS',
    'maleteams',
    class_selector
)

add_filter(
    femaleteams,
    ['TODOS'],
    'EQUIPOS FEMENINOS',
    'femaleteams',
    class_selector
)
