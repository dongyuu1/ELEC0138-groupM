import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import pickle
import os


def train_model():
    #if os.path.exists("ddos_model.pickle") and os.path.exists("scaler.pickle"):
    #    print("Already detected trained model")
    #    return

    clf = KNeighborsClassifier()
    scaler = MinMaxScaler()
    imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    data_df = pd.read_csv("dataset_sdn.csv")
    x_train, x_test, y_train, y_test = preprocess_data(data_df, imputer)

    print("Training model for Ddos detection")
    clf.fit(scaler.fit_transform(x_train), y_train)

    y_pred = clf.predict(scaler.transform(x_test))

    print("The confusion matrix is: ")
    print(confusion_matrix(y_pred, y_test))
    print("The accuracy of the model is: {}".format(accuracy_score(y_pred, y_test)))

    pickle.dump(clf, open('./ddos_model.pickle', 'wb'))
    print("Model is saved at ./ddos_model.pickle")

    pickle.dump(scaler, open('./scaler.pickle', 'wb'))
    print("Scaler is saved at ./scaler.pickle")


def preprocess_data(df, imputer):
    df = df.join(pd.get_dummies(df.Protocol))
    labels = np.array(df["label"])
    input_df = df.drop(["src", "dst", "dt", "switch", "Protocol", "label", "dur_nsec","tot_dur", "flows", "packetins","pktperflow",
                        "byteperflow","pktrate","Pairflow","port_no","tx_bytes","rx_bytes","tx_kbps", "rx_kbps",
                        "tot_kbps"], axis=1).astype("float64")
    print(input_df)
    inputs = imputer.fit_transform(input_df)

    x_train, x_test, y_train, y_test = train_test_split(inputs, labels, test_size=0.25)
    return x_train, x_test, y_train, y_test


def detect_ddos(input):
    if not (os.path.exists("ddos_model.pickle") and os.path.exists("scaler.pickle")):
        print("No available pre-trained model")
        return
    else:
        clf = pickle.load(open('./ddos_model.pickle', 'rb'))
        scaler = pickle.load(open('./scaler.pickle', 'rb'))
        y_pred = clf.predict(scaler.transform(input))
        # Return Ture if a ddos attack is detected
        if y_pred > 0.5:
            return True
        else:
            return False


if __name__ == '__main__':
    train_model()
    #simulated_data = np.random.rand(1, 18) # batch_size * number of features
    #pred = detect_ddos(simulated_data)
    #print(pred)
