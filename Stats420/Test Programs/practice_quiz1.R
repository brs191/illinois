#Practice Quiz 1

x = 1:100
sum(log(x))


set.seed(42)
a_vector = rpois(250, lambda = 6)
sum(a_vector > 5)


x = 1:100
y = x
for(i in x) {
  ifelse(i%%2, {y[i] = y[i] + 5}, {y[i] = y[i]-10})
}
sd(y)

library(MASS, lib.loc = "/usr/lib/R/library")
melo = MASS::Melanoma
hist(melo$age)
