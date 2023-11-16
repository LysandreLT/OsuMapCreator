import json
import  numpy as np
from sklearn.model_selection import train_test_split

from tensorflow import keras

DATA_PATH = "MapCreator/datasets"

def load_data(data_path):
    with open(data_path,"r") as fp:
        data = json.load(fp)
    x=np.array(data["mfcc"])
    y = np.array(data["labels"])
    return x,y

def prepare_datasets(test_size, validation_size):
    # load data
    x, y = load_data(DATA_PATH)
    # create train/test split
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=test_size)

    # create train/validation split
    x_train,x_validation,y_train,y_validation = train_test_split(x_train,y_train, test_size=validation_size)



    return x_train, x_validation, x_test, y_train, y_validation, y_test


def build_model(input_shape):
    # create model
    model = keras.Sequential()
    model.add(keras.layers.Dense(dim,activation="softmax"))
    model.add(keras.layers.Dropout(0.3))
    # output layer




if __name__  == "__main__":
    # create train, validation and test sets
    x_train, x_validation, x_test, y_train, y_validation, y_test = prepare_datasets(0.25, 0.2 ) # test size and validation size / how much of the trainning set we wanna use

    # build the RNN net
    model = build_model(input_shape)

    # compile the network

    # train the RNN

    # evaluate the RNN on the test set

    # make prediction on a sample