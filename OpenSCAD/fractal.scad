sides = 3;
scale = .1;
size = 10;
levels = 5;
$fn = 20;

module tube(p1, p2, s){
    hull() {
      translate(p1) sphere(r=s);
      translate(p2) sphere(r=s);
   }
}

module shape(sz, sc, pos){
    translate(pos){
        for(e=[1:2:sides]){
            tube([sin((360 / sides) * e) * sz, cos((360 / sides) * e) * sz, 0]);
            translate([sin((360 / sides) * (e + 1)) * sz, cos((360 / sides) * (e  + 1)) * sz, 0])sphere(sc);
        }
    }
}

module _draw(l){
    for(e=[1:1:l]){
        for(i=[0:1:sides]){
            rotate([0, 0, i * (360 / sides)])shape(size / (e + 1) / l, scale / (e + 1) / l, [cos(i * (360 / sides)) * l * l, sin(i * (360 / sides)) * l * l, l]);
            _draw(l - 1);
        }
    }
}
module draw(l){
    shape(size, scale, [0, 0, 0]);
    _draw(l - 1);
}

draw(5);