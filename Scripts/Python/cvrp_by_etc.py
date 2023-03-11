import pip
import os
import sys
import argparse
import pandas as pd
import numpy as np
    

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
    data['demands'] =  demandas
    data['vehicle_capacities'] =  [ int(10*0.40)  ] * (int(sum(data['demands'])/int(10*0.40)) + 1)
    data['num_vehicles'] = len(data['vehicle_capacities'] ) 
    data['depot'] = 0
    return data


def create_solution_df(data, manager, routing, solution):
    """Returns solution as a Pandas DataFrame."""
    df = pd.DataFrame(columns=["node_index", "vehicle_id", "route_load", "load" , "position", "route_distance", "route_positions"])
    
    for vehicle_id in range(data['num_vehicles']):
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
                                            0,  # null capacity slack
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