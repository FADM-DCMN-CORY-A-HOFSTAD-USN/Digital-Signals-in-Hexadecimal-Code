// ========================================================
// RT ARCHITECTURE - RADIAL / STAR CORE WAFER TOPOLOGY
// ========================================================

$fn = 60; // Model smooth lines

// --- Design Parameters ---
num_cores = 8;          // Number of processing cores facing center
die_radius = 18.0;      // Distance from center to core faces (mm)
core_w = 6.0;           // Width of an individual core tile
core_l = 8.0;           // Length of an individual core tile
core_h = 0.5;           // Silicon layer thickness
center_nexus_d = 10.0;  // Diameter of central crossbar / NoC router

module compute_core(id) {
    // Individual Core block with a color gradient accent
    color([0.2, 0.4, 0.1 + (id * 0.1)]) {
        cube([core_l, core_w, core_h], center=true);
        
        // Data Interface Port Indicator (Visual marker pointing inside)
        translate([-core_l/2 + 0.5, 0, core_h/2 + 0.05])
            color("Gold") cube([1, core_w - 1, 0.1], center=true);
    }
}

module central_router() {
    // The central network crossbar that all cores look at
    color("DarkRed") {
        cylinder(h=core_h + 0.2, d=center_nexus_d, center=true);
        // Central micro-via clock tower reference indicator
        translate([0,0,1]) cylinder(h=2, d=1, center=true);
    }
}

module interconnect_bus(angle) {
    // Radial trace lines connecting the core interfaces straight to center
    rotate([0, 0, angle])
        translate([die_radius / 2, 0, 0])
            color("Cyan", 0.6) 
                cube([die_radius, 0.4, 0.05], center=true);
}

module build_radial_processor() {
    // 1. Establish the Dead Center Nexus Point
    central_router();
    
    // 2. Map and Rotate Cores radially around the circle boundary
    for (i = [0 : num_cores - 1]) {
        current_angle = i * (360 / num_cores);
        
        // Render interconnect routing lines running inward
        interconnect_bus(current_angle);
        
        // Position and rotate the individual compute block
        rotate([0, 0, current_angle])
            translate([die_radius, 0, 0])
                rotate([0, 0, 180]) // Flips core front porch toward center
                    compute_core(i);
    }
}

// Instantiate the complete circular chip layout
build_radial_processor();
