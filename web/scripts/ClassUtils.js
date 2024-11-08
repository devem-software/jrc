export default class ClassUtils {
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
}
