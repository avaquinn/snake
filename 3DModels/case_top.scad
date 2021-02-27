length = 105;
width = 76;
thickness = 2.5;
screw_hole_width = 66.85;
screw_hole_length = 96.96;
diameter_screw_hole = 3;
viewport_size = 45;

screw_hole_border_width = (width - screw_hole_width) / 2;

module viewport()
{
    distance_from_edge = 11.5;
    
    translate([distance_from_edge, (width - viewport_size) / 2, 0])
        cube([viewport_size, viewport_size, thickness]);
}
module top()
{
    cube([length, width, thickness]);
}
module screw_hole(x, y, z)
{
    $fn = 15;
    translate([x, y, z])
        #cylinder(thickness, d = diameter_screw_hole);
}

difference()
{
    top();
    screw_hole(screw_hole_border_width, screw_hole_border_width, 0);
    #screw_hole(length - screw_hole_border_width, screw_hole_border_width, 0);
    screw_hole(screw_hole_border_width, width -screw_hole_border_width, 0);
    screw_hole(length - screw_hole_border_width, width -screw_hole_border_width, 0);
    viewport();
}
    