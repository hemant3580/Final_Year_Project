

from flask import Flask, request, render_template
import pickle


model = pickle.load(open('PCASSS_model.pkl', 'rb'))
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inspect", methods=["GET", "POST"])
def inspect():
    if request.method == "POST":
        GlobalReactivePower = float(request.form['GlobalReactivePower'])
        Global_intensity = float(request.form['Global_intensity'])
        Sub_metering_1 = float(request.form['Sub_metering_1'])
        Sub_metering_2 = float(request.form['Sub_metering_2'])
        Sub_metering_3 = float(request.form['Sub_metering_3'])
        x = [[GlobalReactivePower, Global_intensity, Sub_metering_1, Sub_metering_2, Sub_metering_3]]
        output = str(round(model.predict(x)[0], 3))
        conversation = []
        prompt = 'assuming the global active power is '+output+ ' watts and the average global active power is 10 watts, the carbon footprint in India can be estimated to be approximately '+output+ ' kilograms of CO2 per hour.watts'
        conversation.append({'role': 'user', 'content': prompt})
        #conversation = ChatGPT_conversation(conversation)
        q = conversation[-1]['content'].strip()
        return render_template('output.html', output1=output,output2 = q)
    return render_template("inspect.html")

if __name__ == "__main__":
    app.run(debug=True)
