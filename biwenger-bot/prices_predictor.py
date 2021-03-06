import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from player import Player


class PricesPredictor:

    def __init__(self):
        self.days_to_lookback=3
        self.prediction_day=1

    #TODO MAKE TESTS WITH PAST VALUES AND TRY TO PREDICT THE RESULTS FROM THE CLOSE PAST
    def predict_price(self, player: Player):
        try:
            days_to_lookback = min(self.days_to_lookback, player.prices.__len__())
            x = [days_to_lookback + self.prediction_day]
            dates = range(days_to_lookback)
            prices = [x[1] for x in player.prices][-days_to_lookback:]
            x = np.reshape(x, (len(x), 1))
            dates = np.reshape(dates, (len(dates), 1)) # converting to matrix of n X 1
            svr_rbf = SVR(kernel='rbf', C=1e6, gamma=0.01)
            svr_poly = SVR(kernel='poly', C=1e6, degree=2, gamma='auto')
            svr_rbf.fit(dates, prices)  # fitting the data points in the models
            svr_poly.fit(dates, prices)

            dates_extended = range(days_to_lookback+5)
            dates_extended = np.reshape(dates_extended,(len(dates_extended), 1)) # converting to matrix of n X 1

            plt.scatter(dates, prices, color='k', label='Data') # plotting the initial datapoints
            plt.scatter(x, svr_rbf.predict(x), color='green')
            plt.scatter(x, svr_poly.predict(x), color='green')
            plt.plot(dates_extended, svr_rbf.predict(dates_extended), color='red', label='RBF model') # plotting the line made by the RBF kernel
            plt.plot(dates_extended, svr_poly.predict(dates_extended), color='blue', label='Polynomial model') # plotting the line made by polynomial kernel
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.title('Prediction for ' + player.name)
            plt.legend()
            plt.show()
            prediction_mean = (svr_rbf.predict(x)[0]+svr_poly.predict(x)[0])/2
            #prediction_mean = svr_rbf.predict(x)[0]
            return prediction_mean
        except Exception:
            print("ERROR: Couldn't predict price for this player")

