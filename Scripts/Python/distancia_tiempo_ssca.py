from numpy import float64
from pyproj import CRS
import pyproj
from math import dist
import requests
import warnings
warnings.filterwarnings("ignore")
import time

def consulta_etc_iteracion(etc):
  SQL  = """ WITH OUTPUT_COSTO_TRANSPORTE AS (SELECT 
            Cod_ETC,
            codigo_dane,
            COD_COL,
            codigo_dane_sede,
            cons_sede,
            tipo_jornada,
            Divipola_MUNICIPIO ,
            LATITUD,
            LONGITUD,
            GEOMETRY,
            LATITUD LAT_ORIGEN,
            LONGITUD 	LONG_ORIGEN	,
            codigo_dane_sede ID_ORIGEN,
            Cod_ETC ETC,
              FROM `ph-jabri.WorldBank.costo_transporte`
            LEFT JOIN `ph-jabri.WorldBank.sedes_dane`
            ON  CAST(COD_COL AS INT64) = CAST(codigo_dane_sede AS INT64)
            ),
BASE_GEOREF AS (
  SELECT * FROM (SELECT
                        CASE WHEN SAFE_CAST(LAT_ORIGEN AS FLOAT64) = 0.0 THEN NULL ELSE SAFE_CAST(LAT_ORIGEN AS FLOAT64) END LAT_ORIGEN,
                        SAFE_CAST(LONG_ORIGEN AS FLOAT64) LONG_ORIGEN, 
                        ID_ORIGEN,
                      ETC
                      FROM OUTPUT_COSTO_TRANSPORTE
                      )
UNION ALL
 SELECT 
 SAFE_CAST(LAT_ORIGEN AS FLOAT64) LAT_ORIGEN,
 SAFE_CAST(LONG_ORIGEN AS FLOAT64) LONG_ORIGEN,
 ID_ORIGEN, ETC
  FROM ph-jabri.WorldBank.ETC_center
),
BASE AS (SELECT DISTINCT *   FROM BASE_GEOREF WHERE ETC = '{}'),
 TABLA AS (
          SELECT 
          LAT_ORIGEN,	LONG_ORIGEN,	CAST(ID_ORIGEN AS STRING) ID_ORIGEN,	
          LAT_DEST,	LONG_DEST, CAST(ID_DEST AS STRING)	ID_DEST, ETC	
          FROM  (SELECT  LAT_ORIGEN  , LONG_ORIGEN , ID_ORIGEN , ETC   FROM BASE  )  A
          INNER JOIN (SELECT  LAT_ORIGEN LAT_DEST, LONG_ORIGEN LONG_DEST, ID_ORIGEN ID_DEST, ETC ETC_1 FROM BASE) B
          ON 1 =1
			)
SELECT * FROM TABLA WHERE LAT_ORIGEN IS NOT NULL AND LONG_DEST IS NOT NULL
""".format(etc)

