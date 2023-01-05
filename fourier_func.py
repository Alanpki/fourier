from sympy import *
from flask import Flask, request, abort,render_template
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sympy.interactive import printing

def sympy_text(int_1,int_2,int_3,constant):
  n=100
  # create a x vector
  x = np.linspace(-5, 5, n) 
  # compute y
  y = int_1*(x**3) -int_2*(x**2) -int_3*x + constant

  plt.plot(x, y)
  plt.grid(True)
  plt.xlabel('X')
  plt.ylabel('Y')
  plt.title('Picturing')
  # plt.show()  # just for py file
  plt.savefig("static/1.png")
  plt.clf()
  #傅立葉轉換後

  printing.init_printing(use_latex=False)
  
  
  #在(-pi < x < pi)內用傅立葉級數Fourier Series模擬三次方多項式的線型
  x = symbols('x')
  f = Function('f')(x)

  f = int_1*x**3 -int_2*x**2 -int_3*x + constant
  #語法：fourier_series(要模擬的f函數, (x的範圍, -pi, pi))
  s = fourier_series(f, (x, -pi, pi))
  #不太可能去使用n=∞去計算，在實際計算時要截短級數truncate（指定n=數字）
  fs5 = s.truncate(n=5)
  
  out_put = plot(fs5) #畫圖
  backend = out_put.backend(out_put)
  backend.process_series()

  backend.fig.savefig("static/2.png",dpi=300)
  # print(type(fs5))
  plt.clf()
  return

# sympy_text(1,1,40,-1)

app = Flask(__name__)

@app.route("/draw",methods=["GET"])

def draw():
  try:
    int_1 =int(request.values['int_1'])
    int_2 =int(request.values['int_2'])
    int_3 =int(request.values['int_3'])
    constant =int(request.values['constant'])
    print(int_1,int_2,int_3,constant)
    sympy_text(int_1,int_2,int_3,constant)
  except Exception as e:
    print(e)  

  return render_template('draw.html')


if __name__ == "__main__":

  app.run()
  app._static_folder = "./static"
