# https://numpy.org/doc/stable/user/index.html
import numpy as np
import csv
# https://matplotlib.org/stable/tutorials/introductory/pyplot.html
import matplotlib.pyplot as plt
import matplotlib
# https://docs.python.org/3/library/random.html
import random
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
from flask import Flask,render_template,request,redirect,send_from_directory
from threading import Thread
import os
import base64
from io import BytesIO

def hw4(args):
  n = args
  if args == None:
    n = rand = random.randint(100, 200)
    
  # Init. normal distribution ( mean , standard_dev , n )
  cycles = np.random.normal(6000,2400,n)
  mem = np.random.normal(20,10,n)

  # check cycles for outliers
  cycle_min = 100000.0
  cycle_max = -100000.0
  for x in cycles:
    if x < 1001 or x > 10999:
      x = np.where(cycles==x)
      cycles[x] = 6000
    else :
      if x > cycle_max:
       cycle_max = int(x)
      if x < cycle_min:
       cycle_min = int(x)
        
  # Check memory for outliers
  cpu_min = 1000.0
  cpu_max = -1000.0
  for x in mem:
    if x < 2 or x > 98:
      x = np.where(mem==x)
      mem[x] = 20.00
    else :
      if x > cpu_max:
       cpu_max = int(x)
      if x < cpu_min:
       cpu_min = int(x)
  
  # Move to DICTIONARY DATA STRUCTURE for FAST LOOKUP's 
  map = {}
  for x in range(n):
    output_tuple = (x, cycles[x], mem[x])
    map.update({ x : output_tuple })
    
  # Create folder for assets
  path = "./templates"
  exist = os.path.exists(path)
  if not exist:
    os.makedirs(path)
    
  # EXPORT TO CSV for later use 
  with open('./templates/firebase.csv','w') as f:
    producer = csv.writer(f)
    producer.writerow('PCM')
    for x in map:
      producer.writerow(map[x])
  
  # Create HISTOGRAM for CPU Cycles
  fig, cycles_figure = plt.subplots(figsize = (10, 3))
  cycles_figure.hist(cycles, bins = n)
  fig.savefig("./templates/Cpu-cyles.png")

  # Create histogram for MEMORY Footprint
  fig2, mem_figure = plt.subplots(figsize = (10, 3))
  mem_figure.hist(mem, bins = n)
  fig2.savefig("./templates/Mem-footprint.png")

  # Create HTML for Histogram visualization
  tmpfile = BytesIO()
  fig.savefig(tmpfile, format='png')
  encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
  cycle_graph = '<html><script>alert("Sorry, it could take a moment to load while creating your histograms")</script><style>h3 {color:#1D4348;margin:5%}div{margin:5%}body{background-color:#ABEDF5}h1{text-align:center;margin-top:5%</style><body><div><h1>Process Simulator</h1>'+f"<h2 style=text-align:center>Total Processes: {n}</h2>"+f"<h3 style=padding-left:60px>Average CPU time:  {int(np.mean(cycles))} cycles</h3>"+f"<h3 style=padding-left:60px>Max CPU cycles: {cycle_max}</h3>"+f"<h3 style=padding-left:60px>Min CPU cycles: {cycle_min}</h3>"+'<div style=text-align:center><img src=\'data:image/png;base64,{}\'></div>'.format(encoded) 
  tmpfile = BytesIO()
  fig2.savefig(tmpfile, format='png')
  encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
  memory_graph = f"<h3 style=padding-left:60px>Average Memory Footprint: {int(np.mean(mem))} kB's</h3>"+f"<h3 style=padding-left:60px>Max Memory: {cpu_max}kB's</h3>"+f"<h3 style=padding-left:60px>Min Memory: {cpu_min}kB's</h3>"+'<div style=text-align:center><img src=\'data:image/png;base64,{}\'></div></div></body></html>'.format(encoded) 
  
  cycle_graph = cycle_graph  + ( memory_graph )
  with open('./templates/render.html','w') as f:
      f.write( cycle_graph)

  # Show Histogram
app = Flask(__name__)
@app.route("/")
def index():
  # Set number of simulations desired as the value for rand
  # then press run!
  rand = random.randint(500, 1000)
  hw4(rand)
  return render_template('render.html')

def run():
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(host='0.0.0.0', port=7000)


t = Thread(target=run)
t.start() 