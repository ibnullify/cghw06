from display import *
from draw import *
from parser import *
from matrix import *
import math

screen = new_screen()
color = [ 0, 255, 0 ]
edges = []
transform = new_matrix()

# print_matrix( make_bezier() )
# print
# print_matrix( make_hermite() )
# print

ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus' ]

#I consistently get an error importing parser
def parse_file( fname, edges, transform, screen, color ):

    f = open(fname)
    lines = f.readlines()

    step = 100
    c = 0
    while c < len(lines):
        line = lines[c].strip()
        #print ':' + line + ':'

        if line in ARG_COMMANDS:
            c+= 1
            args = lines[c].strip().split(' ')

        if line == 'circle':
            #print 'CIRCLE\t' + str(args)
            add_circle(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)

        elif line == 'hermite' or line == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            add_curve(edges,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)                      
            
        elif line == 'line':            
            #print 'LINE\t' + str(args)

            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )

            
        #NEW CODE INCOMING
        #step is already defined above

        #add_box( points, x, y, z, width, height, depth ):
        elif line == 'box':
            add_box(edges,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]) )

        #add_sphere( points, cx, cy, cz, r, step ):
        elif line == 'sphere':
            add_sphere(edges,
                       float(args[0]), float(args[1]),
                       float(args[2]), float(args[3]), step)

        #add_torus( points, cx, cy, cz, r0, r1, step ):
        elif line == 'torus':
            add_torus(edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step)

        #clear
        elif line == 'clear':
            edges = new_matrix()
        #END OF INCOMING NEW CODE

        
        elif line == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(t, transform)

        elif line == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(t, transform)

        elif line == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(t, transform)
                
        elif line == 'ident':
            ident(transform)

        elif line == 'apply':
            matrix_mult( transform, edges )

        elif line == 'display' or line == 'save':
            clear_screen(screen)
            draw_lines(edges, screen, color)

            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
            
        c+= 1


parse_file( 'script', edges, transform, screen, color )
