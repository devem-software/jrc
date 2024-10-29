'use strict'

import { gen_options } from './functions.js'

import DataGamesClass from './data.js'
import RenderClass from './render.js'

const Render = new RenderClass()
const DataGames = new DataGamesClass()

await DataGames.init()
const data = DataGames.get_Games()

let ifilters = {
    tournament: '',
    year: '',
    category: '',
    modality: '',
    team: ''
}
DataGames.set_Filtered(ifilters)
console.log(DataGames.get_Filtered())

var filters = document.querySelector('.app__filters_controls')
let results = document.querySelector('.app__filters_results')

// var GAMES_FILTERED = GAMES;

// const TEAMS = [
//   ...new Set(GAMES_FILTERED.flatMap((game) => game.teams.flat())),
// ].sort();

// const femaleTeams = data_filter_flat(
//   GAMES_FILTERED,
//   "teams",
//   "category",
//   "FEMENINO"
// );
// const maleTeams = data_filter_flat(
//   GAMES_FILTERED,
//   "teams",
//   "category",
//   "MASCULINO"
// );

// const render = (data) => {

var select_Teams, select_FemaleTeams, select_MaleTeams

const render = data => {
    console.log(data)
    let tournaments = data.Tournaments
    let years = data.Years
    let categories = data.Categories
    let modalities = data.Modalities
    let teams = data.Teams
    let femaleTeams = data.FemaleTeams
    let maleTeams = data.MaleTeams

    tournaments.unshift('TODAS')
    years.unshift('TODAS')
    categories.unshift('TODAS')
    modalities.unshift('TODAS')
    teams.unshift('TODOS LOS EQUIPOS')
    femaleTeams.unshift('EQUIPOS FEMENINOS')
    maleTeams.unshift('EQUIPOS MASCULINOS')

    filters.innerHTML = ''
    filters.append(
        gen_options(
            'COMPETENCIA',
            'tournaments',
            DataGames.get_Data('Tournaments')
        )
    )
    filters.append(gen_options('AÑO', 'years', DataGames.get_Data('Years')))
    filters.append(
        gen_options('CATEGORIA', 'categories', DataGames.get_Data('Categories'))
    )
    filters.append(
        gen_options('MODALIDAD', 'modalities', DataGames.get_Data('Modalities'))
    )

    select_Teams = gen_options('EQUIPOS', 'Teams', DataGames.get_Data('Teams'))
    select_FemaleTeams = gen_options(
        'EQUIPOS',
        'FemaleTeams',
        DataGames.get_Data('FemaleTeams')
    )
    select_MaleTeams = gen_options(
        'EQUIPOS',
        'FaleTeams',
        DataGames.get_Data('MaleTeams')
    )

    filters.append(select_Teams)
}

render(DataGames.get_All_Data())

document.querySelector('#categories').addEventListener('change', e => {
    let val = e.target.value
    let t = document.getElementById('select_Teams')
    let ft = document.getElementById('select_FemaleTeams')
    let mt = document.getElementById('select_MaleTeams')

    t ? t.remove() : undefined
    ft ? ft.remove() : undefined
    mt ? mt.remove() : undefined

    let selector =
        val === 'TODAS'
            ? 'Teams'
            : val === 'femenino'
            ? 'FemaleTeams'
            : val === 'masculino'
            ? 'MaleTeams'
            : ''

    filters.append(eval(`select_${selector}`))

    let filtered = DataGames.get_Filtered()
    render(filtered)
})

// const data_filtered = (arr, item, compare) => {
//   return arr.filter((el) => el[item] === compare);
// };

// document.querySelector("#tournaments").addEventListener("input", (e) => {
//   let val = e.target.value.toUpperCase();
//   console.log(val.toUpperCase());

//   // GAMES_FILTERED = data_filtered(GAMES_FILTERED, "tournament", val);
//   // console.log(GAMES_FILTERED);
//   let DATA_FILTERED = DATA_FILTERING(data_filtered(GAMES, "tournament", val));
//   console.log(DATA_FILTERED.TEAMS);
//   render(DATA_FILTERED);
// });

// document.querySelector("#years").addEventListener("input", (e) => {
//   let val = e.target.value.toUpperCase();
//   console.log(val.toUpperCase());

//   let DATA_FILTERED = DATA_FILTERING(data_filtered(GAMES, "tournament", val));
//   console.log(DATA_FILTERED.TEAMS);
//   render(DATA_FILTERED);
// });
