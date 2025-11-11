//Restas sucesivas en una lista
let numeros = [15, 22, 30]
let valor = 4
for (let i = 0; i < numeros.length; i++) {
    let n = numeros[i];
for (let j = 0; n >= valor; j++) {
    n = n - valor;
}
console.log(numeros[i] + ":" + n);
}
