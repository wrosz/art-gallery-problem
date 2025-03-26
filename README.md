# Art Gallery Problem  

## Description  
The **Art Gallery Problem** is a mathematical problem that involves finding the minimum number of guards needed to observe an art gallery, which is represented as a simple polygon without holes. This project is a desktop application built with **Pygame**, where the user can draw a polygon (or load data from a file), and the application displays an approximate solution. The solution is found through **triangulation** of the given polygon and **three-coloring** of its vertices, corresponding to its graph representation.  

## Project Structure  
- The **source code** is located in the `agp.project` folder.  
- To run the application, execute the `main.py` file.  
- The `pliki_zrodlowe` folder contains helper scripts, such as function definitions for solving the problem and application window configuration (see comments in the code for details).  
- The application generates **visualizations** of the solutions in the `pliki_wielokat` folder.  
- The file `wspolrzedne_punktow.csv` stores the coordinates of the user-defined polygon.  

## Requirements  
This project requires **Python 3.x** and the following libraries:  
- `pygame`  
- `csv`  
- `tripy`  
- `matplotlib`  
- `numpy`  
- `tkinter`  
- `itertools`  
- `re`  

You can install the required libraries using:  
```bash
pip install pygame tripy matplotlib numpy
```
(`csv`, `tkinter`, `itertools`, and `re` are built into Python and do not require installation.)  

## Usage  
1. Run `main.py`.  
2. Draw a polygon or load one from a file.  
3. The application will compute and visualize an approximate solution.  
