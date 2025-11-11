//Invertir los digitos de un numero
let n = 1234 
let invertido = 0
while (n > 0) {
    let digito = n % 10;
    invertido = invertido * 10 + digito;
    n = Math.floor(n / 10);
}
console.log("Numeros invertidos: " + invertido);
