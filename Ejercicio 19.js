//Sumas sucesivas en una lista
let numeros = [2, 3, 4]
let veces = 4
for (let i = 0; i < numeros.length; i++) {
    let n = numeros[i];
    let resultado = 0;
for (let j = 0; j < veces; j++) {
    resultado = resultado + n;
}
console.log(n + "x" + veces + "=" + resultado);
}
