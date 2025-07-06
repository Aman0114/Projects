import pickle
from flask import Flask, render_template,request,url_for


app = Flask(__name__)
model=pickle.load(open('model.pkl','rb'))
scaler=pickle.load(open('scaler.pkl','rb'))

with open('speciality_mapping.pkl', 'rb') as f:
    speciality_mapping = pickle.load(f)

# home html
@app.route('/',methods=['GET','POSt'])
def index():
    specialities = list(speciality_mapping.keys())
    return render_template('index.html', specialities=specialities)

@app.route('/predict', methods=['GET','POSt'])
def predict():
    city = request.form['city']
    speciality = request.form['speciality_of_doctor']
    qualification = request.form['qualification']
    # ...get other numeric fields...

    # One-hot encode city and qualification as per your model's feature order
    city_Delhi = 1 if city == 'Delhi' else 0
    city_Mumbai = 1 if city == 'Mumbai' else 0

    # One-hot encode qualification
    qual_list = ['BDS', 'BHMS', 'BPTh/BPT', 'MA', 'MBBS', 'MD', 'MS', 'Others']
    qual_onehot = [1 if qualification == q else 0 for q in qual_list]

    # Encode speciality
    speciality_encoded = speciality_mapping.get(speciality, 0)

    # Get other numeric fields from the form
    year_of_experiance = float(request.form['year_of_experiance'])
    dp_score = float(request.form['dp_score'])
    npv = float(request.form['npv'])

    # Arrange features in the same order as model training
    features = [
        city_Delhi, city_Mumbai, speciality_encoded,
        *qual_onehot, year_of_experiance, dp_score, npv
    ]

    input_scaled = scaler.transform([features])
    prediction = model.predict(input_scaled)
    output = int(round(prediction[0], -2))
    return render_template('index.html', prediction_text=f'Doctor Fee Prediction : {output}/-', specialities=list(speciality_mapping.keys()))    
 
if __name__=='__main__':
    app.run(debug=True)


