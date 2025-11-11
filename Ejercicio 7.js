//Determinar cuantos digitos tiene un numero entero
let n = 9876
let contador = 0
while (n > 0) {
    n = Math.floor(n / 10);
    contador = contador + 1;
}
console.log("Cantidad de digitos: " + contador); 
