from flask import Flask, render_template, request
import global_align as g
import local_align as l
import fitting_align as f

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    g_score = None
    g_alignment = None
    f_score = None
    f_alignment = None
    l_score = None
    l_alignment = None
    if request.method == 'POST':
        keys = ['A', 'C', 'T', 'G', '-']
        delta = {}
        for i in range(len(keys)):
            delta[keys[i]] = {k : v for (k,v) in zip(keys, [1 if keys[i] == keys[j]  else -1 for j in range(len(keys))])}


        if request.form['action'] == "Global":
            gl_v = request.form['glb_aln'].upper()
            gl_w = request.form['glb_aln2'].upper()

            g_score, g_alignment = g.global_align(gl_v,gl_w,delta)

            # print(score,alignment)
        elif request.form['action'] == "Fitting":
            short = None
            ref = None

            fit_v = request.form['fit_aln'].upper()
            fit_w = request.form['fit_aln2'].upper()

            if(len(fit_v) <= len(fit_w)):
                short = fit_v
                ref = fit_w
            else:
                short = fit_w
                ref = fit_v
            f_score, f_alignment = l.local_align(short,ref,delta)
            # print(score,alignment)

        elif request.form['action'] == "Local":
            lcl_v = request.form['lcl_aln'].upper()
            lcl_w = request.form['lcl_aln2'].upper()

            l_score, l_alignment = l.local_align(lcl_v,lcl_w,delta)
            # print(score,alignment)

    return render_template("index.html", g_score=g_score, g_alignment=g_alignment, f_score=f_score, f_alignment=f_alignment, l_score=l_score, l_alignment=l_alignment)


if __name__ == '__main__':
    app.run()
