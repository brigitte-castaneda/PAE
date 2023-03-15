library(readr)
base <- read_csv("Input Data/base.csv", col_types = cols(COD_COL = col_character()))
base$frac_stu_trabaja = base$FAC_EXP_ESTU_TRABAJA /base$FAC_EXP
install.packages(  "stargazer")
library(stargazer)

Number_students = (lm(data=subset(base, base$TIME_TO_TREAT >= 7), 
           FAC_EXP ~ factor(TREAT_)*factor(TIME_TO_TREAT) ) )

Number_students_working = (lm(data=subset(base, base$TIME_TO_TREAT >= 7), 
           FAC_EXP_ESTU_TRABAJA ~ factor(TREAT_)*factor(TIME_TO_TREAT) ) )

frac_students_working = (lm(data=subset(base, base$TIME_TO_TREAT >= 7), 
           frac_stu_trabaja ~ factor(TREAT_)*factor(TIME_TO_TREAT) ) )


math_result = (lm(data=subset(base, base$TIME_TO_TREAT >= 7), 
           MEDIAN_MATH_S_c ~ factor(TREAT_)*factor(TIME_TO_TREAT) ) )

reading_result = (lm(data=subset(base, base$TIME_TO_TREAT >= 7), 
                     MEDIAN_READING_LITERACY_S_c ~ factor(TREAT_)*factor(TIME_TO_TREAT) ) )


stargazer::stargazer(Number_students, frac_students_working,
                     math_result, reading_result)



Number_students = (lm(data=subset(base, base$TIME_TO_TREAT == 7), 
                      FAC_EXP ~ factor(TREAT_) ) )

Number_students_working = (lm(data=subset(base, base$TIME_TO_TREAT == 7), 
                              FAC_EXP_ESTU_TRABAJA ~ factor(TREAT_) ) )

frac_students_working = (lm(data=subset(base, base$TIME_TO_TREAT == 7), 
                            frac_stu_trabaja ~ factor(TREAT_) ) )


math_result = (lm(data=subset(base, base$TIME_TO_TREAT == 7), 
                  MEDIAN_MATH_S_c ~ factor(TREAT_)) )

reading_result = (lm(data=subset(base, base$TIME_TO_TREAT == 7), 
                     MEDIAN_READING_LITERACY_S_c ~ factor(TREAT_) ) )


stargazer::stargazer(Number_students, frac_students_working,
                     math_result, reading_result)

summary(lm(data=base,  MEDIAN_READING_LITERACY_S_c ~ factor(TREAT_)*factor(TIME_TO_TREAT)) )
###########################3

base$TREAT_ = factor(base$TREAT_)
math_result_1 = lm(data=subset(base, base$TIME_TO_TREAT == 1), 
                  MEDIAN_MATH_S_c ~ TREAT_  )

math_result_2 = lm(data=subset(base, base$TIME_TO_TREAT == 2), 
                   MEDIAN_MATH_S_c ~ TREAT_  )

math_result_3 = lm(data=subset(base, base$TIME_TO_TREAT == 3), 
                   MEDIAN_MATH_S_c ~ TREAT_  )

math_result_4 = lm(data=subset(base, base$TIME_TO_TREAT == 4), 
                   MEDIAN_MATH_S_c ~ TREAT_  )

math_result_5 = lm(data=subset(base, base$TIME_TO_TREAT == 5), 
                   MEDIAN_MATH_S_c ~ TREAT_  )

math_result_6 = lm(data=subset(base, base$TIME_TO_TREAT == 6), 
                   MEDIAN_MATH_S_c ~ TREAT_  )

math_result_7 = lm(data=subset(base, base$TIME_TO_TREAT == 7), 
                   MEDIAN_MATH_S_c ~ TREAT_  )

math_result_8 = lm(data=subset(base, base$TIME_TO_TREAT == 8), 
                   MEDIAN_MATH_S_c ~ TREAT_  )

math_result_10 = lm(data=subset(base, base$TIME_TO_TREAT == 10), 
                   MEDIAN_MATH_S_c ~ TREAT_  )

