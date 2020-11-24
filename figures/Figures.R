library(ggplot2)
library(readxl)
library(tidyverse)
library(RColorBrewer)
library(mice)

setwd("C:/Users/20200059/Documents/Github/simulations_beam_search_markov_chain/figures/")
#data <- read_excel("../data_output/experiment_initialprobs_20200608_10nreps_[100, 1000]_[2, 5, 25]_[2, 5, 25]_[2, 5, 25].xlsx")

### first type of simulations
data <- read_excel("../data_output/experiment_initialprobs_20200102_25nreps_[100]_[2, 5, 25]_[2, 5, 25]_[2, 5, 25]_5.xlsx")
head(data)
names(data)

long_data <- data %>%
  rename(delta_tv = deltatv,
         omega_tv = omegatv,
         phi_wd = phiwd, 
         phi_kl = phikl,
         #phi_bic = phibic, 
         phi_arl = phiarl, 
         phi_warl = phiwarl) %>%
  pivot_longer(
    cols = c('delta_tv', 'omega_tv', 'phi_wd', 'phi_kl', 'phi_arl', 'phi_warl'),
    names_to = "measure",
    values_to = "Rank") %>%
  mutate(facet = case_when(distAyn == 0 & distPiyn == 0 ~ 'No difference',
                           distAyn == 1 & distPiyn == 0 ~ 'Difference in transition matrix A',
                           distAyn == 0 & distPiyn == 1 ~ 'Difference in initial probabilities pi',
                           distAyn == 1 & distPiyn == 1 ~ 'Difference in both A and pi')) %>%
  mutate(facet = factor(facet, levels = c('No difference', 'Difference in transition matrix A', 
                                          'Difference in initial probabilities pi', 'Difference in both A and pi'))) %>%
  mutate(measure = factor(measure, levels = c('phi_warl', 'phi_arl', 'phi_kl', 
                                              'phi_wd', 'omega_tv', 'delta_tv')))

# plot 1

plot_data <- long_data %>%
  filter(N == 100) %>%
  filter(T == 25) %>%
  filter(S == 25)

plot1 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
  geom_boxplot(aes(fill = as.factor(ncovs))) +
  coord_flip() + 
  facet_wrap(facet~., ncol = 2) +
  labs(title = 'Ranks of the true subgroup',
       fill = 'ncovs') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank())
  
plot1
ggsave("plot_100_25_25.eps", width = 20, height = 20, units = "cm")

# plot 2
plot_data <- long_data %>%
  filter(N == 100) %>%
  filter(T == 5) %>%
  filter(S == 5) %>%
  filter((distAyn == 0 & distPiyn == 1)|(distAyn == 1 & distPiyn == 0))

plot2 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
  geom_boxplot(aes(fill = as.factor(ncovs))) +
  coord_flip() + 
  facet_wrap(facet~., ncol = 2) +
  labs(title = 'Ranks of the true subgroup',
       fill = 'ncovs') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank()
  )

plot2
ggsave("plot_100_5_5.eps", width = 20, height = 11, units = "cm")

plot_data <- long_data %>%
  filter(N == 100) %>%
  filter(T == 25) %>%
  filter(S == 5)

plot2 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
  geom_boxplot(aes(fill = as.factor(ncovs))) +
  coord_flip() + 
  facet_wrap(facet~., ncol = 2) +
  labs(title = 'Ranks of the true subgroup',
       fill = 'ncovs') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank()
  )

plot2

## presentation
plot_data <- long_data %>%
  filter(N == 100) %>%
  filter(T == 5) %>%
  filter(S == 5) %>%
  filter((distAyn == 0 & distPiyn == 1))

plot_for_presentation_1 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
  geom_boxplot(aes(fill = as.factor(ncovs))) +
  coord_flip() + 
  facet_wrap(facet~., ncol = 2) +
  labs(title = 'Difference in initial probabilities',
       fill = 'ncovs') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank())

plot_for_presentation_1
ggsave("plot_100_5_5_pi.eps", width = 16, height = 20, units = "cm")

plot_data <- long_data %>%
  filter(N == 100) %>%
  filter(T == 25) %>%
  filter(S == 25) %>%
  filter((distAyn == 1 & distPiyn == 0))

plot_for_presentation_2 <- ggplot(plot_data, aes(y = Rank, x = measure)) +
  geom_boxplot(aes(fill = as.factor(ncovs))) +
  coord_flip() + 
  facet_wrap(facet~., ncol = 2) +
  labs(title = 'Difference in transition matrix',
       fill = 'ncovs') +
  guides(fill = guide_legend(direction = "horizontal")) +
  theme(legend.position="top",
        legend.justification="right",
        plot.title = element_text(vjust=-4), 
        legend.box.margin = margin(-1,0,0,0, "line"),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank())

plot_for_presentation_2
ggsave("plot_100_25_25_Aboth.eps", width = 16, height = 20, units = "cm")

### Second type of simulations
data <- read_excel("../data_output/experiment_higherorders_20201113_25nreps_[100]_[50, 25, 10]_[10, 5]_[20, 10, 5].xlsx")
#data <- read_excel("../data_output/experiment_higherorders_20201111_25nreps_[100]_[2, 5, 25]_[2, 5, 25]_[2, 5, 25].xlsx")
#data <- read_excel("../data_output/experiment_higherorders_20201117_10nreps_[100, 500]_[50, 200]_[2, 5, 10]_[20].xlsx")
data2 <- read_excel("../data_output/experiment_higherorders_20201118_25nreps_[100]_[50, 25, 10]_[2]_[20, 10, 5].xlsx")
data3 <- read_excel("../data_output/experiment_higherorders_20201118_10nreps_[100]_[200]_[10, 5, 2]_[20, 10, 5].xlsx")
data4 <- read_excel("../data_output/experiment_higherorders_20201123_10nreps_[100]_[200]_[10, 5, 2]_[20, 10, 5].xlsx")

