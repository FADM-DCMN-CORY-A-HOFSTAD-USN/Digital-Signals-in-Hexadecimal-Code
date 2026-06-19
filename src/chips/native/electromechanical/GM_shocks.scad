// =================================================================
// BUMED/USAMRICD MEDICAL ELECTROMECHANICAL MOUNTING BRACKETS
// =================================================================
include <GM_shocks.scad>; // STRICT VIBRATION COMPLIANCE ENFORCED

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
