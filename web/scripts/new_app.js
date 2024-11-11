import ClassDataGames from './ClassDataGames.js'
import ClassRender from './ClassRender.js'
import ClassUtils from './ClassUtils.js'

const dg = new ClassDataGames()
const render = new ClassRender()
const utils = new ClassUtils()

const $ = el => document.querySelector(el)

const localpath = '../data/optimized_partidos.json'
const remotepath =
    'https://raw.githubusercontent.com/devem-software/jrc/refs/heads/main/data/optimized_partidos.json' // dg.set_path('../data/partidos.json')

await dg.set_path(remotepath)
await dg.load_data()

const data = await dg.get_compiled_data()
console.log(data)
console.log(dg.get_years())
const {
    games,
    tournaments,
    years,
    categories,
    modalities,
    teams,
    femaleteams,
    maleteams
} = data
const filters = $('.app__filters_controls')
const results = $('.app__filters_results')

const add_filter = async (data, data_optional, label_text, id, styles) => {
    filters.append(
        render.selector({
            data: Object.keys(data),
            data_optional: data_optional,
            label_text: label_text,
            id: id,
            styles: styles
        })
    )
}

const class_selector = 'app__filters_controls--control'

await Promise.all([
    add_filter(years, ['TODO'], 'AÑOS', 'years', class_selector),
    add_filter(
        tournaments,
        ['TODO'],
        'COMPETENCIAS',
        'tournaments',
        class_selector
    ),
    add_filter(
        categories,
        ['TODO'],
        'CATEGORIAS',
        'categories',
        class_selector
    ),
    add_filter(
        modalities,
        ['TODO'],
        'MODALIDADES',
        'modalities',
        class_selector
    ),
    add_filter(teams, ['TODOS'], 'TODOS LOS EQUIPOS', 'teams', class_selector),
    add_filter(
        maleteams,
        ['TODO'],
        'EQUIPOS MASCULINOS',
        'maleteams',
        class_selector
    ),
    add_filter(
        femaleteams,
        ['TODO'],
        'EQUIPOS FEMENINOS',
        'femaleteams',
        class_selector
    )
])

let selector_categories = $('#selector_categories')
let selector_teams = $('#selector_teams')
let selector_maleteams = $('#selector_maleteams')
let selector_femaleteams = $('#selector_femaleteams')

selector_femaleteams ? selector_femaleteams.remove() : undefined
selector_maleteams ? selector_maleteams.remove() : undefined

selector_categories.addEventListener('change', e => {
    let val = e.target.value

    selector_teams ? selector_teams.remove() : undefined
    selector_femaleteams ? selector_femaleteams.remove() : undefined
    selector_maleteams ? selector_maleteams.remove() : undefined

    let selector =
        val === 'todas' ? 'teams' : val === 'f' ? 'femaleteams' : 'maleteams'

    console.log(val, selector)

    filters.append(eval(`selector_${selector}`))
})

games.forEach(el => {
    let container = document.createElement('p')
    let link = document.createElement('a')
    
    container.classList.add('app__filters_results--result')
    link.classList.add('app__filters_results--result-link')
    link.href = `https://www.youtube.com/watch?v=${el.videoId}`
    link.target = 'blank'
    link.innerHTML = `[${utils.getByValue(el.year, years)}] (${utils.getByValue(
        el.category,
        categories
    )} - ${utils.getByValue(el.modality, modalities)}'s) \t ${utils.getByValue(
        el.teams[0],
        teams
    )} vs ${utils.getByValue(el.teams[1], teams)}`
    container.append(link)
    results.append(container)
})
