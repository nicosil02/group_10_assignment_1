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

First, import NumPy:
```python
import numpy as np
```
Then:
- Create an array containing the numbers from 1 to 10.
- Print the array.
- Display its maximum and minimum values.
- Create an array of 5 zeros.
- Create an array of 5 ones.
- Create the following matrix:
```python
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
```
- Display the matrix.
- Use `.shape` to display its dimensions.
