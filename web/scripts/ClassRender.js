export default class ClassRender {
    constructor() {}
    selector(
        options = {
            data: [],
            data_optional: [],
            label_text: '',
            id: '',
            styles: ''
        }
    ) {
        const fieldset = document.createElement('fieldset')
        const label = document.createElement('label')
        const select = document.createElement('select')

        fieldset.id = `selector_${options.id}`
        fieldset.className = options.styles
        label.htmlFor = options.id
        label.textContent = options.label_text
        select.id = options.id

        const add_options = data => {
            data.sort().forEach(opt => {
                const option = document.createElement('option')
                option.value = opt.toString().toLowerCase()
                option.text = opt.toString().toUpperCase()
                select.append(option)
            })
        }

        if (options.data_optional.length > 0) add_options(options.data_optional)
        add_options(options.data)

        fieldset.append(label)
        fieldset.append(select)

        return fieldset
    }
}
