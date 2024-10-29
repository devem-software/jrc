export default class RenderClass {
  constructor() {}
  select(data, label = '', id = '', styles = '') {
    let fst = document.createElement('fieldset')
    let lbl = (document.createElement('label').text = label)
    let sel = document.createElement('select')

    fst.id = `select_${id}`
    sel.setAttribute('id', id)

    data.forEach(el => {
      let opt = document.createElement('option')
      opt.value = el.toLowerCase()
      opt.text = el
      sel.append(opt)
    })

    fst.append(lbl)
    fst.append(sel)

    return fst
  }
}
