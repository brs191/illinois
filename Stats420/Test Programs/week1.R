# Chapter 3 -- Data and Programming
print("my first R program")

x = c(1, 3, 5, 7, 9) # combine
x
x[-1] # exclude index 1
x[-2] # exclude index 2

# c(42, "Statistics", TRUE)
# 
# (y = 1:100)
# seq(from = 1, to = 100, by = 4)
# rep("RAJA", times = 5)

# Vectorization
x = 1:10
x = x*x
sqrt(x)

# Logical Operators -> same as others


# Matrices
x = 1:9
X = matrix(x, nrow = 3, ncol = 3)
X
X[2, c(1,3)] # why is it 8?

# Matrix Operations

x = 1:9
y = 9:1
X = matrix(x, nrow = 3, ncol = 3)
Y = matrix(y, nrow = 3, ncol = 3)
X
Y
X + Y
X * Y
diag(X*Y)

library(readr)
example_data_from_csv = read_csv("data/example-data.csv")