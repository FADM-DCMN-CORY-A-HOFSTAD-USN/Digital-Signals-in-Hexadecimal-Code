/*
 * REVOLUTIONARY TECHNOLOGY: RT-HEX ACTIVE STYLUS
 * Material: Aerospace Grade Titanium & Carbon Fiber
 * Physics: Inductive Altitude/Azimuth Tracking & Strain-Gauge Pressure
 */

$fn = 64;

// Stylus Dimensions
length = 160;
diameter = 12;
nib_length = 8;
coil_length = 20;

module rt_stylus_nib() {
    // The active elastomer pressure tip
    color("DarkSlateGray") {
        translate([0, 0, -nib_length])
            cylinder(h=nib_length, r1=1, r2=diameter/2 - 1.5);
    }
}

module inductive_tracking_coil() {
    // Copper induction array that transmits the Azimuth/Altitude angles
    color("Gold") {
        translate([0, 0, 5])
            cylinder(h=coil_length, r=diameter/2 - 0.5);
    }
}

module titanium_chassis() {
    color("Silver") {
        difference() {
            // Main barrel
            cylinder(h=length, r=diameter/2);
            
            // Grip knurling (anti-slip in zero gravity)
            for (i = [0 : 45 : 315]) {
                rotate([0, 0, i])
                translate([diameter/2, 0, 15])
                    cylinder(h=40, r=0.5);
            }
            
            // Hollow out front for the coil and strain gauge
            translate([0, 0, -1])
                cylinder(h=30, r=diameter/2 - 1);
        }
        
        // Front bevel down to the nib
        translate([0, 0, 0])
            rotate([180, 0, 0])
            cylinder(h=5, r1=diameter/2, r2=diameter/2 - 1.5);
            
        // Eraser / Rear Inductive Latch
        translate([0, 0, length])
            sphere(r=diameter/2);
    }
}

module master_stylus() {
    titanium_chassis();
    rt_stylus_nib();
    inductive_tracking_coil();
}

master_stylus();
