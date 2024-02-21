from flask import Flask, render_template, request, redirect, url_for, session
import os
import shutil
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)  

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'images' not in session:
        session['images'] = os.listdir('static/images')

    if request.method == 'POST':
        image_name = request.form.get('image_name')
        choice = request.form.get('choice')
        drive_type = request.form.get('drive_type')

        if choice is None or drive_type is None:
            # Show an error message to the user
            return redirect(url_for('index'))
        os.makedirs(f'static/choices/{choice}', exist_ok=True)
        shutil.move(f'static/images/{image_name}', f'static/choices/{choice}/{image_name}')
        num = str(time.time()).replace('.','_')+'.jpg'
        os.rename(f'static/choices/{choice}/{image_name}', f'static/choices/{choice}/{num}')
        session['images'] = os.listdir('static/images')
        # os.makedirs(r"static/driveType.txt", exist_ok=True)
        with open(r"static/driveType.txt", 'a') as f:
            f.write(f'{num} : {drive_type}\n')

        return redirect(url_for('index'))


    image = session['images'][0] if session['images'] else None

    choices = os.listdir('static/choices')

    return render_template('index.html', image=image, choices=choices)

if __name__ == '__main__':
    app.run(debug=True)