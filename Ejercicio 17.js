//Contar digitos de varios numeros
let numeros = [45, 678, 12345];
for (let i = 0; i < numeros.length; i++) {
    let n = numeros[i];
    let contador = 0;
while ( n > 0) {
    n = Math.floor(n/10);
    contador = contador + 1;
}
console.log(numeros[i] + ":" + contador + "digitos");
}
