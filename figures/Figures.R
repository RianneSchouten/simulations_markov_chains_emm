library(ggplot2)
library(readxl)
library(tidyverse)
library(RColorBrewer)
library(mice)

setwd("C:/Users/20200059/Documents/Github/simulations_beam_search_markov_chain/figures/")

# #### Simulation results and figures for work in progress paper september 2020 ####
# #data <- read_excel("../data_output/experiment_initialprobs_20200608_10nreps_[100, 1000]_[2, 5, 25]_[2, 5, 25]_[2, 5, 25].xlsx")
# 
# ### first type of simulations
# data <- read_excel("../data_output/experiment_initialprobs_20200102_25nreps_[100]_[2, 5, 25]_[2, 5, 25]_[2, 5, 25]_5.xlsx")
# head(data)
# names(data)
# 
# long_data <- data %>%
#   rename(delta_tv = deltatv,
#          omega_tv = omegatv,
#          phi_wd = phiwd, 
#          phi_kl = phikl,
#          #phi_bic = phibic, 
#          phi_arl = phiarl, 
#          phi_warl = phiwarl) %>%
#   pivot_longer(
#     cols = c('delta_tv', 'omega_tv', 'phi_wd', 'phi_kl', 'phi_arl', 'phi_warl'),
#     names_to = "measure",
#     values_to = "Rank") %>%
#   mutate(facet = case_when(distAyn == 0 & distPiyn == 0 ~ 'No difference',
#                            distAyn == 1 & distPiyn == 0 ~ 'Difference in transition matrix A',
#                            distAyn == 0 & distPiyn == 1 ~ 'Difference in initial probabilities pi',
#                            distAyn == 1 & distPiyn == 1 ~ 'Difference in both A and pi')) %>%
#   mutate(facet = factor(facet, levels = c('No difference', 'Difference in transition matrix A', 
#                                           'Difference in initial probabilities pi', 'Difference in both A and pi'))) %>%
#   mutate(measure = factor(measure, levels = c('phi_warl', 'phi_arl', 'phi_kl', 
#                                               'phi_wd', 'omega_tv', 'delta_tv')))
# 
# # plot 1
# 
# plot_data <- long_data %>%
#   filter(N == 100) %>%
#   filter(T == 25) %>%
#   filter(S == 25)
# 
# plot1 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
#   geom_boxplot(aes(fill = as.factor(ncovs))) +
#   coord_flip() + 
#   facet_wrap(facet~., ncol = 2) +
#   labs(title = 'Ranks of the true subgroup',
#        fill = 'ncovs') +
#   guides(fill = guide_legend(direction = "horizontal")) +
#   theme(legend.position="top",
#         legend.justification="right",
#         plot.title = element_text(vjust=-4), 
#         legend.box.margin = margin(-1,0,0,0, "line"),
#         axis.title.y = element_blank(),
#         panel.grid.major.x = element_blank(),
#         panel.grid.minor.x = element_blank())
#   
# plot1
# ggsave("plot_100_25_25.eps", width = 20, height = 20, units = "cm")
# 
# # plot 2
# plot_data <- long_data %>%
#   filter(N == 100) %>%
#   filter(T == 5) %>%
#   filter(S == 5) %>%
#   filter((distAyn == 0 & distPiyn == 1)|(distAyn == 1 & distPiyn == 0))
# 
# plot2 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
#   geom_boxplot(aes(fill = as.factor(ncovs))) +
#   coord_flip() + 
#   facet_wrap(facet~., ncol = 2) +
#   labs(title = 'Ranks of the true subgroup',
#        fill = 'ncovs') +
#   guides(fill = guide_legend(direction = "horizontal")) +
#   theme(legend.position="top",
#         legend.justification="right",
#         plot.title = element_text(vjust=-4), 
#         legend.box.margin = margin(-1,0,0,0, "line"),
#         axis.title.y = element_blank(),
#         panel.grid.major.x = element_blank(),
#         panel.grid.minor.x = element_blank()
#   )
# 
# plot2
# ggsave("plot_100_5_5.eps", width = 20, height = 11, units = "cm")
# 
# plot_data <- long_data %>%
#   filter(N == 100) %>%
#   filter(T == 25) %>%
#   filter(S == 5)
# 
# plot2 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
#   geom_boxplot(aes(fill = as.factor(ncovs))) +
#   coord_flip() + 
#   facet_wrap(facet~., ncol = 2) +
#   labs(title = 'Ranks of the true subgroup',
#        fill = 'ncovs') +
#   guides(fill = guide_legend(direction = "horizontal")) +
#   theme(legend.position="top",
#         legend.justification="right",
#         plot.title = element_text(vjust=-4), 
#         legend.box.margin = margin(-1,0,0,0, "line"),
#         axis.title.y = element_blank(),
#         panel.grid.major.x = element_blank(),
#         panel.grid.minor.x = element_blank()
#   )
# 
# plot2
# 
# ## presentation
# plot_data <- long_data %>%
#   filter(N == 100) %>%
#   filter(T == 5) %>%
#   filter(S == 5) %>%
#   filter((distAyn == 0 & distPiyn == 1))
# 
# plot_for_presentation_1 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
#   geom_boxplot(aes(fill = as.factor(ncovs))) +
#   coord_flip() + 
#   facet_wrap(facet~., ncol = 2) +
#   labs(title = 'Difference in initial probabilities',
#        fill = 'ncovs') +
#   guides(fill = guide_legend(direction = "horizontal")) +
#   theme(legend.position="top",
#         legend.justification="right",
#         plot.title = element_text(vjust=-4), 
#         legend.box.margin = margin(-1,0,0,0, "line"),
#         axis.title.y = element_blank(),
#         panel.grid.major.x = element_blank(),
#         panel.grid.minor.x = element_blank())
# 
# plot_for_presentation_1
# ggsave("plot_100_5_5_pi.eps", width = 16, height = 20, units = "cm")
# 
# plot_data <- long_data %>%
#   filter(N == 100) %>%
#   filter(T == 25) %>%
#   filter(S == 25) %>%
#   filter((distAyn == 1 & distPiyn == 0))
# 
# plot_for_presentation_2 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
#   geom_boxplot(aes(fill = as.factor(ncovs))) +
#   coord_flip() + 
#   facet_wrap(facet~., ncol = 2) +
#   labs(title = 'Difference in transition matrix',
#        fill = 'ncovs') +
#   guides(fill = guide_legend(direction = "horizontal")) +
#   theme(legend.position="top",
#         legend.justification="right",
#         plot.title = element_text(vjust=-4), 
#         legend.box.margin = margin(-1,0,0,0, "line"),
#         axis.title.y = element_blank(),
#         panel.grid.major.x = element_blank(),
#         panel.grid.minor.x = element_blank())
# 
# plot_for_presentation_2
# ggsave("plot_100_25_25_Aboth.eps", width = 16, height = 20, units = "cm")

