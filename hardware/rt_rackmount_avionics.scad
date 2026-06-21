/*
 * REVOLUTIONARY TECHNOLOGY: 6U RACKMOUNT AVIONICS DASHBOARD
 * Standard: EIA-310 19-Inch Rack (Width: 482.6mm, 6U Height: 266.7mm)
 * Cutouts: PFD (Primary Flight Display), ND (Nav Display), ISFD (Standby)
 */

$fn = 64;

// 19" Rack Standard Dimensions
rack_width = 482.6;
rack_height = 266.7; // 6U
panel_thick = 4.0;
hole_spacing_x = 465.1; // Standard mounting hole width

module rackmount_avionics_panel() {
    color("Silver") {
        difference() {
            // Main Aluminum Panel
            cube([rack_width, rack_height, panel_thick], center=true);
            
            // Rackmount Ears (Mounting Holes)
            for (x = [-hole_spacing_x/2, hole_spacing_x/2]) {
                for (y = [-100, 0, 100]) { // 3 bolts per side for 6U
                    translate([x, y, 0])
                        cylinder(r=3.5, h=panel_thick + 2, center=true);
                }
            }
            
            // --- AVIONICS SCREEN CUTOUTS ---
            
            // 1. Primary Flight Display (PFD) - Left
            translate([-120, 0, 0])
                cube([180, 220, panel_thick + 2], center=true);
                
            // 2. Navigation Display (ND) - Center
            translate([80, 0, 0])
                cube([180, 220, panel_thick + 2], center=true);
                
            // 3. Integrated Standby Flight Display (ISFD) - Top Right
            translate([200, 60, 0])
                cube([45, 60, panel_thick + 2], center=true);
                
            // 4. EICAS / System Annunciators - Bottom Right
            translate([200, -30, 0])
                cube([45, 100, panel_thick + 2], center=true);
        }
    }
}

rackmount_avionics_panel();
