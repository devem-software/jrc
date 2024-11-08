import ClassDataGames from './ClassDataGames.js'
import ClassRender from './ClassRender.js'

const dg = new ClassDataGames()
const render = new ClassRender()

// dg.set_path('../data/partidos.json')
await dg.set_path(
    'https://raw.githubusercontent.com/devem-software/jrc/refs/heads/main/data/optimized_partidos.json'
)
await dg.load_data()

const data = await dg.get_compiled_data()
// const games = data.games
// const tournaments = data.tournaments
// const years = data.years
// const categories = data.categories
// const modalities = data.modalities
// const teams = data.teams
// const femaleteams = data.femaleteams
// const maleteams = data.maleteams
const {games, tournaments, years, categories, modalities, teams, femaleteams,maleteams} = data
const filters = document.querySelector('.app__filters_controls')

const add_filter = async (data, data_optional, label_text, id, styles) => {
  console.log(data)
//     data = await Object.keys(data)
//     console.log(data)
    filters.append(
        render.selector({
            "data":Object.keys(data),
            "data_optional":data_optional,
            "label_text":label_text,
            "id":id,
            "styles":styles
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