class descarga_dist_btw_points:
  #conductor
    def __init__(self,api_key = "", id_from= "" ,  from_school_long=None,
                 from_school_lat =None , id_to= "", 
		 to_school_long=None, to_school_lat=None, ETC = "" ):  
      self.api_key = api_key
      self.id_from = id_from
      self.from_school_long = from_school_long
      self.from_school_lat = from_school_lat 
      self.id_to = id_to
      self.to_school_long = to_school_long
      self.to_school_lat = to_school_lat
      self.project = 'ph-jabri'
      self.Dataset = 'WorldBank'
      self.Tabla = 'directions'
      self.ETC = ETC
      self.timeout = time.time() + 10   # 10 seconds from now

    def elevation_points(self):
      headers = {
              'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
              'Authorization': '5b3ce3597851110001cf62485acad92faea94c36971be035ed8b266d',
              'Content-Type': 'application/json; charset=utf-8'
              }
      body_from = {"format_in":"point","geometry":[self.from_school_long, self.from_school_lat]}
      body_to   = {"format_in":"point","geometry":[self.to_school_long, self.to_school_lat]}
      
      call_from = requests.post('https://api.openrouteservice.org/elevation/point', json=body_from, headers=headers)
      call_to = requests.post('https://api.openrouteservice.org/elevation/point', json=body_to, headers=headers)
      # print(call.status_code, call.reason)
      elevation_from  = call_from.text.split('"geometry":{"coordinates":')[1].split(']')[0].split(',')[-1]
      elevation_to  = call_to.text.split('"geometry":{"coordinates":')[1].split(']')[0].split(',')[-1]
      return [elevation_from, elevation_to]
 


    def cole_data(self):
      headers = {
          'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
      }
      str_osv  = 'https://api.openrouteservice.org/v2/directions/driving-car?api_key={}&start={},{}&end={},{}'
      str_osv  = str_osv.format(str(self.api_key), 
                                          str(self.from_school_long), 
                                          str(self.from_school_lat ),
                                          str(self.to_school_long), 
                                          str(self.to_school_lat)) 
      
      call = requests.get( str_osv , headers=headers)
      # print(call.status_code, call.reason)
      self.printer_ = call.text 
      self.origen = str(self.from_school_long) + ',' +  str(self.from_school_lat) 
      self.desti = str(self.to_school_long)+ ',' +  str(self.to_school_lat)
      while True:
        test = 0
        if test == 10 or time.time() > self.timeout:
          try:
            self.gjson = '{"type":"LineString",' + self.printer_.split(',"geometry":{')[1].split(',"type":"LineString"}}]')[0] + '}'
            break
          except IndexError:
            print('its getting again the geojson')


      self.ep = self.gjson.split(',[')[-1].split(']')[0]
      if '[[' in self.ep:
        self.end_point = self.ep.split('[[')[-1]
        self.geojson = self.gjson.replace('LineString', 'Point').replace('[[', '[').replace(']]', ']')
      else:
        self.end_point = self.gjson.split(',[')[-1].split(']')[0]
        self.geojson = self.gjson

      # self.end_point = self.geojson.split(',[')[-1].split(']')[0] 
      self.distancia  = self.printer_.split('"properties":{"segments":[{"')[1].split(',"steps":[{')[0].split('distance":')[1].split(',')[0]
      try:
        self.duracion = self.printer_.split('"summary":{')[1].split(',"duration":')[1].split('}')[0]
      except IndexError:
        self.duracion = '0'
      
        #  #################
  # 
      self.long_dest = float64(self.desti.split(',')[0])
      self.lat_dest = float64(self.desti.split(',')[-1])

      self.long_ep = float64(self.end_point.split(',')[0])
      self.lat_ep = float64(self.end_point.split(',')[-1])
      
      proj_4326 = CRS("EPSG:4326")
      proj_3035 = CRS("EPSG:3035")
      

      x1, y1 = pyproj.transform(proj_4326, proj_3035, self.long_dest, self.lat_dest)
      x2, y2 = pyproj.transform(proj_4326, proj_3035, self.long_ep, self.lat_ep)

      Punto1 = (x1, y1 )
      Punto2 = (x2, y2)
     
      self.dist_desti_epd = dist(Punto1, Punto2)
  #   duracion, distancia_end_point_destino, , id_to,  desti  , end_point , distancia  , geojson

      return [self.id_from , self.origen, self.id_to, self.desti, self.end_point, 
              self.distancia,self.duracion,self.dist_desti_epd,  self.geojson , self.printer_ ]

######################################################
    def streaming_load_bq(self):
      self.data_school = self.cole_data()
      self.elevation = self.elevation_points()
      self.table_id = '{}.{}.{}'.format(self.project, self.Dataset, self.Tabla)
      self.rows_to_insert = [
          {"id_origen": str(self.data_school[0]), 
           "long_lat_origen": str(self.data_school[1]), 
           "elevacion_origen" : str(self.elevation[0]), 

           "id_destino": str(self.data_school[2]), 
           "long_lat_destino": str(self.data_school[3]), 
            "elevacion_destino" : str(self.elevation[1]), 
           
           "end_point_route": str(self.data_school[4]), 
           "distancia": str(self.data_school[5]), 
            "duracion": str(self.data_school[6]), 
           "distancia_destino_end_point": str(self.data_school[7]), 
            "geojson_text": str(self.data_school[8]) ,
           "json": str(self.data_school[9]) ,
           "ETC": str(self.ETC )
	
           }, 
          ]

      errors = bq_client.insert_rows_json(self.table_id, self.rows_to_insert)  # Make an API request.
      if errors == []:
          pass #print("New rows have been added.")
      else:
          print("Encountered errors while inserting rows: {}".format(errors))
      return errors 

# api_key  = key[1]
# from_school_long, from_school_lat = -74.373649 , 4.334448
# to_school_long, to_school_lat = -74.390736 , 4.395070

# a = descarga_dist_btw_points(api_key = api_key, id_from= '', 
# from_school_long = from_school_long, id_to= '', 
# from_school_lat = from_school_lat , to_school_long=   to_school_long, to_school_lat =  to_school_lat)
# a.streaming_load_bq()
