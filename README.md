# Assignment 1 - Group 10

## Team Members

| Name                | GitHub                                      |
|---------------------|----------------------------------------------|
| Nicolas Silva        | [@nicosil02](https://github.com/nicosil02)   |
| Marco Virú           | [@marcovirulucas](https://github.com/marcovirulucas)     |
| Estefanny Mejía      | [@estefmej](https://github.com/estefmej)     |
| Luz Supo             | [@lsupo](https://github.com/lsupo)     |

##  Repository Structure

```
assignment_1/
│
├── lists.ipynb
├── tuples.ipynb
├── dictionaries.ipynb
└── numpy.ipynb
```


## Assignment Instructions

### Part 1 – Lists (`lists.ipynb`)

Create a list with the following grades:
```python
grades = [15, 18, 12, 20, 16]
```
Using this list:
- Print the original list.
- Add the grade 17 using `append()`.
- Sort the grades from lowest to highest using `sort()`.
- Display: the highest grade, the lowest grade, and the total number of grades.
- Print the final list.

### Part 2 – Tuples (`tuples.ipynb`)

Create the following tuple:
```python
ages = (20, 25, 22, 30, 28)
```
Using this tuple:
- Print the tuple.
- Display the first and last elements.
- Display: the maximum value, the minimum value, and the number of elements.
- Try to modify one of the elements of the tuple.
- Write a brief comment in the script explaining why Python does not allow this modification.

### Part 3 – Dictionaries (`dictionaries.ipynb`)

Create a dictionary containing the population of the following cities:
```python
population = {
    "Lima": 10092000,
    "Arequipa": 1008000,
    "Trujillo": 919000
}
```
Then:
- Print the complete dictionary.
- Display only its keys using `keys()`.
- Get the population of `"Lima"` using `get()`.
- Add `"Cusco": 428000` to the dictionary.
- Remove `"Trujillo"` using `pop()`.
- Print the final dictionary.

### Part 4 – NumPy (`numpy.ipynb`)

# Importar NumPy
import numpy as np

# 1. Crear un array con los números del 1 al 10
array_numeros = np.arange(1, 10)
print("1. Array con números del 1 al 10:")
print(array_numeros)

# 2. Imprimir la matriz / array
print("\n2. Array:")
print(array_numeros)

# 3. Mostrar el valor máximo y mínimo
valor_maximo = np.max(array_numeros)
valor_minimo = np.min(array_numeros)
print("\n3. Valor máximo:")
print(valor_maximo)
print("Valor mínimo:")
print(valor_minimo)

# 4. Crear un array de 5 ceros
array_ceros = np.zeros(5)
print("\n4. Array de 5 ceros:")
print(array_ceros)

# 5. Crear un array de 5 unos
array_unos = np.ones(5)
print("\n5. Array de 5 unos:")
print(array_unos)

# 6. Crear la matriz
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
print("\n6. Matriz:")
print(matrix)

# 7. Mostrar la matriz
print("\n7. Matriz:")
print(matrix)

# 8. Mostrar las dimensiones de la matriz
print("\n8. Dimensiones de la matriz:")
print(matrix.shape)
