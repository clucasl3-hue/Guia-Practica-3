//Factorial de varios numeros
let numeros = [3, 4, 5]
for (let i = 0; i < numeros.length; i++) {
    let n = numeros[i]
    let factorial = 1
for (let j = 1; j <= n; j++) {
    factorial = factorial * j;
}
console.log(n + "! =" + factorial);
}