math_result_12 = lm(data=subset(base, base$TIME_TO_TREAT == 12), 
                   MEDIAN_MATH_S_c ~ TREAT_  )

math_result_14 = lm(data=subset(base, base$TIME_TO_TREAT == 14), 
                   MEDIAN_MATH_S_c ~ TREAT_  )
math_result_16 = lm(data=subset(base, base$TIME_TO_TREAT == 16), 
                    MEDIAN_MATH_S_c ~ TREAT_  )

stargazer::stargazer(math_result_2, math_result_4,
                     math_result_6,math_result_8 )

stargazer::stargazer(math_result_10,
                     math_result_12,math_result_14, math_result_16 )


library(fixest)
str(base$treat)
base$time_to_treat = base$TIME_TO_TREAT
base$treat = ifelse(base$TREAT_ =='0', 0, 1)
colnames(base)
mod_twfe = feols(MEDIAN_MATH_S_c ~ i(time_to_treat, treat, ref = -1)  #+ ## Our key interaction: time × treatment status
                   # pcinc + asmrh + cases |                    ## Other controls
                 |  
                 COD_COL + ANIO_OBSERV,                             ## FEs
                 cluster = ~COD_COL,                          ## Clustered SEs
                 data = subset(base, base$time_to_treat >=-5))
etable(mod_twfe)
base$year_treated = ifelse(base$treat==0,1000,base$ANIO_FIRMA )
iplot(mod_twfe, 
      xlab = 'Time to treatment',
      main = 'Event study: Staggered treatment (TWFE)')
head(base)
base$year = base$ANIO_OBSERV
mod_sa = feols(MEDIAN_MATH_S_c ~ sunab(year_treated, year)#+ ## Our key interaction: time × treatment status
               # pcinc + asmrh + cases |                    ## Other controls
               |  
                 COD_COL + ANIO_OBSERV,                             ## FEs
               cluster = ~COD_COL,                          ## Clustered SEs
               data = subset(base, base$time_to_treat >=-5) )
iplot(list(mod_twfe, mod_sa), sep = 0.5, ref.line = -1,
      xlab = 'Time to treatment',
      main = 'Event study: Staggered treatment')
legend("topright", col = c(1, 2), pch = c(20, 17), 
       legend = c("TWFE", "Sun & Abraham (2020)"))

iplot(mod_sa , ref.line = -1,
      xlab = 'Time to treatment',
      main = 'Event study: Staggered treatment')


#################################
library(readr)
capacidad_MAEM <- read_csv("C:/Users/USER/Downloads/capacidad_MAEM_update.csv", 
                           col_types = cols(...1 = col_skip(), Divipola_MUNICIPIO = col_character(), 
                                            codigodanesedeeducativa = col_character(), 
                                            Cod_ETC = col_character()), locale = locale(encoding = "ISO-8859-1"))


arrow::write_parquet(capacidad_MAEM, 'capacidad_MAEM.parquet' )


capacidad_MAER <- read_csv("C:/Users/USER/Downloads/capacidad_MAER_update.csv", 
                           col_types = cols(...1 = col_skip(), Divipola_MUNICIPIO = col_character(), 
                                            codigodanesedeeducativa = col_character(), 
                                            Cod_ETC = col_character()), locale = locale(encoding = "ISO-8859-1"))


arrow::write_parquet(capacidad_MAER, 'capacidad_MAER.parquet' )

getwd()
mean(capacidad_MAEM$p_week_1_class_1_ton)





premium_MAER <- read_csv("C:/Users/USER/Downloads/premium_MAER_1.csv", 
                           col_types = cols(...1 = col_skip(), Divipola_MUNICIPIO = col_character(), 
                                            codigodanesedeeducativa = col_character(), 
                                            Cod_ETC = col_character()), locale = locale(encoding = "ISO-8859-1"))
columnas = c("premium_1", "premium_2", "premium_3", "premium_4", "premium_5")

