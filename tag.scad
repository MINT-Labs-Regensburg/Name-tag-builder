// Customizable Nametag with Mounting Hole
// Adjust the parameters below to customize your nametag

// Customizable Parameters
name = "YOUR NAME"; // The name to display on the tag
nametag_width = 80; // Width of the nametag (rectangular part)
nametag_height = 30; // Height of the nametag
nametag_thickness = 3; // Thickness of the nametag base
text_size = 8; // Size of the text
text_height = 1.5; // How much the text raises above the surface
ring_width = 3; // Width of the elevated ring border
ring_height = 1. 2; // Height of the elevated ring (rises into text layer)
mounting_hole_diameter = 4; // Diameter of the mounting hole
corner_radius = 3; // Radius for rounded corners on rectangular side

// Main nametag module
module nametag() {
    difference() {
        union() {
            // Main body: rectangle on one side, semicircle on the other
            nametag_body(nametag_width, nametag_height, nametag_thickness, corner_radius);
            
            // Elevated ring around the border
            elevated_ring(nametag_width, nametag_height, nametag_thickness, ring_width, ring_height, corner_radius);
            
            // Raised text on top - starts at base level, goes up through ring into text layer
            translate([nametag_width/2, nametag_height/2, nametag_thickness])
                linear_extrude(height = ring_height + text_height)
                    text(name, size = text_size, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
        }
        
        // Mounting hole in the center of the circular side
        translate([nametag_width, nametag_height/2, -0.5])
            cylinder(h = nametag_thickness + ring_height + text_height + 1, d = mounting_hole_diameter, $fn = 30);
    }
}

// Module to create the main body shape (rectangle + semicircle)
module nametag_body(width, height, thickness, radius) {
    hull() {
        // Rectangular side with rounded corners (left side)
        translate([radius, radius, 0])
            cylinder(r = radius, h = thickness, $fn = 30);
        translate([radius, height - radius, 0])
            cylinder(r = radius, h = thickness, $fn = 30);
        
        // Semicircle on the right side
        translate([width, height/2, 0])
            cylinder(r = height/2, h = thickness, $fn = 60);
    }
}

// Module to create the elevated ring
module elevated_ring(width, height, thickness, ring_w, ring_h, radius) {
    difference() {
        // Outer shape (same as body but elevated)
        translate([0, 0, thickness])
            hull() {
                // Rectangular side with rounded corners
                translate([radius, radius, 0])
                    cylinder(r = radius, h = ring_h, $fn = 30);
                translate([radius, height - radius, 0])
                    cylinder(r = radius, h = ring_h, $fn = 30);
                
                // Semicircle on the right side
                translate([width, height/2, 0])
                    cylinder(r = height/2, h = ring_h, $fn = 60);
            }
        
        // Inner cutout (smaller shape)
        translate([0, 0, thickness - 0.5])
            hull() {
                // Inner rectangular side
                translate([radius + ring_w, radius + ring_w, 0])
                    cylinder(r = radius, h = ring_h + 1, $fn = 30);
                translate([radius + ring_w, height - radius - ring_w, 0])
                    cylinder(r = radius, h = ring_h + 1, $fn = 30);
                
                // Inner semicircle (smaller radius)
                translate([width, height/2, 0])
                    cylinder(r = height/2 - ring_w, h = ring_h + 1, $fn = 60);
            }
    }
}

// Generate the nametag
nametag();