//Let numeros perfectos en una lista
let numeros = [6,10,28,30];
let perfectos = "";
for (let i = 0; i < numeros.length; i++){
    let n = numeros[i];
    let sumadivisores = 0;
for (let j = 1; j < n; j++) {
    if (n % j === 0) {
        sumadivisores = sumadivisores + j;
    }
}

if (sumadivisores === n) {
    if (perfectos !== "") {
        perfectos = perfectos + ",";
    }
    perfectos = perfectos + n;
}
}
console.log("Numeros perfectos: " + perfectos);
