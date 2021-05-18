library(ggplot2)
library(readxl)
library(tidyverse)
library(RColorBrewer)
library(mice)
library(xtable)

setwd("C:/Users/20200059/Documents/Github/simulations_beam_search_markov_chain/figures/")

#### Simulation results and figures for revised manuscript May 2021 ####

data_phiwd <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201125_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
data_rest <- read_excel("../data_output/results_manuscript/experiment_higherorders_20210107_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
data_omegatv_phiwrl <- read_excel("../data_output/results_manuscript/experiment_higherorders_20210128_30nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")

data_09 <- read_excel("../data_output/results_manuscript/experiment_higherorders_20210109_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
data_10 <- read_excel("../data_output/results_manuscript/experiment_higherorders_20210110_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
data_11 <- read_excel("../data_output/results_manuscript/experiment_higherorders_20210115_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")

total_reps = 10 + 10 + 10 + 10

length_new_column = 1 * 4 * 10 * 1 * 3 * 3 * 3
long_data_phiwd <- data_phiwd %>%
  pivot_longer(
    cols = names(data_phiwd)[9:dim(data_phiwd)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

length_new_column = 2 * 4 * 30 * 1 * 3 * 3 * 3
long_data_phiwrl_omegatv <- data_omegatv_phiwrl %>%
  pivot_longer(
    cols = names(data_omegatv_phiwrl)[9:dim(data_omegatv_phiwrl)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order', 'found_order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))
sel_long_data_phiwrl_omegatv <- long_data_phiwrl_omegatv[long_data_phiwrl_omegatv$type != 'found_order', ]

length_new_column = 3 * 4 * 10 * 1 * 3 * 3 * 3
long_data_rest <- data_rest %>%
  pivot_longer(
    cols = names(data_rest)[9:dim(data_rest)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

length_new_column = 6 * 4 * 10 * 1 * 3 * 3 * 3
long_data_09 <- data_09 %>%
  pivot_longer(
    cols = names(data_09)[9:dim(data_09)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))
sel_long_data_09 <- long_data_09[(long_data_09$measure != 'phiwrl') & (long_data_09$measure != 'omegatv'), ]

long_data_10 <- data_10 %>%
  pivot_longer(
    cols = names(data_10)[9:dim(data_10)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))
sel_long_data_10 <- long_data_10[(long_data_10$measure != 'phiwrl') & (long_data_10$measure != 'omegatv'), ]

length_new_column = 6 * 4 * 10 * 1 * 3 * 3 * 3
long_data_11 <- data_11 %>%
  pivot_longer(
    cols = names(data_11)[9:dim(data_11)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order', 'found_order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))
sel_long_data_11 <- long_data_11[long_data_11$type != 'found_order', ]

# calculate number of times found dataset order = 1
sum(long_data_11[(long_data_11$type == 'found_order') &
                   (long_data_11$value == 1), 'value'])
nrow(long_data_11[long_data_11$type == 'found_order', 'value'])

long_data <- rbind(long_data_phiwd, long_data_rest,
                   sel_long_data_phiwrl_omegatv,
                   sel_long_data_09, sel_long_data_10, 
                   sel_long_data_11) %>%
  arrange(nreps, as.integer(N), as.integer(T), as.integer(S), 
          as.integer(ncovs), as.integer(subgroup_orders)) %>%
  mutate(true_subgroup_order = as.factor(subgroup_orders)) %>%
  mutate(states = ordered(factor(S), 
                          levels = as.character(sort(as.integer(unique(S)))))) %>%
  mutate(timepoints = ordered(factor(T), 
                              levels = as.character(sort(as.integer(unique(T)))))) %>%
  mutate(ncovs = ordered(factor(ncovs), 
                         levels = as.character(sort(as.integer(unique(ncovs)))))) %>%
  mutate(N = ordered(factor(N), 
                     levels = as.character(sort(as.integer(unique(N)))))) %>%
  mutate(measure = ordered(factor(measure), 
                           levels = c('phibic', 'phiaic', 'phiaicc', 'phiwd', 'omegatv', 'phiwrl')))

# two figures
plot_data <- long_data %>%
  filter(N == 100) %>%
  filter(ncovs == 20)

ranks <- plot_data %>% 
  filter(type == 'rank') %>%
  filter(measure != 'phibic') %>%
  filter(measure != 'phiaicc') %>%
  mutate(measure = recode(measure, phiaic = "phibic, phiaic, phiaicc")) %>%
  ggplot(aes(y = value, x = true_subgroup_order)) +
  geom_boxplot(aes(fill = states), outlier.shape = NA) + 
  facet_grid(measure ~ timepoints, labeller = label_both) + 
  labs(title = paste('Boxplots of the rank of the true subgroup in the top-20', 
                     sep = " ", collapse = NULL),
       fill = 'states') + 
  xlab('True subgroup order') + 
  ylab('Rank') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank()) + 
  scale_fill_manual(values=c("#deebf7", "#9ecae1", "#3182bd"))

ranks

name <- paste('../figures/Figures_revised_manuscript/ranks_20ncovs.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 24, units = "cm")

plot_data <- long_data %>%
  filter(N == 100) %>%
  filter(ncovs == 20) %>%
  filter(type == 'order') %>%
  group_by(N, measure, true_subgroup_order, timepoints, states, ncovs) %>%
  summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / total_reps)

orders <- plot_data %>%
  ggplot(aes(x = true_subgroup_order, y = perc_true_order, fill = states)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black") + 
  facet_grid(measure ~ timepoints, labeller = label_both) + 
  labs(title = paste('Percentage of nreps where the true subgroup order is found', 
                     sep = " ", collapse = NULL)) +
  xlab('True subgroup order') + 
  ylab('Percentage') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank()) + 
  scale_fill_manual(values=c("#deebf7", "#9ecae1", "#3182bd")) 

orders

name <- paste('../figures/Figures_revised_manuscript/orders_20ncovs.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 30, units = "cm")

#### Subgroups with exceptional starting behaviour ####

data_12 <- read_excel("../data_output/results_manuscript/experiment_zero_order_subgroups_20210112_10nreps_[100, 500, 1000]_[10, 5, 2]_[10, 5, 2]_[20, 10, 5].xlsx")

# name is too long, but we have to load this dataset
#data_15 <- read_excel("../data_output/results_revised_manuscript/experiment_initial_starting_behaviour_20210515_[10, [1000, 500, 100], [20, 10, 5], [10, 5, 2], [10, 5, 2], [0.5], [2], [1]].xlsx")
data_15 <- read_excel("../data_output/results_revised_manuscript/experiment_initial_starting_behaviour_20210515.xlsx")

length_new_column <- 6 * 1 * 10 * 3 * 3 * 3 * 3
data_12 <- data_12 %>%
  pivot_longer(
    cols = names(data_12)[9:dim(data_12)[2]], 
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order', 'found_order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure)) %>%
  select(-c(refs))

data_15 <- data_15 %>%
  pivot_longer(
    cols = names(data_15)[12:dim(data_15)[2]], 
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order', 'found_order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure)) %>%
  select(-c(true_desc_length, global_model_order, start_at_order, p))

long_data <- rbind(data_12, data_15) %>%
  arrange(nreps, as.integer(N), as.integer(T), as.integer(S), 
          as.integer(ncovs), as.integer(subgroup_orders)) %>%
  mutate(true_subgroup_order = as.factor(subgroup_orders)) %>%
  mutate(states = ordered(factor(S), 
                          levels = as.character(sort(as.integer(unique(S)))))) %>%
  mutate(timepoints = ordered(factor(T), 
                              levels = as.character(sort(as.integer(unique(T)))))) %>%
  mutate(ncovs = ordered(factor(ncovs), 
                         levels = as.character(sort(as.integer(unique(ncovs)))))) %>%
  mutate(N = ordered(factor(N), 
                     levels = as.character(sort(as.integer(unique(N)))))) %>%
  mutate(measure = ordered(factor(measure), 
                           levels = c('phibic', 'phiaic', 'phiaicc', 'phiwd', 'omegatv', 'phiwrl')))

plot_data <- long_data %>%
  filter(states == 5)

ranks <- plot_data %>%
  filter(type == 'rank') %>%
  filter(measure == 'phiaic' | measure == 'phiwrl') %>%
  mutate(measure = recode(measure, phiaic = "phiaic, phibic, phiaicc, phiwd")) %>%
  ggplot(aes(y = value, x = N)) +
  geom_boxplot(aes(fill = ncovs), outlier.shape = NA) +
  facet_grid(measure ~ timepoints, labeller = label_both) + 
  labs(title = paste('Boxplots of the rank of the true subgroup in the top-20', 
                     sep = " ", collapse = NULL),
       fill = 'Z') + 
  xlab('Number of data sequences') + 
  ylab('Rank') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank()) + 
  scale_fill_manual(values=c("#e5f5e0", "#a1d99b", "#31a354"))

ranks

name <- paste('../figures/Figures_revised_manuscript/ranks_exceptional_starting_behaviour.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 16, units = "cm")

orders <- plot_data %>% 
  filter(type == 'order') %>%
  filter(measure != 'phiwrl') %>%
  filter(measure != 'omegatv') %>%
  filter(measure == 'phiaic' | measure == 'phiwd') %>%
  mutate(measure = recode(measure, phiaic = "phiaic, phibic, phiaicc")) %>%
  group_by(N, measure, true_subgroup_order, timepoints, states, ncovs) %>%
  summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / 10) %>%
  ggplot(aes(x = N, y = perc_true_order, fill = ncovs)) + 
  geom_bar(stat = "identity", position = position_dodge(), colour="black") + 
  facet_grid(measure ~ timepoints, labeller = label_both) + 
  labs(title = paste('Percentage of nreps where the true subgroup order is found', 
                     sep = " ", collapse = NULL),
       fill = 'Z') +
  xlab('Number of data sequences') + 
  ylab('Percentage') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank()) +
  scale_y_continuous(labels=seq(0, 100, 25), breaks=seq(0,100,25)) + 
  expand_limits(y = c(0, 100)) + 
  scale_fill_manual(values=c("#e5f5e0", "#a1d99b", "#31a354"))

orders

name <- paste('../figures/Figures_revised_manuscript/orders_exceptional_starting_behaviour.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 16, units = "cm")

#### Sensitivity Analysis ####

## varying global model, varying start parameter s

data50 <- read_excel("../data_output/results_revised_manuscript/experiment_varying_globalmodel_and_start_parameter_20210511_[10, [100], [20], [50], [5], [0.5], [2], [1, 3]].xlsx")
total_reps = 10
length_new_column = 6 * 4 * 10 * 1 * 1 * 1 * 1 * 2 * 2
long_data_50 <- data50 %>%
  pivot_longer(
    cols = names(data50)[12:dim(data50)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order', 'found_order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

data10200 <- read_excel("../data_output/results_revised_manuscript/experiment_varying_globalmodel_and_start_parameter_20210512_[10, [100], [20], [10, 200], [5], [0.5], [2], [1, 3]].xlsx")
total_reps = 10
length_new_column = 6 * 4 * 10 * 2 * 1 * 1 * 1 * 2 * 2
long_data_10200 <- data10200 %>%
  pivot_longer(
    cols = names(data10200)[12:dim(data10200)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order', 'found_order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

long_data <- rbind(long_data_50,long_data_10200) %>%
  arrange(nreps, as.integer(N), as.integer(T), as.integer(S), 
          as.integer(ncovs), as.integer(subgroup_orders), 
          as.integer(global_model_order), 
          as.integer(start_at_order)) %>%
  mutate(true_subgroup_order = as.factor(subgroup_orders)) %>%
  mutate(states = ordered(factor(S), levels = as.character(sort(as.integer(unique(S)))))) %>%
  mutate(timepoints = ordered(factor(T), levels = as.character(sort(as.integer(unique(T)))))) %>%
  mutate(ncovs = ordered(factor(ncovs), levels = as.character(sort(as.integer(unique(ncovs)))))) %>%
  mutate(N = ordered(factor(N), levels = as.character(sort(as.integer(unique(N)))))) %>%
  mutate(measure = ordered(factor(measure), levels = c('phibic', 'phiaic', 'phiaicc', 'phiwd', 'omegatv', 'phiwrl'))) %>%
  mutate(globalmodel = ordered(factor(global_model_order), levels = as.character(sort(as.integer(unique(global_model_order)))))) %>%
  mutate(s = ordered(factor(start_at_order), levels = as.character(sort(as.integer(unique(start_at_order)))))) %>%
  mutate(sglobalmodel = interaction(globalmodel, s))

long_data %>% 
  filter(type == 'rank') %>%
  ggplot(aes(y = measure, x = value)) + 
  geom_boxplot(aes(fill = true_subgroup_order), outlier.shape = NA) + #, outlier.alpha = 0.2, outlier.size=0.5) +
  facet_grid(sglobalmodel ~ timepoints, labeller = label_both) +
  labs(title = paste('Boxplots of the rank of the true subgroup in the top-20', 
                     sep = " ", collapse = NULL),
       fill = 'True subgroup order') + 
  xlab('Rank') + 
  ylab('Quality measure') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank()) + 
  scale_fill_manual(values=c("#fde0dd", "#fa9fb5", "#e0f3db", "#a8ddb5"))

table <- long_data %>% filter(type == 'rank') %>%
  filter(true_subgroup_order %in% c(2,3)) %>%
  filter(measure == 'phiwd') %>%
  group_by(measure, T, globalmodel, s, true_subgroup_order) %>% 
  summarise(median(value), IQR(value)) 

## varying subgroup size and description length

data20 <- read_excel("../data_output/results_revised_manuscript/experiment_varying_sample_size_20210512_[10, [100], [20], [50], [5], [0.35, 0.5], [1, 2], [1]].xlsx")
data510 <- read_excel("../data_output/results_revised_manuscript/experiment_varying_sample_size_20210513_[10, [100], [5, 10], [50], [5], [0.35, 0.5], [1, 2], [1]].xlsx")

total_reps = 10
length_new_column = 6 * 4 * 10 * 1 * 1 * 1 * 1 * 1 * 1 * 2 * 2
long_data_20 <- data20 %>%
  pivot_longer(
    cols = names(data20)[12:dim(data20)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order', 'found_order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

length_new_column = 6 * 4 * 10 * 1 * 1 * 2 * 1 * 1 * 1 * 2 * 2
long_data_510 <- data510 %>%
  pivot_longer(
    cols = names(data510)[12:dim(data510)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order', 'found_order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

long_data <- rbind(long_data_20, long_data_510) %>%
  arrange(nreps, as.integer(N), as.integer(T), as.integer(S), 
          as.integer(ncovs), as.integer(subgroup_orders), 
          as.integer(global_model_order), 
          as.integer(start_at_order)) %>%
  mutate(true_subgroup_order = as.factor(subgroup_orders)) %>%
  mutate(states = ordered(factor(S), levels = as.character(sort(as.integer(unique(S)))))) %>%
  mutate(timepoints = ordered(factor(T), levels = as.character(sort(as.integer(unique(T)))))) %>%
  mutate(ncovs = ordered(factor(ncovs), levels = as.character(sort(as.integer(unique(ncovs)))))) %>%
  mutate(N = ordered(factor(N), levels = as.character(sort(as.integer(unique(N)))))) %>%
  mutate(measure = ordered(factor(measure), levels = c('phibic', 'phiaic', 'phiaicc', 'phiwd', 'omegatv', 'phiwrl'))) %>%
  mutate(globalmodel = ordered(factor(global_model_order), levels = as.character(sort(as.integer(unique(global_model_order)))))) %>%
  mutate(s = ordered(factor(start_at_order), levels = as.character(sort(as.integer(unique(start_at_order)))))) %>%
  mutate(sglobalmodel = interaction(globalmodel, s)) %>%
  mutate(desc = ordered(factor(true_desc_length))) %>%
  mutate(p = ordered(factor(p))) %>%
  mutate(descp = interaction(desc, p))

long_data %>% filter(type == 'rank') %>%
  ggplot(aes(y = measure, x = value)) + 
  geom_boxplot(aes(fill = true_subgroup_order), outlier.shape = NA) + #, outlier.alpha = 0.2, outlier.size=0.5) +
  facet_grid(descp ~ ncovs, labeller = label_both) +
  labs(title = paste('Boxplots of the rank of the true subgroup in the top-20', 
                     sep = " ", collapse = NULL),
       fill = 'True subgroup order') + 
  xlab('Rank') + 
  ylab('Quality measure') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank()) + 
  scale_fill_manual(values=c("#fde0dd", "#fa9fb5", "#e0f3db", "#a8ddb5"))

table <- long_data %>% filter(type == 'rank') %>%
  filter(true_subgroup_order %in% c(1,4)) %>%
  filter(measure == 'phiwrl') %>%
  group_by(measure, desc, p, ncovs, true_subgroup_order) %>% 
  summarise(median(value), IQR(value), n()) 
