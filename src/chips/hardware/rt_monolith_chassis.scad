/*
 * REVOLUTIONARY TECHNOLOGY: RT-16K MONOLITH CAMERA CHASSIS
 * Material Outer: Over-molded Thermoplastic Polyurethane (TPU) Rubber
 * Material Inner: Aerospace Grade Titanium Skeleton
 * Mount: Canon EF 
 */

$fn = 64;

// Camera Dimensions
cam_width = 160;
cam_height = 140;
cam_depth = 120;
wall_thickness = 4.0;
rubber_armor = 3.0;

// Canon EF Mount Specs
ef_diameter = 54.0;
ef_flange_distance = 44.0;

module canon_ef_mount() {
    color("Silver") {
        translate([0, cam_height/2, cam_depth]) {
            // Main ring
            cylinder(h=8, r=ef_diameter/2);
            // Locking bayonet tabs (Simplified)
            for(angle = [0, 120, 240]) {
                rotate([0, 0, angle])
                translate([ef_diameter/2 - 1, -5, 4])
                cube([4, 10, 2]);
            }
        }
    }
}

module elastomer_shock_mount() {
    // These decouple the internal titanium frame from the outer shell
    color("DarkSlateGray") {
        cylinder(h=10, r=4, center=true);
        cylinder(h=2, r=7, center=true); // Flange
    }
}

module internal_titanium_skeleton() {
    color("LightGray", 0.9) {
        difference() {
            // Inner rigid frame
            translate([-cam_width/2 + wall_thickness, wall_thickness, wall_thickness])
                cube([cam_width - 2*wall_thickness, cam_height - 2*wall_thickness, cam_depth - 2*wall_thickness]);
            
            // Hollow out for the CPU, CUDA, and Sensor
            translate([-cam_width/2 + 2*wall_thickness, 2*wall_thickness, 2*wall_thickness])
                cube([cam_width - 4*wall_thickness, cam_height - 4*wall_thickness, cam_depth]);
        }
        
        // M.2 Snap Circuit Bay (Rear)
        translate([-20, 10, 5])
            cube([40, 80, 10]);
    }
}

module outer_rubber_armor() {
    color("Black", 0.85) {
        difference() {
            // Massive rubber over-mold block
            translate([-cam_width/2 - rubber_armor, -rubber_armor, -rubber_armor])
                minkowski() {
                    cube([cam_width + 2*rubber_armor, cam_height + 2*rubber_armor, cam_depth + 2*rubber_armor]);
                    sphere(r=5);
                }
                
            // Hollow out for the titanium skeleton
            translate([-cam_width/2, 0, 0])
                cube([cam_width, cam_height, cam_depth + 10]); // +10 to cut out the lens opening
                
            // Cutout for the EF Lens Mount
            translate([0, cam_height/2, cam_depth])
                cylinder(h=20, r=(ef_diameter/2) + 2, center=true);
                
            // Rear Waterproof Hatch (Access to USB 3.2, Battery, and M.2)
            translate([-cam_width/3, cam_height/4, -10])
                cube([cam_width * 0.66, cam_height/2, 20]);
        }
        
        // Add rugged grip ridges
        for (i = [-cam_width/2 + 10 : 15 : cam_width/2 - 10]) {
            translate([i, -rubber_armor, cam_depth/2])
                cylinder(h=cam_depth-20, r=2, center=true);
        }
    }
}

module master_assembly() {
    // 1. Core Structure
    outer_rubber_armor();
    internal_titanium_skeleton();
    canon_ef_mount();
    
    // 2. Elastomer Decoupling (Placing shocks between outer and inner shell)
    for (x = [-cam_width/2 + 10, cam_width/2 - 10]) {
        for (y = [10, cam_height - 10]) {
            translate([x, y, 5])
                elastomer_shock_mount();
            translate([x, y, cam_depth - 15])
                elastomer_shock_mount();
        }
    }
    
    // 3. I/O Ports (Rear)
    color("Gold") {
        // USB 3.2 Gen 2 Port
        translate([10, cam_height/3, 0])
            cube([12, 5, 8]); 
            
        // Solid-State Battery Block
        translate([-30, cam_height/3, 0])
            cube([35, 20, 15]);
    }
}

// Render the Ultimate Camera
master_assembly();
