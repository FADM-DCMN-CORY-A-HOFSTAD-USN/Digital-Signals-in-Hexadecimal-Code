/*
 * REVOLUTIONARY TECHNOLOGY: TYPE-S SAIYA HOTAS (FLIGHT STICK)
 * Mount: Bolt-Down Deck Plate (4-Point Aerospace Standard)
 * Features: Ergonomic Grip, Dual-Stage Trigger, 4-Way Trim Hat
 */

$fn = 64;

// Base Plate Dimensions
base_w = 160;
base_l = 200;
base_h = 12;
bolt_radius = 4.5; // M8 Bolts

module bolt_down_base() {
    color("DarkSlateGray") {
        difference() {
            // Main Deck Plate
            minkowski() {
                cube([base_w - 10, base_l - 10, base_h/2], center=true);
                cylinder(r=5, h=base_h/2, center=true);
            }
            // 4x Corner Bolt Holes for Deck Mounting
            for (x = [-base_w/2 + 15, base_w/2 - 15]) {
                for (y = [-base_l/2 + 15, base_l/2 - 15]) {
                    translate([x, y, 0])
                        cylinder(r=bolt_radius, h=base_h + 10, center=true);
                    // Countersink for flush bolts
                    translate([x, y, base_h/2 - 2])
                        cylinder(r=bolt_radius*2, h=5, center=true);
                }
            }
        }
    }
}

module gimbal_boot() {
    // Flexible dust boot covering the dual-axis Hall-Effect sensors
    color("Black", 0.9) {
        translate([0, 0, base_h/2]) {
            for (i = [0:4]) {
                translate([0, 0, i*8 + 4])
                    cylinder(r1=35 - i*3, r2=32 - i*3, h=8, center=true);
            }
        }
    }
}

module flight_grip() {
    color("DimGray") {
        translate([0, 0, 80]) {
            // Main Shaft
            rotate([0, 10, 0]) { // 10-degree ergonomic forward tilt
                cylinder(r=16, h=120, center=true);
                
                // Palm Rest
                translate([0, -10, -50])
                    resize([1, 1.5, 0.5]) sphere(r=20);
                    
                // Head / Electronics Bay
                translate([0, 5, 55])
                    minkowski() {
                        cube([30, 40, 30], center=true);
                        sphere(r=5);
                    }
                    
                // Trigger (Dual Stage)
                color("DarkRed")
                translate([0, 25, 30])
                    rotate([45, 0, 0])
                    cube([8, 20, 10], center=true);
                    
                // 4-Way Trim Hat (Top)
                color("Silver")
                translate([0, 5, 75])
                    cylinder(r=8, h=5, center=true);
            }
        }
    }
}

module master_hotas_assembly() {
    bolt_down_base();
    gimbal_boot();
    flight_grip();
}

master_hotas_assembly();
