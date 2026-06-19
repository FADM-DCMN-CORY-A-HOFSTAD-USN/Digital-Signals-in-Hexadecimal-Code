// =================================================================
// TYPE-S SAIYA GLOBAL SHOCK ABSORBER LIBRARY
// Enforces vibration dampening across all mounting interfaces.
// =================================================================

$fn = 50;

module shock_absorber(bolt_radius = 2.5, rubber_thickness = 3, height = 5) {
    // Standard cylindrical rubber grommet / shock bushing
    color("Black", 0.9)
    difference() {
        // Outer rubber bushing
        cylinder(h = height, r = bolt_radius + rubber_thickness, center = true);
        
        // Inner clearance for the steel bolt
        cylinder(h = height + 2, r = bolt_radius, center = true);
    }
}

module heavy_shock_mount(bolt_radius = 4, rubber_thickness = 5, height = 10) {
    // Flanged heavy-duty shock mount for high-mass items (OXYMOSS tanks, ATX Motherboard)
    color("Black", 0.85)
    difference() {
        union() {
            // Main rubber core
            cylinder(h = height, r = bolt_radius + rubber_thickness, center = true);
            // Compression flanges (Top and Bottom)
            translate([0, 0, height/2 - 1]) 
                cylinder(h = 2, r = bolt_radius + rubber_thickness + 3, center = true);
            translate([0, 0, -height/2 + 1]) 
                cylinder(h = 2, r = bolt_radius + rubber_thickness + 3, center = true);
        }
        // Inner bolt clearance
        cylinder(h = height + 4, r = bolt_radius, center = true);
    }
}

module pcb_standoff_shock(height=8) {
    // Specialized mount for silicon/motherboards
    // Combines a brass standoff with a rubber vibration isolation pad
    union() {
        // Brass standoff body
        color("Brass")
        translate([0,0, -height/2])
        cylinder(h = height, r = 3, center=true, $fn=6); // Hexagonal brass
        
        // Rubber isolation pad separating the PCB from the brass
        translate([0,0, 1])
        shock_absorber(bolt_radius=1.5, rubber_thickness=2, height=2);
    }
}
