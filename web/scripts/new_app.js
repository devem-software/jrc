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

let data_games = data.games
let data_tournaments = data.tournaments
let data_years = data.years
let data_categories = data.categories
let data_modalities = data.modalities
let data_teams = data.teams
let data_femaleteams = data.femaleteams
let data_maleteams = data.maleteams

console.log(data_games, data_years)

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
    add_filter(data_years, ['TODO'], 'AÑOS', 'years', class_selector),
    add_filter(
        data_tournaments,
        ['TODO'],
        'COMPETENCIAS',
        'tournaments',
        class_selector
    ),
    add_filter(
        data_categories,
        ['TODO'],
        'CATEGORIAS',
        'categories',
        class_selector
    ),
    add_filter(
        data_modalities,
        ['TODO'],
        'MODALIDADES',
        'modalities',
        class_selector
    ),
    add_filter(
        data_teams,
        ['TODOS'],
        'TODOS LOS EQUIPOS',
        'teams',
        class_selector
    ),
    add_filter(
        data_maleteams,
        ['TODO'],
        'EQUIPOS MASCULINOS',
        'maleteams',
        class_selector
    ),
    add_filter(
        data_femaleteams,
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

let y2015 = utils.filterBy(data_games, 'year', 2015, data_years)

console.log(data_tournaments)
console.log(
    utils.getNames(data_tournaments, utils.getUniqueValues(y2015, 'tournament'))
)
console.log(utils.getUniqueValues(y2015, 'modality'))

const renderlinks = (container, data) => {
    data.forEach(el => {
        let table = ''
        let body = document.createElement('p')
        let link = document.createElement('div')

        let year = utils.getByValue(el.year, data_years)
        let category =
            utils.getByValue(el.category, data_categories) == 'F'
                ? 'FEM'
                : 'MAS'
        let tournament = utils.getByValue(el.tournament, data_tournaments)
        let modality = utils.getByValue(el.modality, data_modalities)
        let team_a = utils.getByValue(el.teams[0], data_teams)
        let team_b = utils.getByValue(el.teams[1], data_teams)

        table = `<div style="display:flex;margin-bottom:.5rem">`
        table += `<span style="width:2rem">${year}</span>`
        table += `<span style="width:1.75rem; text-align:center">${modality}'s</span>`
        table += `<span style="width:2.5rem; text-align:center">${category}</span>`
        table += `<span style="flex:1;text-align:right">${tournament}</span>`
        table += `</div>`
        table += `<div style="width: 100%;display:flex; justify-content:space-around; font-weight: bold">`
        table += `<span style="flex:1;">${team_a}</span>`
        table += `<span style="flex:0;width: 1.5rem; text-aling:center">${0}</span>`
        table += `<span style="width: 1rem;margin:0 .25rem; text-align:center">vs</span>`
        table += `<span style="flex:0;width: 1.5rem; text-aling:center">${0}</span>`
        table += `<span style="flex:1;text-align:right">${team_b}</span>`
        table += `</div>`

        body.classList.add('app__filters_results--result')
        link.classList.add('app__filters_results--result-link')
        link.id = `${el.videoId}`
        link.target = 'blank'
        link.innerHTML = table
        body.append(link)
        container.append(body)
    })
}

renderlinks(results, data_games)