#head(data)
#head(data2)
#head(data3)
#head(data4)

data2 <- data2[, c(1:6, 8:20)]
data3 <- data3[, c(1:6, 8:20)]
data4 <- data4[, c(1:6, 8:10)]

#head(data)

#length_new_column = 6 * 5 * 25 * 1 * 3 * 2 * 3
#length_new_column = 10 * 2 * 25 * 1 * 3 * 3 * 3
#length_new_column = 1 * 5 * 10 * 2 * 2 * 3 * 1

# process data 1
data1 <- data %>%
  filter(T != 25) %>%
  filter(subgroup_orders != 0)
length_new_column1 = 6 * 4 * 25 * 1 * 2 * 2 * 3
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
  filter(subgroup_orders != 0)
length_new_column2 = 6 * 4 * 25 * 1 * 2 * 1 * 3
long_data2 <- data2 %>%
  pivot_longer(
    cols = names(data2)[8:dim(data1)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column2)) %>%
  mutate(measure = gsub("_.*", "", measure))

# process data 3
data3 <- data3 %>%
  select(-phiaicc_order) %>%
  select(-phiaicc_rank) %>%
  filter(subgroup_orders != 0)
length_new_column3 = 5 * 4 * 10 * 1 * 1 * 3 * 3
long_data3 <- data3 %>%
  pivot_longer(
    cols = names(data3)[8:dim(data3)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column3)) %>%
  mutate(measure = gsub("_.*", "", measure))

# process data 4
length_new_column4 = 1 * 4 * 10 * 1 * 1 * 3 * 3
long_data4 <- data4 %>%
  pivot_longer(
    cols = names(data4)[8:dim(data4)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column4)) %>%
  mutate(measure = gsub("_.*", "", measure))

long_data <- rbind(long_data1, long_data2, long_data3, long_data4) %>%
  mutate(value = case_when(
    value == 0 & type == 'order' ~ 1,
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
                     levels = as.character(sort(as.integer(unique(N))))))

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
                     ': boxplots of the resultlist rank of the true subgroup', 
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
plot_order_data1
  plot_order_data1 <- plot_data %>% 
    filter(timepoints != 200) %>%
    filter(type == 'order') %>% 
    group_by(N, true_subgroup_order, timepoints, states, ncovs) %>%
    summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / 25)

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
                     ': percentage where the true subgroup order is found', 
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

### Only zero order
data <- read_excel("../data_output/experiment_higherorders_20201120_10nreps_[100, 500, 1000]_[2, 5, 10]_[10, 5, 2]_[20, 10, 5].xlsx")
head(data)

length_new_column = 6 * 1 * 10 * 3 * 3 * 3 * 3
  
long_data <- data %>%
  pivot_longer(
    cols = names(data)[9:dim(data)[2]],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), length_new_column)) %>%
  mutate(measure = gsub("_.*", "", measure)) %>% 
  arrange(nreps, as.integer(T), as.integer(S), as.integer(ncovs), as.integer(subgroup_orders)) %>%
  mutate(true_subgroup_order = as.factor(subgroup_orders)) %>%
  mutate(states = ordered(factor(S), levels = c("2", "5", "10"))) %>%
  mutate(timepoints = ordered(factor(T), levels = c("2", "5", "10"))) %>%
  mutate(ncovs = ordered(factor(ncovs), levels = c("5", "10", "20"))) %>%
  mutate(N = ordered(factor(N), levels = c("100", "500", "1000"))) %>%
  mutate(measure = ordered(factor(measure), levels = c("omegatv", "phiwd", "phibic",
                                                       "phiaic", "phiaicc", "phiwarl")))

plot_data <- long_data %>%
  #filter(ncovs == 20) %>%
  #filter(N == 100) %>%
  #filter(measure == sel_measure) %>%
  filter(states == 5)

ranks <- plot_data %>% 
  filter(type == 'rank') %>%
  ggplot(aes(y = value, x = N)) +
  geom_boxplot(aes(fill = ncovs), outlier.shape = NA) +
  facet_grid(timepoints ~ measure, labeller = label_both) + 
  labs(title = paste('Rank of a true subgroup with exceptional starting behaviour', 
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

name <- paste('ranks_exceptional_starting_behaviour.eps', sep = "", collapse = NULL)
ggsave(name, dpi = 300) #width = 20, height = 16, units = "cm")

# order data

orders <- plot_data %>% 
  filter(type == 'order') %>%
  group_by(N, measure, true_subgroup_order, timepoints, states, ncovs) %>%
  summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / 10) %>%
  ggplot(aes(x = N, y = perc_true_order, fill = ncovs)) + 
  geom_bar(stat = "identity", position = position_dodge()) + 
  facet_grid(timepoints ~ measure, labeller = label_both) + 
  labs(title = paste('% where the true subgroup order of 0 is found', 
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

name <- paste('orders_exceptional_starting_behaviour.eps', sep = "", collapse = NULL)
ggsave(name, dpi = 300) #width = 20, height = 16, units = "cm")
