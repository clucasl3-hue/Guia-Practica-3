//Divisores de varios numeros
let numeros = [6, 10 ,15];
for (let i = 0; i < numeros.length; i++) {
    let n = numeros[i];
    let divisores = "";
for (let j = 1; j <= n; j++) {
if (n % j === 0) {
    if (divisores !== "") {
        divisores = divisores + ",";
    }
    divisores = divisores + j;
}
}
console.log(n + ":" + divisores);
}