#### Simulation results and figures for firstpaperdraft december 2020 ####

# first set with start at start_at_order = 4 and multiple orders on 13-11
data <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201113_25nreps_[100]_[50, 25, 10]_[10, 5]_[20, 10, 5].xlsx")
# at 11 11, order 0 and 1 with start at order = 1
#data <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201111_25nreps_[100]_[2, 5, 25]_[2, 5, 25]_[2, 5, 25].xlsx")
# here, we compare with the complement and find out we should increase the dimensions
#data <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201117_10nreps_[100, 500]_[50, 200]_[2, 5, 10]_[20].xlsx")
# we add a setting for states = 2 to the experiments on 13-11
data2 <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201118_25nreps_[100]_[50, 25, 10]_[2]_[20, 10, 5].xlsx")
# we add a setting for times = 200 to the experiments on 13-11
data3 <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201118_10nreps_[100]_[200]_[10, 5, 2]_[20, 10, 5].xlsx")
# we repeat phi aicc for 200 because we find that there is a problem when we restructured the code on 18-11
data_phiaicc_200 <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201123_10nreps_[100]_[200]_[10, 5, 2]_[20, 10, 5].xlsx")
# we run omegatv again to be sure about the output
data_omegatv <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201124_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
# we run phiwd again to be sure about the output
data_phiwd <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201125_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
# we find a mistake in phiwrl and repeat those simulations
data_phiwrl <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201126_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")

