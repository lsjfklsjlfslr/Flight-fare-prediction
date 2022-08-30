from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
import json
import shutil

from Raw_Data_Validation.Raw_Data_Validation_Training import Raw_Data_Validation_Training
from Raw_Data_Validation.Raw_Data_Validation_Testing import Raw_Data_Validation_Testing

import logging
from Data_Preprocessing.data_preprocessing import dataPreprocessing
from Files_For_Prediction.prediction import predict
from Cassandra_DB_Folder.General_DB_func import All_DB_func
from Model_Training.model_training import trainModel

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)

CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        logging.basicConfig(filename='All_logs/Testing_logs.log',
                            filemode='w',
                            level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(module)s---- %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger('')
        f = open('All_logs/Testing_logs.log', 'w')
        f.truncate()
        f.close()

        if request.form is not None:

            clients_path = request.form['filepath']
            if os.path.isdir(clients_path + '/Output_Files/'):
                shutil.rmtree(clients_path + '/Output_Files')
                logger.info('Deleted Existing Output_Files In path specified')

            # path is just a folder name in which raw data are kept

            obj = Raw_Data_Validation_Testing(clients_path + '/', 'Testing_Schema.json', logger, f.name)
            G_path = obj.start_validation()  # G_path is Good Data folder path

            obj = dataPreprocessing(logger, G_path, f.name, clients_path)
            preprocessed_data_path = obj.start_preprocessing_for_testing()

            obj = predict(preprocessed_data_path, logger, G_path, f.name, clients_path)
            json_predictions = obj.start_prediction()
            shutil.copy(f.name, clients_path + '/' + 'logfile.txt')

            return Response(
                "Prediction File created at !!!" + str(clients_path) + ' and few of the predictions are ' + str(
                    json.loads(json_predictions)))
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        logging.basicConfig(filename='All_logs/Training_logs.log',
                            filemode='w',
                            level=logging.INFO,
                            format='%(asctime)s %(levelname)s ---- %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger('')

        f = open('All_logs/Training_logs.log', 'w')
        f.truncate()
        f.close()

        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            # path is just a folder name in which raw data are kept

            obj = Raw_Data_Validation_Training(path + '/', 'Training_Schema.json', logger, f.name)
            G_path = obj.start_validation()

            # Now our files are moved to Good Data and Bad Data folders
            # Its time for uploading data to cloud storage

            obj = All_DB_func(logger, G_path, path, f.name)
            train_path = obj.start_db()

            obj = dataPreprocessing(logger, train_path, f.name, path)
            preprocessed_data_path = obj.start_preprocessing_for_training()

            obj = trainModel(logger, preprocessed_data_path, f.name, path)
            obj.start_training()
            shutil.copy(f.name, path + '/' + 'logfile.txt')

            if os.path.isdir(path + '/' + 'Models_plot'):
                shutil.rmtree(path + '/' + 'Models_plot/')
                os.makedirs(path + '/' + 'Models_plot/')
            else:
                os.makedirs(path + '/' + 'Models_plot/')

            for plot in os.listdir('Models_plot/'):
                shutil.copy('Models_plot' + '/' + plot, path + '/Models_plot/')

    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successful!!")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port)
