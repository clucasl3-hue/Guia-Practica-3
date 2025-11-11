//Mostrar todos los numeros que dividen exactamente el numero ingresado
let n = 12
console.log("Divisores de " + n + ":");
for (let i = 1; i <= n; i++) {
    if (n % i === 0) {
    console.log(i);
}
}