min_values <- apply(premium_MAER[, c("premium_6", "premium_2", "premium_3", "premium_4", "premium_5")], 1, min)
max_values <- apply(premium_MAER[, c("premium_6", "premium_2", "premium_3", "premium_4", "premium_5")], 1, max)
mean_values <- apply(premium_MAER[, c( "premium_2", "premium_3", "premium_4", "premium_5")], 1,  sum)
premium_MAER$min_values <- min_values
premium_MAER$max_values <- max_values
premium_MAER$mean_values <- ( as.numeric(premium_MAER$min_values) + as.numeric(premium_MAER$max_values)  ) / 2

premium_MAEM <- read_csv("C:/Users/USER/Downloads/premium_temp_TON_KM.xlsx", 
                         col_types = cols(...1 = col_skip(), Divipola_MUNICIPIO = col_character(), 
                                          codigodanesedeeducativa = col_character(), 
                                          Cod_ETC = col_character()), locale = locale(encoding = "ISO-8859-1"))
if(1==1){
library(readxl)
premium_MAEM <- read_excel("C:/Users/USER/Downloads/premium_temp_TON_KM.xlsx")
premium_MAEM$cod_etc  = ifelse(premium_MAEM$ETC_ ==  'CORDOBA', '23000' , NaN)
premium_MAEM$cod_etc= ifelse(premium_MAEM$ETC_ ==  'HUILA', '41000' , premium_MAEM$cod_etc)
premium_MAEM$cod_etc= ifelse(premium_MAEM$ETC_ ==  'NARIÑO', '52000' , premium_MAEM$cod_etc)

min_values <- apply(premium_MAEM[, c("premium_1", "premium_2", "premium_3", "premium_4", "premium_5")], 1, min)
max_values <- apply(premium_MAEM[, c("premium_1", "premium_2", "premium_3", "premium_4", "premium_5")], 1, max)
mean_values <- apply(premium_MAEM[, c("premium_1", "premium_2", "premium_3", "premium_4", "premium_5")], 1, function(x) mean(x, na.rm = TRUE))
premium_MAEM$min_values<- min_values
premium_MAEM$max_values <- max_values
premium_MAEM$mean_values <- mean_values #/5 #(premium_MAEM$min_values + premium_MAEM$max_values) / 2
arrow::write_parquet(premium_MAEM, 'premium_MAEM.parquet' )
}

if(1==1){
  library(readr)
  library(readr)
  premium_MAEM <- read_delim("C:/Users/USER/Downloads/premium_MAER_TON_KM.csv", 
                                    delim = ";", escape_double = FALSE, col_types = cols(...1 = col_skip(), 
                                                                                         Divipola_MUNICIPIO = col_character()), 
                                    locale = locale(encoding = "ISO-8859-1"), 
                                    trim_ws = TRUE)
  premium_MAEM$cod_etc  = ifelse(premium_MAEM$ETC ==  'CORDOBA', '23000' , NaN)
  premium_MAEM$cod_etc= ifelse(premium_MAEM$ETC ==  'HUILA', '41000' , premium_MAEM$cod_etc)
  premium_MAEM$cod_etc= ifelse(premium_MAEM$ETC ==  'NARIÑO', '52000' , premium_MAEM$cod_etc)
  
  min_values <- apply(premium_MAEM[, c("premium_1", "premium_2", "premium_3", "premium_4", "premium_5")], 1, min)
  max_values <- apply(premium_MAEM[, c("premium_1", "premium_2", "premium_3", "premium_4", "premium_5")], 1, max)
  mean_values <- apply(premium_MAEM[, c("premium_1", "premium_2", "premium_3", "premium_4", "premium_5")], 1, function(x) mean(x, na.rm = TRUE))
  premium_MAEM$min_values<- min_values
  premium_MAEM$max_values <- max_values
  premium_MAEM$mean_values <- mean_values #/5 #(premium_MAEM$min_values + premium_MAEM$max_values) / 2
  arrow::write_parquet(premium_MAEM, 'premium_MAER.parquet' )
}
getwd()
