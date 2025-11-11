// Suma de divisores de varios números
let numeros = [6, 12, 28];

for (let i = 0; i < numeros.length; i++) {
  let n = numeros[i];
  let suma = 0;

  for (let j = 1; j <= n; j++) {
    if (n % j === 0) {
      suma = suma + j;
    }
  }

  console.log(n + ":" + suma);
}
