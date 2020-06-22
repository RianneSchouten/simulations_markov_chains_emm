library(ggplot2)
library(readxl)
library(tidyverse)

setwd("C:/Users/20200059/Documents/Github/simulations_beam_search_markov_chain/figures/")
#data <- read_excel("../data_output/experiment_initialprobs_20200608_10nreps_[100, 1000]_[2, 5, 25]_[2, 5, 25]_[2, 5, 25].xlsx")

data <- read_excel("../data_output/experiment_initialprobs_20200619_50nreps_[100, 1000]_[2, 5, 25]_[2, 5, 25]_[2, 5, 10, 25].xlsx")
head(data)
names(data)

long_data <- data %>%
  rename(delta_tv = deltatv,
         omega_tv = omegatv,
         phi_wd = phiwd, 
         phi_kl = phikl,
         phi_bic = phibic, 
         phi_arl = phiarl, 
         phi_warl = phiwarl) %>%
  pivot_longer(
    cols = c('delta_tv', 'omega_tv', 'phi_wd', 'phi_kl', 'phi_bic', 'phi_arl', 'phi_warl'),
    names_to = "measure",
    values_to = "Rank") %>%
  mutate(facet = case_when(distAyn == 0 & distPiyn == 0 ~ 'No difference',
                           distAyn == 1 & distPiyn == 0 ~ 'Difference in transition matrix A',
                           distAyn == 0 & distPiyn == 1 ~ 'Difference in initial probabilities pi',
                           distAyn == 1 & distPiyn == 1 ~ 'Difference in both A and pi')) %>%
  mutate(facet = factor(facet, levels = c('No difference', 'Difference in transition matrix A', 
                                          'Difference in initial probabilities pi', 'Difference in both A and pi'))) %>%
  mutate(measure = factor(measure, levels = c('phi_warl', 'phi_arl', 'phi_bic', 'phi_kl', 
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



