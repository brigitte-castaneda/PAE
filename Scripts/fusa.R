########################################
##               PAE                 ##
##          Demo_fusagasuga          ##
##            (21/12/22)             ##
#######################################

# load packages
require(pacman)
p_load(tidyverse , rio , data.table , png , grid)
lista = c('readr','readxl','lubridate', 'ggplot2',
          'hrbrthemes','dplyr','plotly','tseries',
          'fUnitRoots','forecast','FitAR', 'write.xlsx', 
          'sqldf','tidyr', 'haven')

for (i in 1:length(lista) ) {
  if(lista[i] %in% rownames(installed.packages()) == FALSE) {
    install.packages(lista[i])
  }
  lapply(lista[i], library, character.only = TRUE)
  
}


getwd()
