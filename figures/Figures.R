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
### first type of simulations
data <- read_excel("../data_output/experiment_higherorders_20201111_25nreps_[100]_[2, 5, 25]_[2, 5, 25]_[2, 5, 25].xlsx")
head(data)

long_data <- data %>%
  pivot_longer(
    cols = names(data)[8:27],
    names_to = "measure",
    values_to = "value") %>%
  add_column(type = rep(c('rank', 'order'), 10*3*3*3*2*25)) %>%
  mutate(measure = gsub("_.*", "", measure)) %>%
  mutate(true_subgroup_order = as.factor(subgroup_orders)) %>%
  mutate(states = factor(S)) %>%
  mutate(timepoints = factor(T)) %>%
  mutate(ncovs = factor(ncovs))

head(long_data)

sel_measure = 'deltatv'

plot_data <- long_data %>%
  filter(N == 100) %>%
  filter(measure == sel_measure)

plot_data %>% 
  filter(type == 'rank') %>%
  ggplot(aes(y = value, x = true_subgroup_order)) +
  geom_boxplot(aes(fill = ncovs)) +
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

# order data

plot_data %>% 
  filter(type == 'order') %>%
  group_by(true_subgroup_order, timepoints, states, ncovs) %>%
  summarize(perc_true_order = 
              100 * sum(subgroup_orders == 
                          value, na.rm = TRUE) / 25) %>%
  ggplot(aes(x = true_subgroup_order, y = perc_true_order, fill = ncovs)) + 
  geom_bar(stat = "identity", position = position_dodge()) + 
  facet_grid(timepoints ~ states, labeller = label_both) + 
  labs(title = paste(sel_measure, 
                     ': percentage of simulations that the true subgroup order is found', 
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

dat <- long_data %>%
  filter(N == 100) %>%
  filter(T == 25) %>%
  filter(S == 25) %>%
  filter(ncovs == 5) %>%
  filter(subgroup_orders == 1) %>%
  filter(measure == 'phiaicc') %>%
  filter(type == 'rank')
