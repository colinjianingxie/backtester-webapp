
from datetime import datetime as dt, timedelta as td
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import (
	LinearDiscriminantAnalysis as LDA,
	QuadraticDiscriminantAnalysis as QDA
)
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC, SVC
from sklearn.model_selection import train_test_split, KFold, GridSearchCV, ParameterGrid
#from sklearn.grid_search import ParameterGrid
from main.pricing.helpers.get_daily_prices import get_daily_prices
from main.pricing.helpers.basic_input import call_basic_security_input
from main.pricing.helpers.lagged_series import create_lagged_series

def generate_confusion_matrix(ticker_names, start_date, end_date, vendor_name):
	snpret = create_lagged_series(ticker_names, start_date, end_date, lags=5, column_name='adj_close_price', additional_columns=['volume'], vendor_name=vendor_name)
	# Use the prior two days of returns as predictor # values, with direction as the response
	X = snpret[['Lag1', 'Lag2']]
	y = snpret['Direction']

	# The test data is split into two parts: Before and after 1st Jan 2017.

	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.8, random_state=42
	)
	'''
	kf = KFold(
		n_splits=10, shuffle=True, random_state=42
	)
	'''

	# Models example..
	'''
	models = [
	('LR - Logistic Regression', LogisticRegression(solver='liblinear')),
	('LDA', LDA(solver='svd')),
	('QDA - Quadratic Discriminant Analyser', QDA()),
	('LSVC', LinearSVC(max_iter=10000)),
	('RSVM', SVC(C=1000000.0,
		cache_size=200,
		class_weight=None,
		coef0=0.0,
		degree=3,
		gamma=0.0001,
		kernel='rbf',
		max_iter=-1,
		probability=False,
		random_state=None,
		shrinking=True,
		tol=0.001,
		verbose=False
	)),
	('RF', RandomForestClassifier(
		n_estimators=1000,
		criterion='gini',
		max_depth=None,
		min_samples_split=2,
		min_samples_leaf=1,
		max_features='auto',
		bootstrap=True,
		oob_score=False,
		n_jobs=1,
		random_state=None,
		verbose=0))
	]
	'''

	tuned_parameters = [{'kernel': ['rbf'], 'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}]

	model = GridSearchCV(SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, degree=3,  tol=0.001), tuned_parameters, cv=10, return_train_score=True)
	model.fit(X_train, y_train)
	print("Optimised parameters found on training set:")
	print(model.best_estimator_, "\n")
	print("Grid scores calculated on training set:")
	for mean_score, params in zip(model.cv_results_['mean_train_score'], model.cv_results_['params']):
		print("%0.3f for %r" % (mean_score, params))


	'''
	# For cross validation example....
	for train_index, test_index in kf.split(X):
		X_train = X.loc[X.index[train_index]]
		X_test = X.loc[X.index[test_index]]
		y_train = y.loc[y.index[train_index]]
		y_test = y.loc[y.index[test_index]]

		# Create the (parametrised) models
		print('Hit Rates/Confusion Matrices:\n')
		# Iterate through the models
		# print([['Correct Up Periods', 'Incorrect Up Periods'],['Incorrect Down Periods', 'Correct Down Periods']])
		for m in models:
			# Train each of the models on the training set
			m[1].fit(X_train, y_train)
			# Make an array of predictions on the test set
			pred = m[1].predict(X_test)
			# Output the hit-rate and the confusion matrix for each model
			print(f'{m[0]}:\n{m[1].score(X_test, y_test):.3f}')
			print(f'{confusion_matrix(pred, y_test)}\n')
		print("-------------------")
	'''

def perform_confusion_matrix():
	#ticker_names, start_date, end_date = call_basic_security_input()
	ticker_names=['SPY']
	start_date = '2016-01-10'
	end_date = '2017-12-31'
	start_date = dt.strptime(start_date, "%Y-%m-%d")
	end_date = dt.strptime(end_date, "%Y-%m-%d")

	generate_confusion_matrix(ticker_names, start_date, end_date, vendor_name='Yahoo Finance')
