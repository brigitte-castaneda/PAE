library(readxl)
#load("C:/Users/USER/Desktop/DID roads/did_roads/did_roads.RData")
package_list = c('readr','readxl','sqldf','plyr', 
          'did' , 'arrow',  'plyr', 'ggplot2',
          'dplyr','fixest' , 'gargle' , 'stringr'
          #, 'bigrquery' 
)
for (i in 1:length(package_list) ) {
  if(package_list[i] %in% rownames(installed.packages()) == FALSE) {
    install.packages(package_list[i])
  }
  lapply(package_list[i], library, character.only = TRUE)
}

FOCALIZACION_PAE <- read_excel("inputs/FOCALIZACION PAE NOVIEMBRE_SEGMENTO 1.xlsx")

# sedes de cada ETC
RUTAS_IMPORT <- read_excel("inputs/RUTAS IMPORT.xlsx", 
                           col_types = c("text", "text", "numeric", 
                                         "numeric"))


library(readr)
sedes_dane_georef <- read_csv("inputs/sedes_dane_georef.csv", 
                              col_types = cols(COD_COL = col_character(), 
                                               COD_INST = col_character(), CODIGO_DEPARTAMENTO = col_character(), 
                                               LATITUD = col_double()))

