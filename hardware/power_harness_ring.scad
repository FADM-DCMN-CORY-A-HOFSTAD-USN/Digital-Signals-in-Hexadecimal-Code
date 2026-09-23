// ==========================================
// RT ARCHITECTURE - FLEXIBLE POWER HARNESS RING
// ==========================================

$fn = 100; // Render resolution

// --- Parameters ---
cable_diameter = 6.0;   // Diameter of your heavy gauge power cable
ring_thickness = 2.5;   // Wall thickness of the snap-ring
harness_width = 8.0;    // Depth/width of the harness clip
gap_angle = 45;         // Opening expansion gap angle in degrees
mount_height = 5.0;     // Base anchoring section offset

module power_cable_harness() {
    difference() {
        // Main Outer Ring Structure
        union() {
            cylinder(h=harness_width, d=cable_diameter + (ring_thickness * 2), center=true);
            
            // Third section anchor latch mount
            translate([0, -(cable_diameter/2 + ring_thickness + mount_height/2), 0])
                cube([cable_diameter + ring_thickness, mount_height, harness_width], center=true);
        }
        
        // Inner Core Cable Routing Channel
        cylinder(h=harness_width + 2, d=cable_diameter, center=true);
        
        // Compliant Expansion Cutout Latch (Top Section Open Gap)
        rotate([0, 0, 90])
            linear_extrude(height=harness_width + 2, center=true)
                polygon(points=[
                    [0, 0],
                    [cable_diameter * 2 * cos(gap_angle/2), cable_diameter * 2 * sin(gap_angle/2)],
                    [cable_diameter * 2 * cos(-gap_angle/2), cable_diameter * 2 * sin(-gap_angle/2)]
                ]);
    }
}

// Render the structural component
power_cable_harness();