#head(data)
#head(data2)
#head(data3)
#head(data4)

data2 <- data2[, c(1:6, 8:20)]
data3 <- data3[, c(1:6, 8:20)]
data_phiaicc_200 <- data_phiaicc_200[, c(1:6, 8:10)]
data_omegatv <- data_omegatv[, c(1:6, 8:10)]
data_phiwd <- data_phiwd[, c(1:6, 8:10)]
data_phiwrl <- data_phiwrl[, c(1:6, 8:10)]

#head(data)

#length_new_column = 6 * 5 * 25 * 1 * 3 * 2 * 3
#length_new_column = 10 * 2 * 25 * 1 * 3 * 3 * 3
#length_new_column = 1 * 5 * 10 * 2 * 2 * 3 * 1

# process data 1
data1 <- data %>%
  filter(T != 25) %>%
  filter(subgroup_orders != 0) %>%
  select(-omegatv_order) %>%
  select(-omegatv_rank) %>%
  select(-phiwd_rank) %>%
  select(-phiwd_order)  %>%
  select(-phiwarl_rank) %>%
  select(-phiwarl_order)
length_new_column1 = 3 * 4 * 25 * 1 * 2 * 2 * 3
long_data1 <- data1 %>%
  pivot_longer(
    cols = names(data1)[8:dim(data1)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column1)) %>%
  mutate(measure = gsub("_.*", "", measure))

# process data 2
data2 <- data2 %>%
  filter(T != 25) %>%
  filter(subgroup_orders != 0) %>%
  select(-omegatv_order) %>%
  select(-omegatv_rank) %>%
  select(-phiwd_rank) %>%
  select(-phiwd_order)  %>%
  select(-phiwarl_rank) %>%
  select(-phiwarl_order)
length_new_column2 = 3 * 4 * 25 * 1 * 2 * 1 * 3
long_data2 <- data2 %>%
  pivot_longer(
    cols = names(data2)[8:dim(data1)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column2)) %>%
  mutate(measure = gsub("_.*", "", measure))

# add timepoints 200
# process data 3
data3 <- data3 %>%
  select(-phiaicc_order) %>%
  select(-phiaicc_rank) %>% 
  select(-omegatv_order) %>%
  select(-omegatv_rank) %>%
  filter(subgroup_orders != 0) %>%
  select(-phiwd_rank) %>%
  select(-phiwd_order)  %>%
  select(-phiwarl_rank) %>%
  select(-phiwarl_order)
length_new_column3 = 2 * 4 * 10 * 1 * 1 * 3 * 3
long_data3 <- data3 %>%
  pivot_longer(
    cols = names(data3)[8:dim(data3)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column3)) %>%
  mutate(measure = gsub("_.*", "", measure))

# process data 4
length_new_column4 = 1 * 4 * 10 * 1 * 1 * 3 * 3
long_data4 <- data_phiaicc_200 %>%
  pivot_longer(
    cols = names(data_phiaicc_200)[8:dim(data_phiaicc_200)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column4)) %>%
  mutate(measure = gsub("_.*", "", measure))

# repeat all of it for omegatv
# process data 5
length_new_column5 = 1 * 4 * 10 * 1 * 3 * 3 * 3
long_data5 <- data_omegatv %>%
  pivot_longer(
    cols = names(data_omegatv)[8:dim(data_omegatv)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column5)) %>%
  mutate(measure = gsub("_.*", "", measure))

# repeat all of it for phiwd
# process data 6
length_new_column6 = 1 * 4 * 10 * 1 * 3 * 3 * 3
long_data6 <- data_phiwd %>%
  pivot_longer(
    cols = names(data_phiwd)[8:dim(data_phiwd)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column6)) %>%
  mutate(measure = gsub("_.*", "", measure))

