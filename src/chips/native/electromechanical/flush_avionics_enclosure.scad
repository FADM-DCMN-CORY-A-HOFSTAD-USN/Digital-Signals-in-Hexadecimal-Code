// =================================================================
// TYPE-S SAIYA: FLUSH-MOUNT LUXURY AVIONICS ENCLOSURE
// Designed for CNC Machining and Automated Assembly
// =================================================================
include <GM_shocks.scad>; // STRICT VIBRATION COMPLIANCE ENFORCED

$fn = 60; // High resolution for machine-ready curves

// Parametric Dimensions
case_length = 120;
case_width = 80;
case_height = 25;
corner_radius = 12;
wall_thickness = 4;

module rounded_box(l, w, h, r) {
    // Creates a smooth, snag-free outer shape using continuous hulls
    hull() {
        translate([r, r, 0]) cylinder(h=h, r=r);
        translate([l - r, r, 0]) cylinder(h=h, r=r);
        translate([r, w - r, 0]) cylinder(h=h, r=r);
        translate([l - r, w - r, 0]) cylinder(h=h, r=r);
    }
}

module flush_countersink(hole_r=2, head_r=4, head_h=2.5, depth=10) {
    // Generates the negative space for perfectly flush flat-head aerospace screws
    union() {
        cylinder(h=depth, r=hole_r, center=true);
        translate([0, 0, (depth / 2) - head_h])
            cylinder(h=head_h + 0.1, r1=hole_r, r2=head_r);
    }
}

module luxury_flush_case_top() {
    color("DimGray")
    difference() {
        // Main outer shell
        rounded_box(case_length, case_width, case_height, corner_radius);

        // Hollow interior cavity for the silicon
        translate([wall_thickness, wall_thickness, -1])
            rounded_box(case_length - (wall_thickness * 2), case_width - (wall_thickness * 2), case_height - wall_thickness + 1, corner_radius - 2);

        // Four countersunk flush mounting holes
        positions = [
            [corner_radius, corner_radius],
            [case_length - corner_radius, corner_radius],
            [corner_radius, case_width - corner_radius],
            [case_length - corner_radius, case_width - corner_radius]
        ];

        for (pos = positions) {
            translate([pos[0], pos[1], case_height / 2])
                flush_countersink(hole_r=2.5, head_r=5.5, head_h=3.5, depth=case_height + 2);
        }

        // Flush wiring egress port, heavily filleted to prevent cable chafing
        translate([case_length / 2, 0, 5])
        rotate([90, 0, 0])
        hull() {
            translate([-12, 0, 0]) cylinder(h=10, r=4, center=true);
            translate([12, 0, 0]) cylinder(h=10, r=4, center=true);
        }
    }
}

module interior_shock_mounts() {
    // Shock absorbers mapped exactly beneath the flush casing mounting posts
    positions = [
        [corner_radius, corner_radius],
        [case_length - corner_radius, corner_radius],
        [corner_radius, case_width - corner_radius],
        [case_length - corner_radius, case_width - corner_radius]
    ];

    for (pos = positions) {
        translate([pos[0], pos[1], 4])
            pcb_standoff_shock(height=8); 
    }
}

// Execute Machine Render
luxury_flush_case_top();
interior_shock_mounts();
