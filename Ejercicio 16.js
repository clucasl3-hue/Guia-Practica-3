//Invertir varios numeros
let numeros = [123, 456, 780];
for (let i = 0; i < numeros.length; i++){
    let n = numeros[i];
    let invertido = 0;
while (n > 0) {
    let digito = n % 10;
    invertido = invertido * 10 + digito;
    n = Math.floor(n/10);
}
console.log(numeros[i] + ":" + invertido);
}
