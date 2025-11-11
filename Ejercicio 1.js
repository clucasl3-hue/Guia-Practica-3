//Los primeros n terminos, donde cada termino se obtiene sumando los dos anteriores
let n = 8
let c = 0
let k = 1
console.log(c);
console.log(k);
for (let i= 2; i < n; i++) {
    let a = c + k;
    console.log(a);
    c = k
    k = a
}
