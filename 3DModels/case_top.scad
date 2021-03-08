length = 103.5;
width = 74.25;
thickness = 3.5;
screw_hole_width = 66.85;
screw_hole_length = 96.96;
diameter_screw_hole = 3.5;
viewport_size = 45;
snake_scale = 0.7;



screw_hole_border_width = (width - screw_hole_width) / 2;

module viewport()
{
    distance_from_edge = 11.5;
    
    translate([distance_from_edge, (width - viewport_size) / 2 +1.5, - thickness])
        cube([viewport_size - 4.5, viewport_size - 1.5, thickness * 3]);
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

module ava_text()
{
    translate([21, 5.5, 1.5])
        linear_extrude(3)
            #text("By Ava", size = 5);
    
}
module snake_text()
{
    translate([13, 63, 1.5])
        linear_extrude(3)
            #text("SNAKE", size = 8);
}

module snake_placer()
{
    translate([78, 38, 2])
        scale([snake_scale, snake_scale, snake_scale])
            rotate([90,0,0])
                import("STL_Snake.stl");
}
difference()
{
    top();
    screw_hole(screw_hole_border_width, screw_hole_border_width, 0);
    #screw_hole(length - screw_hole_border_width, screw_hole_border_width, 0);
    screw_hole(screw_hole_border_width, width -screw_hole_border_width, 0);
    screw_hole(length - screw_hole_border_width, width -screw_hole_border_width, 0);
    viewport();
    snake_text();
    ava_text();
}
snake_placer();