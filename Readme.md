# Modified Euler and Heun's Methods

A Python GUI application for solving first-order initial value problems using the **Modified Euler Method** and **Heun's Method**.

The program solves differential equations of the form:

\[
y' = f(x,y), \quad y(x_0)=y_0
\]

It allows the user to enter the differential equation, initial values, step size, final x-value, and optional exact solution. The results are displayed in a clear table showing the numerical solution, exact solution, and magnitude of error.

---

## Project Description

This project implements two numerical methods for solving ordinary differential equations:

1. **Modified Euler Method**
2. **Heun's Method**

Both methods are second-order numerical methods and are commonly used in numerical analysis to approximate solutions of initial value problems.

The application includes a simple graphical user interface built with **Tkinter**, making it easier for students to enter inputs and view results without using the command line.

---

## Numerical Methods Used

### 1. Modified Euler Method

The Modified Euler Method uses the slope at the midpoint of the interval.

Formula:

\[
k_1 = f(x_i, y_i)
\]

\[
k_2 = f\left(x_i + \frac{h}{2}, y_i + \frac{h}{2}k_1\right)
\]

\[
y_{i+1} = y_i + hk_2
\]

---

### 2. Heun's Method

Heun's Method first predicts the next value using Euler's method, then corrects it using the average of two slopes.

Formula:

\[
k_1 = f(x_i, y_i)
\]

\[
y^* = y_i + hk_1
\]

\[
k_2 = f(x_i+h, y^*)
\]

\[
y_{i+1} = y_i + \frac{h}{2}(k_1+k_2)
\]

---

## Features

- Graphical user interface using Tkinter
- Supports user-defined differential equations
- Supports optional exact solution
- Calculates numerical solution using:
  - Modified Euler Method
  - Heun's Method
- Displays:
  - Point
  - Numerical solution
  - Exact solution
  - Magnitude of error
- Handles mathematical functions such as:
  - `sin(x)`
  - `cos(x)`
  - `tan(x)`
  - `exp(x)`
  - `log(x)`
  - `sqrt(x)`
  - `e`
  - `pi`
- Supports both `**` and `^` for powers

---

## Requirements

This project uses only Python built-in libraries.

No external packages are required.

Required:

```bash
Python 3.x