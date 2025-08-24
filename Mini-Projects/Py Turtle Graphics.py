import turtle as t 
from random import random as r 
 
t.mode("logo"),t.bgcolor(0,0,0) 
t.hideturtle() 
step, angle = 6, 30 
 
def f(t, l): 
   if l >= step: 
       t.color(r(), r(), r()) 
       t.forward(l) 
 
       lt = t.clone() 
       lt.left(angle) 
       f(lt, l-step) 
 
       rt = t.clone() 
       rt.right(angle) 
       f(rt, l-step) 
 
f(t, 60) 
t.exitonclick() 