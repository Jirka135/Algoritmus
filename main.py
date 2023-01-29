from flask import Flask, render_template, request
import random
import matplotlib
matplotlib.use('agg')  # new line
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__, template_folder='static')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/plot', methods=['POST'])
def plot():
    #definice seznamů
    serazene = []
    n_cisla = []

    #req z formuláře
    nejmensi = int(request.form['nejmensi'])
    nejvetsi = int(request.form['nejvetsi'])
    cisel = int(request.form['cisel'])
    #naplnění
    def napl_cisly(cisla,c1,c2):
        while len(cisla) < cisel:
            cisla.append(random.randint(c1,c2))

    napl_cisly(n_cisla,nejmensi,nejvetsi)
    #sorting
    for c in n_cisla:
        if not serazene:
            serazene.append(c)
        else:
            for i in range(len(serazene)):
                if c < serazene[i]:
                    serazene.insert(i, c)
                    break
            else:
                serazene.append(c)
    #labely
    labels = list(set(serazene))
    plt.clf()
    plt.bar(labels, [serazene.count(x) for x in labels],label='čísla')
    plt.title('Graf čísel')

    #buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode()


    return render_template('form.html', plot_url=plot_url)