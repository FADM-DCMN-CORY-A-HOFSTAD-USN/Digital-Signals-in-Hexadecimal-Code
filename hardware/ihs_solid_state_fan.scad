// ========================================================
// RT ARCHITECTURE - INTEGRATED SOLID-STATE COOLING IHS
// ========================================================

$fn = 60; // Render quality

// --- IHS Dimensions ---
ihs_width = 37.5;       // Standard CPU IHS width (mm)
ihs_length = 37.5;      // Standard CPU IHS length (mm)
ihs_total_height = 4.5; // Total height including internal cavity
die_floor_thick = 0.5;  // Ultra-thin copper floor above silicon die

// --- Solid-State Cavity Dimensions (e.g., AirJet Mini Spec) ---
ss_width = 27.5;        // Width of solid state cooler
ss_length = 20.5;       // Half-length or compact footprint variant
ss_height = 2.8;        // Thickness of the active cooling unit
exhaust_width = 1.5;    // Side exhaust spout slot thickness

module integrated_solid_state_ihs() {
    difference() {
        // 1. Main Outer Metal Cap (Copper Heat Spreader)
        translate([0, 0, ihs_total_height/2])
            cube([ihs_width, ihs_length, ihs_total_height], center=true);
        
        // 2. Embedded Solid-State Fan Internal Cavity
        // Placed directly above the thin die contact floor
        translate([0, 0, die_floor_thick + ss_height/2])
            cube([ss_width, ss_length, ss_height + 0.1], center=true);
        
        // 3. Top Intake Vents (Where the membrane pulls clean air down)
        translate([0, 0, ihs_total_height - 1])
            cube([ss_width - 4, ss_length - 4, 3], center=true);
            
        // 4. Lateral Exhaust Spouts (Flushes hot air out the sides)
        // High-velocity air escapes through these structural paths
        translate([0, 0, die_floor_thick + ss_height/2])
            cube([ihs_width + 2, ss_length - 2, exhaust_width], center=true);
            
        // 5. Secondary Cross-Flow Exhaust Channel
        translate([0, 0, die_floor_thick + ss_height/2])
            cube([ss_width - 2, ihs_length + 2, exhaust_width], center=true);
    }
    
    // Visual Guide: Silicon Die Boundary Footprint Indicator (Underside)
    % translate([0, 0, -0.1])
        color("Gray", 0.5) 
            cube([15, 15, 0.2], center=true);
}

// Instantiate the solid-state structural cap
integrated_solid_state_ihs();
