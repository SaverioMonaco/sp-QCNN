# Animation, see: 
# You must have manim installed to compile this
# to render this:
#      manim -pqk spQCNNanim.py Render 

from manim import *

class spQCNNanim(Scene):
   """
   Animation of the construction of a spQCNN circuit for 8 qubits
   (animation from left to right)
   """ 
   def construct(self):
      x0 = -6
      x1 = -3
      x2 = -1
      x3 = +1.5
      x4 = +2.5
      x5 = +5
      x6 = +5.5

      ########
      # |0>s #
      ########
      write_state0 = AnimationGroup(*tuple([Write(MathTex(r"|0\rangle", font_size=48).move_to([-6.5,-3.5+wire,0])) 
                           for wire in range(8)]) )

      #########
      # WIRES #
      #########
      def extrude(start_x, end_x):
         qs = []
         for wire in range(0,8,1):
            qs.append(Line(start=[start_x, -3.5+wire, 0.], end=[end_x, -3.5+wire, 0.], buff=0))

         return tuple([Create(q) for q in qs])

      create_wires0 = tuple([Create(Line(start=[x0, -3.5+wire, 0.], end=[x1, -3.5+wire, 0.]), rate_functions=linear)
                           for wire in range(8)]) 
      # First split
      split_wires0 = []
      # Even wires go up
      for i, wire in enumerate(range(0,8,2)):
         split_wires0.append(Create(Line(start=[x1, -3.5+wire, 0.], end=[x2, -3.5+i, 0.], buff=0)))
      # Odd wires go down
      for i, wire in enumerate(range(1,8,2)):
         split_wires0.append(Create(Line(start=[x1, -3.5+wire, 0.], end=[x2, +.5+i, 0.],  buff=0)))
      split_wires0 = tuple(split_wires0)

      # Extrude
      extrude_wires0 = extrude(x2, x3)

      # Second split
      split_wires1 = []
      for i, wire in enumerate(range(0,4,2)):
         split_wires1.append(Create(Line(start=[x3, -3.5+wire, 0.],     end=[x4, -3.5+i, 0.], buff=0)))
         split_wires1.append(Create(Line(start=[x3, -3.5+wire + 4, 0.], end=[x4, -3.5+i + 4, 0.], buff=0)))
      for i, wire in enumerate(range(1,4,2)):
         split_wires1.append(Create(Line(start=[x3, -3.5+wire, 0.],    end=[x4, -1.5+i, 0.], buff=0)))
         split_wires1.append(Create(Line(start=[x3, -3.5+wire+ 4, 0.], end=[x4, -1.5+i + 4, 0.], buff=0)))

      split_wires1 = tuple(split_wires1)

      # Extrude
      extrude_wires1 = extrude(x4, x5)
     
      w0 = AnimationGroup(*create_wires0)
      w1 = AnimationGroup(*split_wires0)
      w2 = AnimationGroup(*extrude_wires0)
      w3 = AnimationGroup(*split_wires1)
      w4 = AnimationGroup(*extrude_wires1)

      wires = Succession(w0, w1, w2, w3, w4, rate_functions=linear)

      ###############
      # MEASUREMENT #
      ###############
      write_zs = []
      for wire in range(8):
         write_zs.append(Write(MathTex(r"\langle z \rangle", font_size=48).move_to([x6,-3.5+wire,0])))
      write_zs = tuple(write_zs)
      write_zs = AnimationGroup(*write_zs)

      #############
      # UNITARIES #
      #############
      def createU(num = 0, height = 8, width=1.5, x = -4.5, y = 0):
         # Make layer 0 
         U = Rectangle(color=BLACK, height=height, width=width).move_to([x, y, 0])
         Uanim = (Create(U), U.animate.set_fill(WHITE, opacity = .8), Write(MathTex(rf"V_{num}", font_size=48, color=BLACK).move_to([x,y,0])) )

         return Uanim 

      U0 = AnimationGroup(*createU())
      U1 = AnimationGroup(*( createU(1, 3.6, 1.5, .25, 2) + createU(1, 3.6, 1.5, .25, -2)))
      U2 = AnimationGroup(*( createU(2, 1.6, 1, 3.75, -3) + createU(2, 1.6, 1, 3.75,  3) + createU(2, 1.6, 1, 3.75,  1) + createU(2, 1.6, 1, 3.75, -1)))
      self.play(write_state0)
      self.play(wires, Succession(U0,U1,U2, lag_ratio=2))
      self.play(write_zs)

