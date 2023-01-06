from numpy import float64
from pyproj import CRS
import pyproj
from math import dist
import requests
import warnings
warnings.filterwarnings("ignore")


class descarga_dist_btw_points:
  #conductor
    def __init__(self,api_key = "", id_from= "" ,  from_school_long=None,
                 from_school_lat =None , id_to= "",  to_school_long=None, to_school_lat=None ):  
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
        try:
          self.geojson = '{"type":"LineString",' + self.printer_.split(',"geometry":{')[1].split(',"type":"LineString"}}]')[0] + '}'
          break
        except IndexError:
          print('its getting again the geojson')

      self.end_point = self.geojson.split(',[')[-1].split(']')[0] 
      self.distancia  = self.printer_.split('"properties":{"segments":[{"')[1].split(',"steps":[{')[0].split('distance":')[1].split(',')[0]
      self.duracion = self.printer_.split('"summary":{')[1].split(',"duration":')[1].split('}')[0]
      
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
           "json": str(self.data_school[9]) 
           }, 
          ]

      errors = bq_client.insert_rows_json(self.table_id, self.rows_to_insert)  # Make an API request.
      if errors == []:
          print("New rows have been added.")
      else:
          print("Encountered errors while inserting rows: {}".format(errors))
      return errors 

