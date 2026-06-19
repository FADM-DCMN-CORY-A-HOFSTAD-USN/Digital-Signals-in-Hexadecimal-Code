// =================================================================
// TYPE-S SAIYA AVIONICS MOTHERBOARD (ATX FORM FACTOR)
// =================================================================

atx_width = 244;
atx_length = 305;
pcb_thickness = 2.4;

module atx_base() {
    difference() {
        // Main PCB
        color("DarkSlateGray")
        cube([atx_width, atx_length, pcb_thickness]);
        
        // Standard ATX Mounting Holes
        mounting_positions = [
            [6.35, 6.35], [6.35, 165], [6.35, 285],
            [165, 6.35], [165, 165], [165, 285],
            [238, 6.35], [238, 165], [238, 285]
        ];
        
        for (pos = mounting_positions) {
            translate([pos[0], pos[1], -1])
            cylinder(h=pcb_thickness+2, r=2, $fn=30);
        }
    }
}

module hex_components() {
    // 1. Central CPU / Optical Router Socket
    color("Gold") translate([120, 220, pcb_thickness]) cube([50, 50, 4], center=true);
    
    // 2. RAM Slots (DDR5 / CAMM2)
    color("DimGray") translate([180, 220, pcb_thickness]) cube([8, 130, 8], center=true);
    color("DimGray") translate([200, 220, pcb_thickness]) cube([8, 130, 8], center=true);
    
    // 3. PCIe Slot (For the AG-Bridge Plate Controller)
    color("DodgerBlue") translate([120, 80, pcb_thickness]) cube([140, 12, 10], center=true);
    
    // 4. M.2 Slot (For the ECLSS Manager)
    color("Silver") translate([60, 140, pcb_thickness]) cube([22, 80, 3], center=true);
    
    // 5. Jamoni Crystal Mount (Custom Hex Socket)
    color("Cyan", 0.8) translate([60, 40, pcb_thickness]) cylinder(h=15, r=18, $fn=6);
}

atx_base();
hex_components();
