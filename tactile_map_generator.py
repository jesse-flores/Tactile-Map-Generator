import osmnx as ox
from shapely.geometry import Polygon, LineString, MultiPolygon
from shapely.ops import unary_union
from shapely import simplify
import trimesh
import numpy as np
import argparse
import geopandas as gpd

# Configure OSMnx
ox.settings.log_console = False # Enable console logging
# ox.settings.log_file = "osm_log.txt"  # Log file for OSMnx
# ox.settings.log_file_level = "DEBUG"  # Log level for OSMnx
ox.settings.use_cache = True
ox.settings.timeout = 300  # Increase timeout for large areas

#optional library for debugging
# def debug_geometry(geom, name):
#     """Print detailed geometry information"""
#     print(f"\nDEBUG {name}:")
#     print(f"Type: {type(geom)}")
#     if hasattr(geom, 'is_empty'):
#         print(f"Empty: {geom.is_empty}")
#     if hasattr(geom, 'is_valid'):
#         print(f"Valid: {geom.is_valid}")
#     if hasattr(geom, 'area'):
#         print(f"Area: {geom.area:.1f} m²")
#     if hasattr(geom, 'length'):
#         print(f"Length: {geom.length:.1f} m")

def fetch_map_data(place_name):
    """Fetch building and walkable paths"""
    print(f"\nFETCHING DATA FOR: {place_name}")
    try:
        # Get area boundary (without buffer_dist)
        area = ox.geocode_to_gdf(place_name).geometry.iloc[0]
        # debug_geometry(area, "Original Area")
        
        # Create a buffered area for queries
        buffered_area = area.buffer(0.001)  # ~100m buffer in degrees
        # debug_geometry(buffered_area, "Buffered Area")
        
        # Get UTM CRS
        centroid = area.centroid
        utm_zone = int((centroid.x + 180)/6) + 1
        utm_crs = f"EPSG:326{utm_zone}" if centroid.y >= 0 else f"EPSG:327{utm_zone}"
        # print(f"Using UTM CRS: {utm_crs}")
        
        # Fetch data
        print("\nFetching buildings...")
        buildings = ox.features_from_polygon(buffered_area, tags={"building": True})
        if len(buildings) > 0:
            buildings = buildings.to_crs(utm_crs)
            # debug_geometry(buildings.geometry.iloc[0], "First Building")
        
        print("\nFetching walkways...")
        graph = ox.graph_from_polygon(buffered_area, network_type="walk")
        graph_proj = ox.project_graph(graph, to_crs=utm_crs)
        
        return buildings, graph_proj
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        return None, None

def process_geometries(buildings, graph):
    """Process geometries with validation"""
    print("\nPROCESSING GEOMETRIES")
    
    # Buildings processing
    if len(buildings) == 0:
        print("Using fallback building (20x20m)")
        building_poly = Polygon([(0,0), (20,0), (20,20), (0,20)])
    else:
        # Combine all buildings
        all_buildings = unary_union(buildings.geometry)
        if isinstance(all_buildings, MultiPolygon):
            building_poly = max(all_buildings.geoms, key=lambda p: p.area)
        else:
            building_poly = all_buildings
        
        # Clean geometry
        if not building_poly.is_valid:
            building_poly = building_poly.buffer(0)
        building_poly = simplify(building_poly, tolerance=2.0)
    
    # debug_geometry(building_poly, "Final Building")
    
    # Paths processing
    paths = []
    if graph is not None:
        edges = ox.graph_to_gdfs(graph, nodes=False)
        for _, edge in edges.iterrows():
            if isinstance(edge.geometry, LineString) and len(edge.geometry.coords) >= 2:
                path = simplify(edge.geometry, tolerance=1.0)
                if path.is_valid:
                    paths.append(path)
    
    if len(paths) == 0:
        print("Using fallback path")
        paths = [LineString([(5,5), (15,15)])]
    
    print(f"Found {len(paths)} valid paths")
    # if len(paths) > 0:
        # debug_geometry(paths[0], "First Path")
    
    return building_poly, paths

def generate_3d_model(building_poly, paths, output_file):
    """Generate 3D model with validation"""
    print("\nGENERATING 3D MODEL")
    
    # Create building mesh (10m tall)
    try:
        print("Creating building mesh...")
        building_mesh = trimesh.creation.extrude_polygon(building_poly, height=10)
        # print(f"Building mesh bounds: {building_mesh.bounds}")
    except Exception as e:
        # print(f"Building mesh failed: {e}. Using fallback.")
        building_mesh = trimesh.creation.box((20, 20, 10))
    
    # Create path meshes (0.3m tall, 1m wide)
    path_meshes = []
    for i, path in enumerate(paths):
        try:
            path_2d = path.buffer(0.5)  # 1m total width
            path_mesh = trimesh.creation.extrude_polygon(path_2d, height=0.3)
            path_meshes.append(path_mesh)
            print(f"Path {i} bounds: {path_mesh.bounds}")
        except Exception as e:
            print(f"Path {i} failed: {e}")
    
    # Combine all meshes
    if path_meshes:
        combined_mesh = trimesh.util.concatenate([building_mesh] + path_meshes)
    else:
        combined_mesh = building_mesh
    
    # Validate final mesh
    if combined_mesh.is_empty:
        raise ValueError("Final mesh is empty!")
    
    # print(f"\nFINAL MESH:")
    # print(f"Bounds: {combined_mesh.bounds}")
    # print(f"Volume: {combined_mesh.volume:.1f} m³")
    
    # Center and export
    combined_mesh.apply_translation(-combined_mesh.centroid)
    combined_mesh.export(output_file)
    print(f"\nSAVED: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate tactile maps from OSM data")
    parser.add_argument("place", help="Location name/address")
    parser.add_argument("--output", default="map.stl", help="Output STL file")
    args = parser.parse_args()

    print("\n" + "="*50)
    print(f"TACTILE MAP GENERATOR - {args.place}")
    print("="*50)
    
    # Fetch and process data
    buildings, graph = fetch_map_data(args.place)
    if buildings is None or graph is None:
        print("\nFAILED: Could not fetch map data")
        return
    
    building_poly, paths = process_geometries(buildings, graph)
    
    # Generate 3D model
    try:
        generate_3d_model(building_poly, paths, args.output)
        print("\nSUCCESS: Map generated")
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    main()