
from flask import Flask, request, render_template_string
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load model
MODEL_PATH = "xg.pkl"

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Insurance Cost Predictor</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Segoe UI',sans-serif;
}

body{
    min-height:100vh;
    background:linear-gradient(135deg,#667eea,#764ba2,#f093fb);
    background-size:400% 400%;
    animation:gradient 12s ease infinite;
    display:flex;
    justify-content:center;
    align-items:center;
    overflow-x:hidden;
    padding:30px;
}

@keyframes gradient{
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
}

.container{
    width:100%;
    max-width:1050px;
    background:rgba(255,255,255,.15);
    backdrop-filter:blur(18px);
    border:1px solid rgba(255,255,255,.25);
    border-radius:28px;
    padding:35px;
    box-shadow:0 20px 60px rgba(0,0,0,.25);
}

.header{
    text-align:center;
    color:white;
    margin-bottom:30px;
}

.header h1{
    font-size:38px;
    margin-bottom:8px;
}

.header p{
    font-size:17px;
    opacity:.9;
}

.form-grid{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:22px;
}

.card{
    background:rgba(255,255,255,.9);
    border-radius:18px;
    padding:20px;
    box-shadow:0 8px 25px rgba(0,0,0,.12);
}

.card label{
    display:block;
    font-weight:600;
    color:#333;
    margin-bottom:8px;
}

input,select{
    width:100%;
    padding:13px;
    border-radius:12px;
    border:1px solid #ddd;
    font-size:15px;
    outline:none;
    transition:.3s;
}

input:focus,select:focus{
    border-color:#764ba2;
    box-shadow:0 0 0 3px rgba(118,75,162,.15);
}

.predict-btn{
    margin-top:28px;
    width:100%;
    padding:17px;
    border:none;
    border-radius:16px;
    background:linear-gradient(135deg,#ff512f,#dd2476);
    color:white;
    font-size:20px;
    font-weight:bold;
    cursor:pointer;
    transition:.3s;
    position:relative;
    overflow:hidden;
}

.predict-btn:hover{
    transform:translateY(-3px);
    box-shadow:0 10px 30px rgba(221,36,118,.4);
}

.result{
    margin-top:28px;
    background:linear-gradient(135deg,#11998e,#38ef7d);
    padding:22px;
    border-radius:18px;
    color:white;
    text-align:center;
    animation:pop .6s ease;
}

@keyframes pop{
    0%{transform:scale(.5);opacity:0}
    100%{transform:scale(1);opacity:1}
}

.result h2{
    font-size:22px;
    margin-bottom:10px;
}

.price{
    font-size:38px;
    font-weight:bold;
}

.footer{
    margin-top:22px;
    text-align:center;
    color:white;
    font-size:13px;
    opacity:.8;
}

.balloon{
    position:fixed;
    bottom:-120px;
    width:55px;
    height:70px;
    border-radius:50%;
    animation:floatUp 6s linear forwards;
    z-index:9999;
}

.balloon:after{
    content:'';
    position:absolute;
    width:2px;
    height:55px;
    background:white;
    left:50%;
    top:68px;
}

@keyframes floatUp{
    0%{
        transform:translateY(0) rotate(0deg);
        opacity:1;
    }
    100%{
        transform:translateY(-115vh) rotate(360deg);
        opacity:0;
    }
}

@media(max-width:700px){
    .form-grid{
        grid-template-columns:1fr;
    }

    .header h1{
        font-size:28px;
    }

    .container{
        padding:20px;
    }
}

</style>

</head>

<body>

<div class="container">

<div class="header">
    <h1>🏥 Insurance Cost Predictor</h1>
    <p>Predict your estimated medical insurance charges using Machine Learning</p>
</div>

<form method="POST" onsubmit="launchBalloons()">

<div class="form-grid">

<div class="card">
<label>Age</label>
<input type="number" name="age" placeholder="Enter age" required min="1" max="100">
</div>

<div class="card">
<label>Sex</label>
<select name="sex" required>
<option value="">Select Gender</option>
<option value="0">Female</option>
<option value="1">Male</option>
</select>
</div>

<div class="card">
<label>BMI</label>
<input type="number" step="0.01" name="bmi" placeholder="Enter BMI" required>
</div>

<div class="card">
<label>Children</label>
<input type="number" name="children" placeholder="Number of children" required min="0" max="10">
</div>

<div class="card">
<label>Smoker</label>
<select name="smoker" required>
<option value="">Select</option>
<option value="0">No</option>
<option value="1">Yes</option>
</select>
</div>

<div class="card">
<label>Region</label>
<select name="region" required>
<option value="">Select Region</option>
<option value="0">Northeast</option>
<option value="1">Northwest</option>
<option value="2">Southeast</option>
<option value="3">Southwest</option>
</select>
</div>

</div>

<button class="predict-btn" type="submit">
✨ Predict Insurance Cost
</button>

</form>

{% if prediction is not none %}

<div class="result">
    <h2>🎉 Predicted Insurance Charges</h2>
    <div class="price">₹ {{ prediction }}</div>
    <p style="margin-top:8px;">Thank you for using our AI prediction system 💜</p>
</div>

{% endif %}

<div class="footer">
Built with Flask • XGBoost • Render Deployment 🚀
</div>

</div>


<script>

function launchBalloons(){

    let colors=[
        '#ff4d6d',
        '#ffbe0b',
        '#8338ec',
        '#3a86ff',
        '#06d6a0',
        '#fb5607'
    ];

    for(let i=0;i<35;i++){

        let balloon=document.createElement("div");

        balloon.className="balloon";

        balloon.style.left=Math.random()*100+"vw";

        balloon.style.background=
        colors[Math.floor(Math.random()*colors.length)];

        balloon.style.animationDuration=
        (4+Math.random()*3)+"s";

        document.body.appendChild(balloon);

        setTimeout(()=>{
            balloon.remove();
        },7000);

    }

}

</script>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None

    if request.method == "POST":

        age = float(request.form["age"])
        sex = int(request.form["sex"])
        bmi = float(request.form["bmi"])
        children = int(request.form["children"])
        smoker = int(request.form["smoker"])
        region = int(request.form["region"])

        features = pd.DataFrame(
            [[age, sex, bmi, children, smoker, region]],
            columns=["Age", "Sex", "BMI", "Children", "Smoker", "Region"]
        )

        pred = model.predict(features)[0]

        prediction = round(float(pred), 2)

    return render_template_string(HTML, prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)
