// =================================================================
// BUMED/USAMRICD MEDICAL ELECTROMECHANICAL MOUNTING BRACKETS
// =================================================================
include <GM_shocks.scad>; // STRICT VIBRATION COMPLIANCE ENFORCED

module plasma_shield_vrm_housing() {
    // Massive aluminum heatsink array for the voltage regulator
    color("Silver")
    difference() {
        cube([60, 40, 25], center=true);
        // Cut out cooling fins
        for(i = [-25 : 5 : 25]) {
            translate([i, 0, 10])
            cube([2, 42, 16], center=true);
        }
    }
    
    // Heavy electrical isolation mounts (rubber + ceramic)
    for (x = [-25, 25]) {
        for (y = [-15, 15]) {
            translate([x, y, -15])
            heavy_shock_mount(bolt_radius=3, rubber_thickness=4, height=10);
        }
    }
}

module astrometrics_inertial_core() {
    // A perfectly spherical, pressurized housing for the quantum gyroscopes
    color("Gold", 0.9)
    sphere(r=20, $fn=100);
    
    // The mounting bracket holding the sphere
    color("DarkSlateGray")
    difference() {
        translate([0, 0, -10])
        cylinder(h=15, r=25, center=true, $fn=60);
        
        // Hollow for the sphere to rest in
        sphere(r=21, $fn=100);
    }
    
    // 6-Point micro-shock absorbers for absolute zero-drift stability
    for(i = [0 : 60 : 359]) {
        rotate([0, 0, i])
        translate([20, 0, -20])
        pcb_standoff_shock(height=8);
    }
}

// Render the components
translate([-40, 0, 0]) plasma_shield_vrm_housing();
translate([40, 0, 0]) astrometrics_inertial_core();

module bumed_spectrometer_bridge_mount() {
    // Mounts the HexNativeCBRNAnalyzer near the external airlock sampling tubes
    difference() {
        // Thick protective titanium casing for the sensor bridge
        color("Silver")
        cube([80, 40, 15], center=true);
        
        // Internal hollow for the PCB
        cube([70, 30, 16], center=true);
        
        // Fiber Optic pass-through hole for the spectrometer
        translate([0, 20, 0]) rotate([90, 0, 0])
        cylinder(h=10, r=4, $fn=30, center=true);
    }
    
    // 4-Point Heavy Duty Shock Absorbers to prevent optical misalignment
    positions = [[-45, -25], [45, -25], [-45, 25], [45, 25]];
    for (pos = positions) {
        translate([pos[0], pos[1], -10])
        heavy_shock_mount(bolt_radius=3, rubber_thickness=4, height=8);
    }
}

module med_dispenser_fluid_block() {
    // Mounts the HexNativeMedDispenser. Must integrate with fluid lines.
    difference() {
        color("White", 0.9) // Medical White
        cylinder(h=30, r=25, $fn=60, center=true);
        
        // 3 Fluid micro-valve routing channels (Atropine, Stimulant, Iodine)
        for (i = [0, 120, 240]) {
            rotate([0, 0, i])
            translate([15, 0, 0])
            cylinder(h=32, r=2.5, $fn=20, center=true);
        }
    }
    
    // The Stepper Motor / Actuator PCB sits on top, isolated from fluid vibrations
    translate([0, 0, 15])
    pcb_standoff_shock(height=6);
}

// Render the assembly for the KiCad/Gantry Bridge
bumed_spectrometer_bridge_mount();
translate([100, 0, 0]) med_dispenser_fluid_block();
