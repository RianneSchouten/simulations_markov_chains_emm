# In this document we create an overview of the relation between the simulation conditions,
# the number of parameters and the dataset size,
# for our paper: Exceptional transition behaviour of varying order.

library(tidyverse)
library(readxl)

n <- 100
t <- c(10, 50, 200)
s <- c(2, 5, 10)
o <- c(1,2,3,4)

d <- data.frame(matrix(NA, ncol=6))
g <- 1
for(i in 1:3){
  for(j in 1:3){
    for(h in 1:4){
      d[g,] <- c(t[i], s[j], o[h], s[j]^o[h]*(s[j]-1), s[j]*(s[j]-1), n*t[i])
      g = g + 1
    }
  }
}
names(d) <- c('T', 'S', 'O', 'K', 'G', 'N')
d <- d %>% mutate('NK' = N / K) %>%
  mutate('Feasible' = NK > 1) %>%
  mutate('AIC' = NK > 40) %>%
  mutate(pAICcSG = (2*K^2 + 2*K) / (N - K - 1)) %>%
  mutate(pAICcD = (2*G^2 + 2*G) / (N - G - 1)) %>%
  mutate(difSGD = pAICcSG - pAICcD)

d

# check found subgroup order
setwd("C:/Users/20200059/Documents/Github/simulations_beam_search_markov_chain/figures/")
data_11 <- read_excel("../data_output/results_manuscript/experiment_higherorders_20210115_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
length_new_column = 6 * 4 * 10 * 1 * 3 * 3 * 3
long_data_11 <- data_11 %>%
  pivot_longer(
    cols = names(data_11)[9:dim(data_11)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order', 'found_order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))
sel_long_data_11 <- long_data_11[long_data_11$type != 'found_order', ]

data <- long_data_11
sel_data <- data %>% filter(type == 'found_order') %>% 
  filter(measure == 'phiaic') %>%
  filter(T == 50) %>% filter(S == 10) %>%
  filter(ncovs == 20)

