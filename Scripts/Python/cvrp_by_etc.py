import pip
import os
import sys
import argparse
import pandas as pd
import numpy as np
    
etc = 41000
def inicializacion_MAER(etc):
  
  sql = """
  select *   from `ph-jabri.WorldBank.distacias_etc_{}`
  WHERE ID_ORIGEN  IN (
    SELECT '0'
    UNION ALL
    SELECT codigodanesedeeducativa FROM 
    `ph-jabri.WorldBank_raw.capacidad_MAER`)
    AND 
  ID_DEST  IN (
    SELECT '0'
    UNION ALL
    SELECT codigodanesedeeducativa FROM 
    `ph-jabri.WorldBank_raw.capacidad_MAER`)

  """
  df = bq_client.query(sql.format(etc)).to_dataframe() 
  # df.head(3)
  columnas = ['ELEVACION_ORIGEN','ELEVACION_DESTINO', 'ELEVATION_GAIN', 'distance', 'duracion_real' , 'distance_real' ]
  lista = []
  for i in columnas:
    df[i] = pd. to_numeric(df[i]) 
    var_interes =  i
    temp = df[['ID_ORIGEN','ID_DEST', var_interes ]].pivot_table( values=var_interes, index=['ID_ORIGEN'],
                      columns=['ID_DEST'], aggfunc=np.sum)
    escuelas = temp.index.values 
    temp = temp.to_numpy()
    lista.append(temp)        

  #Las cargas por semana, estaran dadas por:

  sql_ = """
  SELECT cod_sede, ifnull(termoking_w{}_ton ,  0 ) termoking_w{}_ton ,
                    ifnull( furgon_c2_w{}_ton , 0 )  furgon_c2_w{}_ton  ,
                    ifnull( furgon_c3_w{}_ton , 0 ) furgon_c3_w{}_ton 
      FROM(
                SELECT 
                cod_sede,
                SUM(termoking_w1_ton) termoking_w1_ton,
                SUM(furgon_c2_w1_ton) furgon_c2_w1_ton, SUM(furgon_c3_w1_ton) furgon_c3_w1_ton,

--                SUM(termoking_w2_ton) termoking_w2_ton,
--                SUM(furgon_c2_w2_ton) furgon_c2_w2_ton, SUM(furgon_c3_w2_ton) furgon_c3_w2_ton,
--                
--                SUM(termoking_w3_ton) termoking_w3_ton,
--                SUM(furgon_c2_w3_ton) furgon_c2_w3_ton, SUM(furgon_c3_w3_ton) furgon_c3_w3_ton,
--                
--                SUM(termoking_w4_ton) termoking_w4_ton,
--                SUM(furgon_c2_w4_ton) furgon_c2_w4_ton, SUM(furgon_c3_w4_ton) furgon_c3_w4_ton, 
                FROM (
                      SELECT 
                      codigodanesedeeducativa cod_sede, Cod_ETC ,
                      p_week_1_class_1_ton as termoking_w1_ton,
                      p_week_1_class_2_ton  as furgon_c2_w1_ton ,  p_week_1_class_3_ton as furgon_c3_w1_ton,

--                      p_week_2_class_1_ton  as termoking_w2_ton, 
--                      p_week_2_class_2_ton as furgon_c2_w2_ton,    p_week_2_class_3_ton as furgon_c3_w2_ton , 
--                      
--                      p_week_3_class_1_ton  as termoking_w3_ton ,
--                      p_week_3_class_2_ton as furgon_c2_w3_ton,    p_week_3_class_3_ton as furgon_c3_w3_ton ,
--                      
--                      p_week_4_class_1_ton  as termoking_w4_ton,
--                      p_week_4_class_2_ton as furgon_c2_w4_ton,    p_week_4_class_3_ton as furgon_c3_w4_ton,
                      
                      FROM `ph-jabri.WorldBank_raw.capacidad_MAEM`

                )
  where Cod_ETC = '{}'
  GROUP BY 1
  order by 1
  )"""
  return [lista, escuelas, sql_ ] 

