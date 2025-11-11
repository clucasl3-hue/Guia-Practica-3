//Serie de fibonacci para varios terminos 
let valores = [5, 8, 10];
for (let i = 0; i < valores.length; i++) {
let n = valores[i];
let a = 0;
let b = 1;
console.log("Es (" + n + "):"); 

console.log(a);
console.log(b);

for (let j = 2; j < n; j++) {
let suma = a + b;
console.log(suma);
a = b;
b = suma; 
}
console.log("------------");
}
