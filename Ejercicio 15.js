//Numeros primos en una lista
let numeros = [5, 6, 7, 8, 11];
let primos = "";
for (let i = 0; i < numeros.length; i++) {
    let n = numeros[i];
    let esPrimo = true;
    if (n < 2) {
        esPrimo = false
    } else {
        for (let j = 2; j < n; j++) {
            if (n % j === 0) {
                esPrimo = false;
                break;
            }
        }
    }
    if (esPrimo) {
        if (primos !== "") {
            primos = primos + ",";
        }
        primos = primos + n;
    }
}
console.log("Primos:" + primos);
