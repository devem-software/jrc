export default class ClassUtils {
  returnKeyFor(val, json) {
    for (let key in json) {
        if (json[key] === val) {
            return key;
        }
    }
    return null;
}
}