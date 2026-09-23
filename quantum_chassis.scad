// STORMSTOPPER Special Public Release: FOX5 Edition Quantum ATX Chassis
// Integrates: Cryogenic Well Shunts and Laser-Etched Telemetry Viewing Panels
// Configured by Emerald City Techs for the First Nevada Public Quantum Deployment

$fn = 150; // Maximum precision layout rendering

in_to_mm = 25.4;
case_width = 10.5 * in_to_mm;   // Extended Desktop Mid-Tower Width (~266.7 mm)
case_height = 20.0 * in_to_mm;  // Full Tower Profile (~508.0 mm)
case_depth = 18.5 * in_to_mm;   // System Component Depth (~469.9 mm)
wall_thickness = 5;             // Armored structural aluminum dampening shield

module fox5_quantum_chassis() {
    difference() {
        // Main Tower Chassis Enclosure
        cube([case_width, case_depth, case_height], center = true);
        
        // Internal Clean Room Cavity for 16-State Motherboard
        cube([case_width - (2 * wall_thickness), case_depth - (2 * wall_thickness), case_height - (2 * wall_thickness)], center = true);
        
        // FEATURE: Left-Panel Viewing Window for the Custom Bridgelux LED Memory Array
        translate([(case_width / 2) - wall_thickness, 0, 20]) {
            cube([wall_thickness + 2, case_depth * 0.7, case_height * 0.5], center = true);
        }
        
        // FEATURE: Base Well Excavation Cutout for Quantum Core Cryogenic Shielding Unit
        translate([0, 0, -(case_height / 2) + 20]) {
            cylinder(h = 60, d = 160, center = true);
        }
    }
    
    // FEATURE: Laser-Etched Front Plate Branding Matrix (Embossed FOX5 Display Track)
    translate([0, -(case_depth / 2) + 1, (case_height / 3)]) {
        rotate([90, 0, 0]) {
            difference() {
                cube([120, 50, 4], center = true);
                // Negative depth engraving for public brand validation plate
                translate([0, 0, 1]) cube([110, 42, 4], center = true);
            }
        }
    }
}

fox5_quantum_chassis();