def inicializacion_MAEM(etc):
  
  sql = """
  select *   from `ph-jabri.WorldBank.distacias_etc_{}`
  WHERE ID_ORIGEN  IN (
    SELECT '0'
    UNION ALL
    SELECT codigodanesedeeducativa FROM 
    `ph-jabri.WorldBank_raw.capacidad_MAEM`)
    AND 
  ID_DEST  IN (
    SELECT '0'
    UNION ALL
    SELECT codigodanesedeeducativa FROM 
    `ph-jabri.WorldBank_raw.capacidad_MAEM`)

  """
  df = bq_client.query(sql.format(etc)).to_dataframe() 
  # df.head(3)
  columnas = ['ELEVACION_ORIGEN','ELEVACION_DESTINO', 'ELEVATION_GAIN', 'distance', 'duracion_real' , 'distance_real' ]
  lista = []
  for i in columnas:
    df[i] = pd. to_numeric(df[i]) 
    var_interes =  i
    temp = df[['ID_ORIGEN','ID_DEST', var_interes ]].pivot_table( values=var_interes, index=['ID_ORIGEN'],
                      columns=['ID_DEST'], aggfunc=np.sum)
    escuelas = temp.index.values 
    temp = temp.to_numpy()
    lista.append(temp)        

  #Las cargas por semana, estaran dadas por:

  sql_ = """
  SELECT cod_sede, ifnull(termoking_w{}_ton ,  0 ) termoking_w{}_ton ,
                    ifnull( furgon_c2_w{}_ton , 0 )  furgon_c2_w{}_ton  ,
                    ifnull( furgon_c3_w{}_ton , 0 ) furgon_c3_w{}_ton 
      FROM(
                SELECT 
                cod_sede,
                SUM(termoking_w1_ton) termoking_w1_ton,
                SUM(furgon_c2_w1_ton) furgon_c2_w1_ton, SUM(furgon_c3_w1_ton) furgon_c3_w1_ton,

                SUM(termoking_w2_ton) termoking_w2_ton,
                SUM(furgon_c2_w2_ton) furgon_c2_w2_ton, SUM(furgon_c3_w2_ton) furgon_c3_w2_ton,
                
                SUM(termoking_w3_ton) termoking_w3_ton,
                SUM(furgon_c2_w3_ton) furgon_c2_w3_ton, SUM(furgon_c3_w3_ton) furgon_c3_w3_ton,
                
                SUM(termoking_w4_ton) termoking_w4_ton,
                SUM(furgon_c2_w4_ton) furgon_c2_w4_ton, SUM(furgon_c3_w4_ton) furgon_c3_w4_ton, 
                FROM (
                      SELECT 
                      codigodanesedeeducativa cod_sede, Cod_ETC ,
                      p_week_1_class_1_ton as termoking_w1_ton,
                      p_week_1_class_2_ton  as furgon_c2_w1_ton ,  p_week_1_class_3_ton as furgon_c3_w1_ton,

                      p_week_2_class_1_ton  as termoking_w2_ton, 
                      p_week_2_class_2_ton as furgon_c2_w2_ton,    p_week_2_class_3_ton as furgon_c3_w2_ton , 
                      
                      p_week_3_class_1_ton  as termoking_w3_ton ,
                      p_week_3_class_2_ton as furgon_c2_w3_ton,    p_week_3_class_3_ton as furgon_c3_w3_ton ,
                      
                      p_week_4_class_1_ton  as termoking_w4_ton,
                      p_week_4_class_2_ton as furgon_c2_w4_ton,    p_week_4_class_3_ton as furgon_c3_w4_ton,
                      
                      FROM `ph-jabri.WorldBank_raw.capacidad_MAEM`

                )
  where Cod_ETC = '{}'
  GROUP BY 1
  order by 1
  )"""
  return [lista, escuelas, sql_ ] 

def optimize_route(df, vehicle_type, week):
    if vehicle_type =='termoking':
      demandas = df.loc[df['cod_sede'].isin(escuelas), vehicle_type.replace(' ', '_') + '_w' + str(week) + '_ton'].fillna(0).values
    else:
      demandas = df.loc[df['cod_sede'].isin(escuelas), vehicle_type.replace(' ', '_').replace('class_', 'c') + '_w' + str(week) + '_ton'].fillna(0).values
    
    Tabla = main()
    Tabla['total_load'] = Tabla.groupby('vehicle_id')['route_load'].transform('max')
    Tabla['total_distance'] = Tabla.groupby('vehicle_id')['route_distance'].transform('max')
    Tabla['total_load_frac'] = np.where(Tabla['total_load'] == 0, np.nan, Tabla['total_load'])
    Tabla['total_load_frac'] = Tabla['load'] / Tabla['total_load_frac']
    Tabla['Week'] = week
    Tabla['Tipo_Unidad'] = vehicle_type
    return Tabla
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])  


import_or_install('ortools')
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
 
def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distancia_matriz
    data['demands'] =  demandas #map(lambda v:0 if np.isnan(v) == True else v, demandas )
 
    data['vehicle_capacities'] =  [ int(10*0.70)  ] * (int(sum(data['demands'])/int(10*0.70)) + 1) # 23000 implies 0.60 , 41000 implies 0.7
    data['num_vehicles'] = len(data['vehicle_capacities'] ) 
    data['depot'] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
            
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(  index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))



def create_solution_df(data, manager, routing, solution):
    """Returns solution as a Pandas DataFrame."""
    df = pd.DataFrame(columns=["node_index", "vehicle_id", "route_load", "load" , "position", "route_distance", "route_positions"])
    
    for vehicle_id in range(data['num_vehicles']):
      # try:
          
        index = routing.Start(vehicle_id)
        route_distance = 0
        route_load = 0
        route_positions = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            route_positions.append(school[node_index])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            
            # Append row to DataFrame
            df = df.append({
                "node_index": school[node_index],
                "vehicle_id": vehicle_id,
                "route_load": route_load,
                "load": data['demands'][node_index],
                "position": len(route_positions) - 1,
                "route_distance": route_distance,
                "route_positions": route_positions
            }, ignore_index=True)
      # except AttributeError:    


    # print(df) 
    return df



def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager( len(data['distance_matrix']) ,
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback( demand_callback)
    routing.AddDimensionWithVehicleCapacity( 
                                            demand_callback_index,
                                            2,  # null capacity slack
                                            data['vehicle_capacities'] ,  # vehicle maximum capacities
                                            True,  # start cumul to zero
                                            'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    return  create_solution_df(data, manager, routing, solution)
 