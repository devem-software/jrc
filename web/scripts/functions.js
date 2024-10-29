const $ = el => document.querySelector(el)
const createEl = el => document.createElement(el)

const data_flating = (array, items) =>
  [...new Set(array.map(data => data[items]))].sort()

const data_filter_flat = (array, items, filter, compare) => [
  ...new Set(
    array
      .filter(data => data[filter] === compare)
      .flatMap(data => data[items].flat())
  )
]

const gen_options = (label, id, data) => {
  let fieldset = createEl('fieldset')
  fieldset.id = `select_${id}`
  let title = (createEl('label').text = label)
  let select = createEl('select')
  select.setAttribute('id', id)
  console.log(data)
  data.forEach(el => {
    let opt = createEl('option')
    opt.value = el.toLowerCase()
    opt.text = el
    select.append(opt)
  })
  fieldset.append(title)
  fieldset.append(select)
  return fieldset
}

const get_data_from_json = async path => {
  return await fetch(path)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error al cargar el archivo ${path}`)
      }
      return response.json()
    })
    .then(data => {
      return data
    })
    .catch(error => console.error('Error: ', error))
}

// Exportando las funciones
export {
  $,
  createEl,
  data_flating,
  data_filter_flat,
  gen_options,
  get_data_from_json
}
