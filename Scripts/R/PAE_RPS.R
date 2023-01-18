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



############
# Seleccionamos escuelas publicas que pertenecen a la ETC de Fusagasugá

FUSAGASUGA =  sqldf::sqldf(" SELECT * FROM (
            SELECT 
                              LATITUD, LONGITUD, 
                              IFNULL(COD_COL, COD_INST ) AS COD_INST, 
                              'FUSAGASUGA' AS ETC 
                            FROM sedes_dane_georef
             WHERE SECTOR LIKE 'OFICIAL%'
             AND NOMBRE_MUNICIPIO LIKE '%FUSAGASU%' 
             AND LONGITUD   IS NOT NULL  )
             UNION ALL
             SELECT 4.3459142 AS LATITUD, -74.3791805 AS LONGITUD,
              '0' COD_INST, 'FUSAGASUGA' AS ETC
                           ")

Correccion_cod_id = sqldf::sqldf(" SELECT distinct COD_INST as COD_COL, LONGITUD||','||LATITUD FROM  FUSAGASUGA")
write.csv2(Correccion_cod_id, 'Correccion_cod_id.csv', row.names = F)
FUSAGASUGA = sqldf("
      SELECT A.LATITUD AS LAT_ORIGEN,
             A.LONGITUD AS LONG_ORIGEN,
             A.COD_INST ID_ORIGEN, 
             B.LATITUD AS LAT_DEST,  
             B.LONGITUD AS LONG_DEST,
             B.COD_INST ID_DEST,
             A.ETC
      FROM FUSAGASUGA A
      INNER JOIN FUSAGASUGA B
      ")
getwd()
global_input = "C:/Users/USER/Desktop/WorldBank/PAE/inputs/"

write.csv(FUSAGASUGA, paste0(global_input, 'Demo_ETC_FUSAGASUGA.csv') )
(11*3000/60)/60


####################
# En esta seccion daremos un idenificador unico a cada escuela, y lo remplazaremos por el codigo sede.

library(readr)
Demo_etc_Fusagasiga_dis_tiempo <- read_csv("inputs/Demo_etc_Fusagasiga_dis_tiempo.csv", 
                                           col_types = cols(geomap = col_skip(), 
                                                            id_origen = col_character(), id_destino = col_character()))
View(Demo_etc_Fusagasiga_dis_tiempo)
data.frame(unique(Demo_etc_Fusagasiga_dis_tiempo$id_destino))