# repeat all of it for phiwrl
# process data 7
length_new_column7 = 1 * 4 * 10 * 1 * 3 * 3 * 3
long_data7 <- data_phiwrl %>%
  pivot_longer(
    cols = names(data_phiwrl)[8:dim(data_phiwrl)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column7)) %>%
  mutate(measure = gsub("_.*", "", measure))

long_data <- rbind(long_data1, long_data2, long_data3, long_data4, long_data5,
                   long_data6, long_data7) %>%
  mutate(value = case_when(
    value == 0 & type == 'order' ~ 1, # we stop now at order = 1
    TRUE ~ value)) %>%
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
  ggplot(aes(y = value, x = true_subgroup_order)) +
  geom_boxplot(aes(fill = states), outlier.shape = NA) + #, outlier.alpha = 0.2, outlier.size=0.5) +
  facet_grid(measure ~ timepoints, labeller = label_both) + 
  labs(title = paste('Boxplots of the rank of the true subgroup in the resultlist', 
                     sep = " ", collapse = NULL),
       fill = 'states') + 
  xlab('true subgroup order') + 
  ylab('') +
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

name <- paste('ranks_20ncovs.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 30, units = "cm")

plot_order_data1 <- plot_data %>% 
  filter(timepoints != 200) %>%
  filter(type == 'order') %>% 
  filter(measure == 'omegatv' | measure == 'phiwd' | measure == 'phiwrl') %>%
  group_by(N, measure, true_subgroup_order, timepoints, states, ncovs) %>%
  summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / 10)

plot_order_data2 <- plot_data %>% 
  filter(timepoints != 200) %>%
  filter(type == 'order') %>% 
  filter(measure != 'omegatv' & measure != 'phiwd' & measure != 'phiwrl') %>%
  group_by(N, measure, true_subgroup_order, timepoints, states, ncovs) %>%
  summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / 25)

plot_order_data3 <- plot_data %>% 
  filter(timepoints == 200) %>%
  filter(type == 'order') %>%
  group_by(N, measure, true_subgroup_order, timepoints, states, ncovs) %>%
  summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / 10)

orders <- rbind(plot_order_data1, plot_order_data2, plot_order_data3) %>%
  ggplot(aes(x = true_subgroup_order, y = perc_true_order, fill = states)) + 
  geom_bar(stat = "identity", position = position_dodge()) + 
  facet_grid(measure ~ timepoints, labeller = label_both) + 
  labs(title = paste('Percentage of nreps where the true subgroup order is found', 
                     sep = " ", collapse = NULL)) +
  xlab('true subgroup order') + 
  ylab('') +
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

name <- paste('orders_20ncovs.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 30, units = "cm")

## full figures

all_measures <- unique(long_data$measure)
for(i in 1:length(all_measures)){
  sel_measure = all_measures[i]
  print(sel_measure)

  plot_data <- long_data %>%
    filter(N == 100) %>%
    filter(measure == sel_measure)

  ranks <- plot_data %>% 
    filter(type == 'rank') %>%
    ggplot(aes(y = value, x = true_subgroup_order)) +
    geom_boxplot(aes(fill = ncovs), outlier.shape = NA) + #, outlier.alpha = 0.2, outlier.size=0.5) +
    facet_grid(timepoints ~ states, labeller = label_both) + 
    labs(title = paste(sel_measure, 
                     ': boxplots of the rank of the true subgroup in the resultlist', 
                     sep = " ", collapse = NULL),
       fill = 'ncovs') + 
    xlab('true subgroup order') + 
    ylab('') +
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
    scale_fill_manual(values=c("#CC6666", "#9999CC", "#66CC99"))

  ranks

  name <- paste(sel_measure, '_ranks.eps', sep = "", collapse = NULL)
  ggsave(name, dpi = 300) #width = 20, height = 16, units = "cm")

  # order data
  # last three measures are divided by 10
  if (sel_measure %in% c('omegatv', 'phiwd', 'phiwrl')){
    divide <- 10
  } else {
    divide <- 25
  }
  
  plot_order_data1 <- plot_data %>% 
    filter(timepoints != 200) %>%
    filter(type == 'order') %>% 
    group_by(N, true_subgroup_order, timepoints, states, ncovs) %>%
    summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / divide)

  plot_order_data3 <- plot_data %>% 
    filter(timepoints == 200) %>%
    filter(type == 'order') %>%
    group_by(N, true_subgroup_order, timepoints, states, ncovs) %>%
    summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / 10)

  orders <- rbind(plot_order_data1, plot_order_data3) %>%
    ggplot(aes(x = true_subgroup_order, y = perc_true_order, fill = ncovs)) + 
    geom_bar(stat = "identity", position = position_dodge()) + 
    facet_grid(timepoints ~ states, labeller = label_both) + 
    labs(title = paste(sel_measure, 
                     ': percentage of nreps where the true subgroup order is found', 
                     sep = " ", collapse = NULL)) +
    xlab('true subgroup order') + 
    ylab('') +
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
    scale_fill_manual(values=c("#CC6666", "#9999CC", "#66CC99"))

  name <- paste(sel_measure, '_orders.eps', sep = "", collapse = NULL)
  ggsave(name, dpi = 300)
}

