export default class ClassUtils {
    arrayToObject(array) {
        return Object.fromEntries(array.map((k, v) => [k, v]))
    }

    returnKeyFor(val, json) {
        for (let key in json) {
            if (json[key] === val) {
                return key
            }
        }
        return null
    }

    getNames(set, array) {
        // Invertimos el objeto teams para que las claves sean los valores y viceversa
        const idToName = Object.fromEntries(
            Object.entries(array).map(([name, id]) => [id, name])
        )

        console.log(idToName)

        // Recorremos el Set y construimos el objeto resultante
        const result = {}
        set.forEach(id => {
            if (idToName[id]) {
                result[idToName[id]] = id
            }
        })

        return result
    }
    getByValue(id, array) {
        const result = Object.keys(array).find(result => array[result] === id)
        return result || 'Dato no encontrado'
    }
    filterBy(data, item, value, json) {
        return data.filter(el => el[item] === json[value])
    }
    getUniqueValues(data, item) {
        return Array.from(new Set(data.map(el => el[item])))
    }
}
