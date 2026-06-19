// =================================================================
// TYPE-S SAIYA: SNAP-CIRCUIT DOUBLE LATCH GATE BUFFER
// Flush-Mount Luxury Enclosure with Precision Fracture V-Groove
// Designed for CNC Machining and Automated Assembly
// =================================================================
include <GM_shocks.scad>; 

$fn = 60; 

// Parametric Dimensions
total_length = 160;
width = 60;
height = 15;
corner_radius = 8;
v_groove_depth = 12; // Leaves exactly 3mm of frangible material to snap

module rounded_flush_plate(l, w, h, r) {
    hull() {
        translate([r, r, 0]) cylinder(h=h, r=r);
        translate([l - r, r, 0]) cylinder(h=h, r=r);
        translate([r, w - r, 0]) cylinder(h=h, r=r);
        translate([l - r, w - r, 0]) cylinder(h=h, r=r);
    }
}

module flush_countersink(hole_r=2, head_r=4.5, head_h=3) {
    // Snag-free luxury aerospace countersinks
    translate([0, 0, -0.1])
    union() {
        cylinder(h=height, r=hole_r);
        translate([0, 0, height - head_h])
            cylinder(h=head_h, r1=hole_r, r2=head_r);
    }
}

module snap_circuit_chassis() {
    difference() {
        // Main Titanium or Composite Body
        color("DimGray")
        rounded_flush_plate(total_length, width, height, corner_radius);

        // The Center Fracture V-Groove (Top and Bottom)
        // Allows the machine to score the chassis so it can be snapped by hand
        translate([total_length / 2, width / 2, height])
        rotate([90, 0, 0])
        cylinder(h=width, r1=v_groove_depth, r2=0, center=true, $fn=4); 

        translate([total_length / 2, width / 2, 0])
        rotate([90, 0, 0])
        cylinder(h=width, r1=v_groove_depth, r2=0, center=true, $fn=4); 

        // Internal Cavity for the 24k Gold Lattice and Silicon
        translate([4, 4, 3])
        rounded_flush_plate(total_length - 8, width - 8, height - 6, corner_radius - 2);

        // Flush Mounting Holes (Distributed for stability across the fracture line)
        positions = [
            [corner_radius, corner_radius],
            [(total_length / 2) - 15, corner_radius], 
            [(total_length / 2) - -15, corner_radius], 
            [total_length - corner_radius, corner_radius],
            [corner_radius, width - corner_radius],
            [(total_length / 2) - 15, width - corner_radius],
            [(total_length / 2) - -15, width - corner_radius],
            [total_length - corner_radius, width - corner_radius]
        ];

        for (pos = positions) {
            translate([pos[0], pos[1], 0])
                flush_countersink();
        }
    }
}

module gold_latch_gates() {
    // The 24k Gold internal cross-coupled inverters
    color("Gold") {
        // Node A (Local Hub)
        translate([30, width/2, height/2]) cube([40, 30, 4], center=true);
        // Node B (Remote Node)
        translate([total_length - 30, width/2, height/2]) cube([40, 30, 4], center=true);

        // The frangible gold lattice bridge connecting them across the snap line
        translate([total_length/2, width/2, height/2]) cube([40, 8, 1], center=true);
    }
}

// Deploy Rubber Shock Absorbers beneath each mounting point
module deploy_shock_mounts() {
    positions = [
        [corner_radius, corner_radius],
        [(total_length / 2) - 15, corner_radius],
        [(total_length / 2) - -15, corner_radius],
        [total_length - corner_radius, corner_radius],
        [corner_radius, width - corner_radius],
        [(total_length / 2) - 15, width - corner_radius],
        [(total_length / 2) - -15, width - corner_radius],
        [total_length - corner_radius, width - corner_radius]
    ];

    for (pos = positions) {
        translate([pos[0], pos[1], -4])
            pcb_standoff_shock(height=8);
    }
}

// Execute Assembly Render
snap_circuit_chassis();
gold_latch_gates();
deploy_shock_mounts();