### Only zero order with start at order = 1
# wrl is wrong and we need to repeat
data <- read_excel("../data_output/experiment_higherorders_20201120_10nreps_[100, 500, 1000]_[2, 5, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
data_wrl <- read_excel("../data_output/experiment_higherorders_20201126_10nreps_[100, 500, 1000]_[10, 5, 2]_[10, 5, 2]_[20, 10, 5].xlsx")

data <- data[, c(1:6, 8:20)]
data1 <- data %>%
  select(-phiwarl_order) %>%
  select(-phiwarl_rank)
length_new_column = 5 * 1 * 10 * 3 * 3 * 3 * 3
long_data1 <- data1 %>%
  pivot_longer(
    cols = names(data1)[8:dim(data1)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

data2 <- data_wrl[, c(1:6, 8:10)]
length_new_column2 = 1 * 1 * 10 * 3 * 3 * 3 * 3
long_data2 <- data2 %>%
  pivot_longer(
    cols = names(data2)[8:dim(data2)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column2)) %>%
  mutate(measure = gsub("_.*", "", measure))

long_data <- rbind(long_data1, long_data2) %>%
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
  #filter(ncovs == 20) %>%
  #filter(N == 100) %>%
  #filter(measure == sel_measure) %>%
  filter(states == 5)

ranks <- plot_data %>% 
  filter(type == 'rank') %>%
  ggplot(aes(y = value, x = N)) +
  geom_boxplot(aes(fill = ncovs), outlier.shape = NA) +
  facet_grid(measure ~ timepoints, labeller = label_both) + 
  labs(title = paste('Boxplots of the rank of the true subgroup', 
                     sep = " ", collapse = NULL),
       fill = 'ncovs') + 
  xlab('true subgroup order') + 
  ylab('') +
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

name <- paste('ranks_exceptional_starting_behaviour.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 30, units = "cm")

# order data

orders <- plot_data %>% 
  filter(type == 'order') %>%
  group_by(N, measure, true_subgroup_order, timepoints, states, ncovs) %>%
  summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / 10) %>%
  ggplot(aes(x = N, y = perc_true_order, fill = ncovs)) + 
  geom_bar(stat = "identity", position = position_dodge()) + 
  facet_grid(measure ~ timepoints, labeller = label_both) + 
  labs(title = paste('Percentage of nreps where the true subgroup order is found', 
                     sep = " ", collapse = NULL)) +
  xlab('number of data sequences') + 
  ylab('') +
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

name <- paste('orders_exceptional_starting_behaviour.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 30, units = "cm")

## full figures

all_measures <- unique(long_data$measure)
for(i in 1:length(all_measures)){
  sel_measure = all_measures[i]
  print(sel_measure)
  
  plot_data <- long_data %>%
    filter(measure == sel_measure)
  
  ranks <- plot_data %>% 
    filter(type == 'rank') %>%
    ggplot(aes(y = value, x = N)) +
    geom_boxplot(aes(fill = ncovs), outlier.shape = NA) + #, outlier.alpha = 0.2, outlier.size=0.5) +
    facet_grid(timepoints ~ states, labeller = label_both) + 
    labs(title = paste(sel_measure, 
                       ': boxplots of the rank of the true subgroup in the resultlist', 
                       sep = " ", collapse = NULL),
         fill = 'ncovs') + 
    xlab('number of data sequences') +  
    ylab('') +
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
    scale_fill_manual(values=c("#CC6666", "#9999CC", "#66CC99"))

  name <- paste(sel_measure, '_ranks_exceptionalstartingbehaviour.eps', sep = "", collapse = NULL)
  ggsave(name, dpi = 300) #width = 20, height = 16, units = "cm")
  
  orders <- plot_data %>% 
    filter(type == 'order') %>%
    group_by(N, measure, true_subgroup_order, timepoints, states, ncovs) %>%
    summarize(perc_true_order = 
                100 * sum(subgroup_orders == 
                            value, na.rm = TRUE) / 10) %>%
    ggplot(aes(x = N, y = perc_true_order, fill = ncovs)) + 
    geom_bar(stat = "identity", position = position_dodge()) + 
    facet_grid(timepoints ~ states, labeller = label_both) + 
    labs(title = paste(sel_measure, 
                       ': percentage of nreps where the true subgroup order is found', 
                       sep = " ", collapse = NULL)) +
    xlab('number of data sequences') + 
    ylab('') +
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
    scale_fill_manual(values=c("#CC6666", "#9999CC", "#66CC99"))
  
  name <- paste(sel_measure, '_orders_exceptionalstartingbehaviour.eps', sep = "", collapse = NULL)
  ggsave(name, dpi = 300)
  
}

#### Simulation results and figures for manuscript january 2021 ####

data_omegatv <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201124_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
data_phiwd <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201125_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
data_phiwrl <- read_excel("../data_output/results first paper draft/experiment_higherorders_20201126_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
data_rest <- read_excel("../data_output/results_manuscript/experiment_higherorders_20210107_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")

data_09 <- read_excel("../data_output/results_manuscript/experiment_higherorders_20210109_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
data_10 <- read_excel("../data_output/results_manuscript/experiment_higherorders_20210110_10nreps_[100]_[200, 50, 10]_[10, 5, 2]_[20, 10, 5].xlsx")

length_new_column = 1 * 4 * 10 * 1 * 3 * 3 * 3
long_data_omegatv <- data_omegatv %>%
  pivot_longer(
    cols = names(data_omegatv)[9:dim(data_omegatv)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

long_data_phiwd <- data_phiwrl %>%
  pivot_longer(
    cols = names(data_phiwrl)[9:dim(data_phiwrl)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

long_data_phiwrl <- data_omegatv %>%
  pivot_longer(
    cols = names(data_omegatv)[9:dim(data_omegatv)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

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

long_data_10 <- data_10 %>%
  pivot_longer(
    cols = names(data_10)[9:dim(data_10)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure))

long_data <- rbind(long_data_omegatv, long_data_phiwd, long_data_phiwrl, 
                   long_data_rest,
                   long_data_09, long_data_10) %>%
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
  ggplot(aes(y = value, x = true_subgroup_order)) +
  geom_boxplot(aes(fill = states), outlier.shape = NA) + #, outlier.alpha = 0.2, outlier.size=0.5) +
  facet_grid(measure ~ timepoints, labeller = label_both) + 
  labs(title = paste('Boxplots of the rank of the true subgroup in the resultlist', 
                     sep = " ", collapse = NULL),
       fill = 'states') + 
  xlab('true subgroup order') + 
  ylab('') +
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

name <- paste('../figures/Figures_manuscript/ranks_20ncovs.eps', sep = "", collapse = NULL)
ggsave(name, width = 20, height = 30, units = "cm")

