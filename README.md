# container-problem
Comparison between the top-down, bottom-up and brute-force algorithms for the container problem

## Installation

Download the GitHub repository via SSH or HTTPS

```bash
$ git clone URL
````

Define a virtual environment

```bash
$ python3 -m venv .venv
```

Activate the virtual environment for further dependencies.

```bash
$ source .venv/bin/activate
```

Make sure pip is installed on your computer, check the [pip official documentation](https://pip.pypa.io/en/stable/installation/)
if it isn't.

```bash
(.venv) $ pip3 install -r requirements.txt
```

## Run

```bash
(.venv) $ ./contenedor.py [-h] algorithm -a file.txt iterations
```

Or with a random generated problem...

```bash
(.venv) $ ./contenedor.py [-h] algorithm -p capacity N weights benefits iterations
```

### Arguments

#### Algorithm

Desired algorithm to solve the problem.
```     
1 = Brute force algorithm
2 = Bottom up algorithm
3 = Top Down using memoization algorithms
4 = Compare/Run all algorithms
```        
#### File 

Text file with the container problem in the correct format
#### Capacity

Max weight of the container
#### N
Number of items
#### Weight ranges
Generate a random weight list between those values
#### Benefit ranges
Generate a random benefit list between those values
#### Iterations
Number of times the algorithm should be run

---
## Authors

* María Barquero **@mariabarquero**
* Joseph Valenciano **@JosephV27**
* Wilhelm Carstens **@wolam**
