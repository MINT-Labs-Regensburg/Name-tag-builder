#!/usr/bin/env python3
"""
Automatic Nametag STL Generator
Reads names from a CSV file and generates individual STL files using OpenSCAD
"""

import csv
import subprocess
import os
import sys
from pathlib import Path

# Configuration
OPENSCAD_TEMPLATE = "nametag.scad"
OUTPUT_DIR = "generated_nametags"
CSV_FILE = "names.csv"

# Default nametag parameters (can be overridden in CSV)
DEFAULT_PARAMS = {
    "nametag_width": 80,
    "nametag_height": 30,
    "nametag_thickness": 3,
    "text_size": 8,
    "text_height": 1.5,  # Changed from text_depth to text_height (raised text)
    "ring_width": 3,
    "ring_height": 1.2,
    "mounting_hole_diameter": 4,
    "corner_radius": 3,
}


def find_openscad():
    """Find OpenSCAD executable on the system"""
    possible_paths = [
        "openscad",  # Linux/Mac if in PATH
        "/usr/bin/openscad",  # Linux
        "/usr/local/bin/openscad",  # Linux/Mac
        "C:\\Program Files\\OpenSCAD\\openscad.exe",  # Windows
        "C:\\Program Files (x86)\\OpenSCAD\\openscad.exe",  # Windows 32-bit
        "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",  # macOS
    ]

    for path in possible_paths:
        try:
            result = subprocess.run([path, "--version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                print(f"Found OpenSCAD at: {path}")
                return path
        except (FileNotFoundError, subprocess.TimeoutExpired, PermissionError):
            continue

    return None


def create_temp_scad(name, params, temp_file):
    """Create a temporary OpenSCAD file with the given parameters"""
    scad_content = f"""// Auto-generated nametag for: {name}

// Parameters
name = "{name}";
nametag_width = {params["nametag_width"]};
nametag_height = {params["nametag_height"]};
nametag_thickness = {params["nametag_thickness"]};
text_size = {params["text_size"]};
text_height = {params["text_height"]};
ring_width = {params["ring_width"]};
ring_height = {params["ring_height"]};
mounting_hole_diameter = {params["mounting_hole_diameter"]};
corner_radius = {params["corner_radius"]};

// Main nametag module
module nametag() {{
    difference() {{
        union() {{
            // Main body: rectangle on one side, semicircle on the other
            nametag_body(nametag_width, nametag_height, nametag_thickness, corner_radius);
            
            // Elevated ring around the border
            elevated_ring(nametag_width, nametag_height, nametag_thickness, ring_width, ring_height, corner_radius);
            
            // Raised text on top
            translate([nametag_width/2, nametag_height/2, nametag_thickness])
                linear_extrude(height = text_height)
                    text(name, size = text_size, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
        }}
        
        // Mounting hole in the center of the circular side
        translate([nametag_width, nametag_height/2, -0.5])
            cylinder(h = nametag_thickness + ring_height + text_height + 1, d = mounting_hole_diameter, $fn = 30);
    }}
}}

// Module to create the main body shape (rectangle + semicircle)
module nametag_body(width, height, thickness, radius) {{
    hull() {{
        // Rectangular side with rounded corners (left side)
        translate([radius, radius, 0])
            cylinder(r = radius, h = thickness, $fn = 30);
        translate([radius, height - radius, 0])
            cylinder(r = radius, h = thickness, $fn = 30);
        
        // Semicircle on the right side
        translate([width, height/2, 0])
            cylinder(r = height/2, h = thickness, $fn = 60);
    }}
}}

// Module to create the elevated ring
module elevated_ring(width, height, thickness, ring_w, ring_h, radius) {{
    difference() {{
        // Outer shape (same as body but elevated)
        translate([0, 0, thickness])
            hull() {{
                // Rectangular side with rounded corners
                translate([radius, radius, 0])
                    cylinder(r = radius, h = ring_h, $fn = 30);
                translate([radius, height - radius, 0])
                    cylinder(r = radius, h = ring_h, $fn = 30);
                
                // Semicircle on the right side
                translate([width, height/2, 0])
                    cylinder(r = height/2, h = ring_h, $fn = 60);
            }}
        
        // Inner cutout (smaller shape)
        translate([0, 0, thickness - 0.5])
            hull() {{
                // Inner rectangular side
                translate([radius + ring_w, radius + ring_w, 0])
                    cylinder(r = radius, h = ring_h + 1, $fn = 30);
                translate([radius + ring_w, height - radius - ring_w, 0])
                    cylinder(r = radius, h = ring_h + 1, $fn = 30);
                
                // Inner semicircle (smaller radius)
                translate([width, height/2, 0])
                    cylinder(r = height/2 - ring_w, h = ring_h + 1, $fn = 60);
            }}
    }}
}}

// Generate the nametag
nametag();
"""

    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(scad_content)


def sanitize_filename(name):
    """Create a safe filename from a name"""
    # Remove or replace characters that aren't safe for filenames
    safe_name = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in name)
    safe_name = safe_name.strip().replace(" ", "_")
    return safe_name


def generate_stl(openscad_path, name, params, output_dir):
    """Generate an STL file for a given name"""
    safe_name = sanitize_filename(name)
    temp_scad = os.path.join(output_dir, f"temp_{safe_name}.scad")
    output_stl = os.path.join(output_dir, f"{safe_name}.stl")

    # Create temporary SCAD file
    create_temp_scad(name, params, temp_scad)

    # Generate STL using OpenSCAD
    print(f"Generating STL for: {name}...", end=" ")
    try:
        result = subprocess.run(
            [openscad_path, "-o", output_stl, temp_scad],
            capture_output=True,
            timeout=60,
            text=True,
        )

        if result.returncode == 0 and os.path.exists(output_stl):
            print("✓ Success")
            # Clean up temporary file
            os.remove(temp_scad)
            return True
        else:
            print("✗ Failed")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Timeout")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def read_csv(csv_file):
    """Read names and optional parameters from CSV file"""
    names_data = []

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # get name safely (row.get can return None)
            raw_name = row.get("name") if row is not None else None
            if raw_name is None or str(raw_name).strip() == "":
                # skip rows without a valid name
                continue
            name = str(raw_name).strip()

            # Start with default parameters
            params = DEFAULT_PARAMS.copy()

            # Override with CSV values if provided, but handle None/empty gracefully
            for key in DEFAULT_PARAMS.keys():
                raw_val = row.get(key) if row is not None else None
                if raw_val is None:
                    continue
                sval = str(raw_val).strip()
                if sval == "":
                    continue
                try:
                    # keep numeric defaults as floats
                    params[key] = float(sval)
                except ValueError:
                    # if conversion fails, keep default
                    continue

            names_data.append({"name": name, "params": params})

    return names_data


def main():
    print("=" * 60)
    print("Automatic Nametag STL Generator")
    print("=" * 60)
    print()

    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file '{CSV_FILE}' not found!")
        print(f"\nPlease create a CSV file with at least a 'name' column.")
        print("Example CSV content:")
        print("name")
        print("John Smith")
        print("Jane Doe")
        print("Alice Johnson")
        sys.exit(1)

    # Find OpenSCAD
    openscad_path = find_openscad()
    if not openscad_path:
        print("Error: OpenSCAD not found!")
        print("\nPlease install OpenSCAD from: https://openscad.org/downloads.html")
        print("Or ensure it's in your system PATH.")
        sys.exit(1)

    # Create output directory
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Read names from CSV
    try:
        names_data = read_csv(CSV_FILE)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    if not names_data:
        print("Error: No valid names found in CSV file!")
        sys.exit(1)

    print(f"Found {len(names_data)} name(s) to process")
    print()

    # Generate STL for each name
    successful = 0
    failed = 0

    for i, data in enumerate(names_data, 1):
        print(f"[{i}/{len(names_data)}] ", end="")
        if generate_stl(openscad_path, data["name"], data["params"], OUTPUT_DIR):
            successful += 1
        else:
            failed += 1

    # Summary
    print()
    print("=" * 60)
    print("Generation Complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Output location: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
