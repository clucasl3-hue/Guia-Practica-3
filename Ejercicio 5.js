//Un numero primo solo tiene dos divisores:1 y el mismo
let numeros = [11, 12]
for (let i = 0; i < numeros.length; i++) {
    let n = numeros[i];
    let esPrimo = true;
    if (n <= 1) {
        esPrimo = false;
    } else {
        for (let j = 2; j < n; j++) {
            if (n % j === 0) {
                esPrimo = false;
                break;
            }
        }
    }
    if (esPrimo) {
        console.log(n + " es un numero primo.");
    } else {
        console.log(n + " no es un numero primo.");
    }
}
