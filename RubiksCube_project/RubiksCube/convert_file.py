#!/usr/bin/env python3

import re

def convert_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Function to convert drawPolygon calls
    def convert_draw_polygon(match):
        # Extract the full match including coordinates and fill
        full_match = match.group(0)
        coords_part = match.group(1)
        fill_part = match.group(2)
        
        # Split coordinates by comma and strip whitespace
        coords = [c.strip() for c in coords_part.split(',')]
        
        # Group coordinates into (x,y) pairs and double them
        doubled_coords = []
        for i in range(0, len(coords), 2):
            if i+1 < len(coords):
                x_coord = coords[i]
                y_coord = coords[i+1]
                
                # Double all numeric values in the coordinate expressions
                x_doubled = re.sub(r'\b(\d+)\b', lambda m: str(int(m.group(1)) * 2), x_coord)
                y_doubled = re.sub(r'\b(\d+)\b', lambda m: str(int(m.group(1)) * 2), y_coord)
                
                doubled_coords.append(f"({x_doubled}, {y_doubled})")
        
        # Join the doubled coordinates
        coord_string = ", ".join(doubled_coords)
        
        return f"draw.polygon([{coord_string}], {fill_part}"
    
    # Convert drawPolygon calls to draw.polygon with doubled coordinates
    # Pattern matches the entire drawPolygon call including fill
    pattern = r'drawPolygon\(([^)]+)\), (fill = [^)]+)\)'
    content = re.sub(pattern, convert_draw_polygon, content)
    
    # Also update function signatures to include 'draw' parameter
    content = re.sub(r'def (draw\w+)\(app\):', r'def \1(draw, app):', content)
    
    # Write back the converted content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Conversion completed for {filename}")

if __name__ == "__main__":
    convert_file("__init__.py")
