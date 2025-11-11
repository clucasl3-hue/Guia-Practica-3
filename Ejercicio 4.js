//Un numero es perfecto si la suma de sus divisores (sin incluir el mismo) es igual al numero
let n = 6
let sumadivisores = 0
for (let i = 1; i < n; i++) {
    if (n % i === 0) {
        sumadivisores = sumadivisores + i;
    }
}
if (sumadivisores === n) {
    console.log(n + " es nu numero perfecto.");
} else {
    console.log(n + "no es numero perfecto.");
}
