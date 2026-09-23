// STORMSTOPPER Industrial ATX Chassis Design
// Models both Rugged Field Closures and 4U Server Rack Specs
// Engineered by Emerald City Techs for Data Recovery Nevada Labs

$fn = 80; // High geometric precision rendering threshold

// Structural Dimensional Definitions (Metric Alignment)
in_to_mm = 25.4;
case_width = 19.0 * in_to_mm;   // Standard 19" Rackmount Width (482.6 mm)
case_height = 7.0 * in_to_mm;   // Standard 4U Rackmount Height (177.8 mm)
case_depth = 22.0 * in_to_mm;    // Standard Server Cabinet Depth (558.8 mm)
wall_thickness = 4;              // Heavy-duty structural aluminum walls

module rt_industrial_chassis() {
    difference() {
        // Main Physical Outer Chassis Block
        cube([case_width, case_depth, case_height], center = true);
        
        // Internal Component Bay Cavity (Protected Zone)
        cube([case_width - (2 * wall_thickness), case_depth - (2 * wall_thickness), case_height - (2 * wall_thickness)], center = true);
        
        // Rear Cutout Port Panel for Isolated Interface Array
        translate([0, (case_depth / 2) - wall_thickness, -10]) {
            cube([250, wall_thickness + 4, 60], center = true);
        }
        
        // Front Panel Intake Vent Openings for Centrifugal Exhaust Fans
        for (x = [-150, 0, 150]) {
            translate([x, -(case_depth / 2) + 2, 0]) {
                rotate([90, 0, 0]) cylinder(h = wall_thickness + 4, d = 80, center = true);
            }
        }
    }
    
    // Internal Circular Standoff Array for Hexadecimal ATX Motherboard
    translate([-(case_width/4), 0, -(case_height/2) + wall_thickness]) {
        for (y = [-100, 0, 100]) {
            for (x = [-80, 0, 80]) {
                translate([x, y, 6]) {
                    difference() {
                        cylinder(h = 12, d = 10, center = true);
                        cylinder(h = 14, d = 3.2, center = true); // M3 Screw Pattern
                    }
                }
            }
        }
    }
}

rt_industrial_chassis();
