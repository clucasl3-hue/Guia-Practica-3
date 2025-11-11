//Calcular la suma total de los divisores positivos de un numero
let n = 12
let sumadivisores = 0
for (let i = 1; i <= n; i++) {
    if (n % i === 0) {
        sumadivisores = sumadivisores + i;
}
}
console.log("Suma de divisores de " + n + " = " + sumadivisores);
