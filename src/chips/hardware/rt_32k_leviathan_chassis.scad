/*
 * REVOLUTIONARY TECHNOLOGY: RT-32K LEVIATHAN CINEMA CHASSIS
 * Material Outer: Carbon-Nanotube Infused TPU Rubber (ESD Safe)
 * Material Inner: Exposed Titanium Vapor Chamber Heatsink Fins
 * Mount: ARRI LPL (Large Format 65mm)
 */

$fn = 64;

// Leviathan Dimensions
cam_width = 190;
cam_height = 180;
cam_depth = 160;
wall_thickness = 5.0;
rubber_armor = 4.0;

// ARRI LPL Mount Specs
lpl_throat = 62.0;
lpl_flange = 44.0;

module arri_lpl_mount() {
    color("LightGray") {
        translate([0, cam_height/2, cam_depth]) {
            // Massive LPL Ring
            cylinder(h=12, r=(lpl_throat/2) + 5);
            // Internal Throat
            translate([0, 0, -2]) cylinder(h=16, r=lpl_throat/2);
            // Locking PL-Style wings
            for(angle = [0, 90, 180, 270]) {
                rotate([0, 0, angle])
                translate([(lpl_throat/2) + 2, -8, 6])
                cube([6, 16, 4]);
            }
        }
    }
}

module elastomer_shock_core() {
    color("DarkSlateGray") {
        cylinder(h=15, r=6, center=true);
        cylinder(h=3, r=10, center=true); 
    }
}

module titanium_vapor_chamber_skeleton() {
    // The skeleton is actually a massive finned heatsink for the 32K sensor
    color("Silver", 0.95) {
        difference() {
            translate([-cam_width/2 + 10, 10, 10])
                cube([cam_width - 20, cam_height - 20, cam_depth - 20]);
                
            // Hollow core for the sensor / quantum array
            translate([-cam_width/2 + 20, 20, 20])
                cube([cam_width - 40, cam_height - 40, cam_depth]);
        }
        
        // Massive Thermal Exhaust Fins sticking out of the top and sides
        for (x = [-cam_width/2 + 20 : 10 : cam_width/2 - 20]) {
            translate([x, cam_height - 10, 20])
                cube([2, 25, cam_depth - 40]);
        }
    }
}

module rubber_leviathan_armor() {
    color("Black", 0.9) {
        difference() {
            // Main housing
            translate([-cam_width/2 - rubber_armor, -rubber_armor, -rubber_armor])
                minkowski() {
                    cube([cam_width + 2*rubber_armor, cam_height + 2*rubber_armor, cam_depth + 2*rubber_armor]);
                    sphere(r=8);
                }
                
            // Cutout for the internal skeleton
            translate([-cam_width/2, 0, 0])
                cube([cam_width, cam_height, cam_depth + 20]); 
                
            // Cutout for the Thermal Exhaust Fins (Top)
            translate([-cam_width/2 + 15, cam_height - 15, 15])
                cube([cam_width - 30, 40, cam_depth - 30]);
                
            // Massive LPL Mount Cutout
            translate([0, cam_height/2, cam_depth])
                cylinder(h=30, r=(lpl_throat/2) + 8, center=true);
                
            // 15mm / 19mm Studio Rod cutouts (Baseplate)
            translate([-40, -10, 40]) rotate([90, 0, 0]) cylinder(h=40, r=9.5, center=true);
            translate([ 40, -10, 40]) rotate([90, 0, 0]) cylinder(h=40, r=9.5, center=true);
        }
    }
}

module master_32k_assembly() {
    rubber_leviathan_armor();
    titanium_vapor_chamber_skeleton();
    arri_lpl_mount();
    
    // Heavy-Duty 6-point Elastomer Decoupling
    for (x = [-cam_width/2 + 15, cam_width/2 - 15]) {
        for (y = [20, cam_height - 20]) {
            translate([x, y, 10]) elastomer_shock_core();
            translate([x, y, cam_depth - 25]) elastomer_shock_core();
        }
    }
}

// Render the Leviathan
master_32k_assembly();
