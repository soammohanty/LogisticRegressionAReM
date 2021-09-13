# importing the necessary dependencies
from flask import Flask, render_template, request
from flask_cors import cross_origin
import pickle

application = Flask(__name__)  # initializing a flask app


# app=application
@application.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@application.route('/predict', methods=['POST', 'GET'])  # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            avg_rss12 = float(request.form['avg_rss12'])
            var_rss12 = float(request.form['var_rss12'])
            avg_rss13 = float(request.form['avg_rss13'])
            var_rss13 = float(request.form['var_rss13'])
            avg_rss23 = float(request.form['avg_rss23'])
            var_rss23 = float(request.form['var_rss23'])

            filename = 'modelFile.sav'
            loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from the storage
            # predictions using the loaded model file
            prediction = loaded_model.predict(
                [[avg_rss12, var_rss12, avg_rss13, var_rss13, avg_rss23, var_rss23]])
            print('prediction is', prediction)

            posture = 'Cant Detect the posture'
            if prediction == 0:
                posture = 'bending1'
            elif prediction == 1:
                posture = 'bending2'
            elif prediction == 2:
                posture = 'cycling'
            elif prediction == 3:
                posture = 'lying'
            elif prediction == 4:
                posture = 'sitting'
            elif prediction == 5:
                posture = 'standing'
            else:
                posture = 'walking'

                # showing the prediction results in a UI
            return render_template('results.html', prediction=posture)
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')


if __name__ == "__main__":
    application.run(debug=True)  # running the app
