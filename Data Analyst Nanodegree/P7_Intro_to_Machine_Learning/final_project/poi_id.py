#!/usr/bin/python

"""
This is a script that preprocess data and creates algorithms that
can be used for prediction of fraud persons of interest (POI).
The script contains:
- Creation of new features function
- Outliers removal
- Feature split of data to train/test sets
- Testing of various algorithms
- SelectKBest and MinMaxScaler operations for selecting and scaling features
- Easy algorithm tuning with grid search in a pipeline
It generates classifier and data files so anyone can check the results.
"""

import sys
import pickle
sys.path.append("./tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi',
                 'exercised_stock_options',
                 'total_stock_value',
                 'bonus',
                 'salary',
                 'fraction_to_poi',
                 #'deferred_income',
                 #'long_term_incentive',
                 #'restricted_stock',
                 #'total_payments',
                 #'shared_receipt_with_poi',
                 #'loan_advances'
                ]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop('TOTAL')
data_dict.pop('THE TRAVEL AGENCY IN THE PARK')
data_dict.pop('LOCKHART EUGENE E')

### Task 3: Create new feature(s)
# Create a function that computes the fraction_to_poi or fraction_from_poi.
def computeFraction( poi_messages, all_messages ):
    ### take care of "NaN" when there is no known email address (and so
    ### no filled email features), and integer division.
    ### in case of poi_messages or all_messages having "NaN" value, return 0.
    fraction = 0
    if poi_messages == "NaN" or all_messages == "NaN":
        return fraction
    else:
        fraction = float(poi_messages)/float(all_messages)
        
    return fraction

for name in data_dict:

    data_point = data_dict[name]

    from_poi_to_this_person = data_point["from_poi_to_this_person"]
    to_messages = data_point["to_messages"]
    fraction_from_poi = computeFraction( from_poi_to_this_person, to_messages )
    data_point["fraction_from_poi"] = fraction_from_poi

    from_this_person_to_poi = data_point["from_this_person_to_poi"]
    from_messages = data_point["from_messages"]
    fraction_to_poi = computeFraction( from_this_person_to_poi, from_messages )
    data_point["fraction_to_poi"] = fraction_to_poi

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# Scale features.
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
features = scaler.fit_transform(features)

# Split data to train/test sets.
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 4: Try a variety of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
import warnings; warnings.simplefilter('ignore')
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import classification_report
from time import time

# Instantiate the pipeline steps
select = SelectKBest()
nb = GaussianNB()
svc = SVC()
dtc = DecisionTreeClassifier()
knc = KNeighborsClassifier()
rfc = RandomForestClassifier()
abc = AdaBoostClassifier()

# Make a dictionary of classifiers
classifiers = {"GaussianNB": nb, "SVM": svc, "Decision Tree": dtc, 
               "KNN": knc, "Random Forest": rfc, "AdaBoost": abc}

# Create a function that combines pipeline and grid search and returns the best clf with the best parameters
def optimize_clf(clf, parameters, n_splits):
    t0 = time()
    # Add pipeline steps into a list
    steps = [('feature_selection', select),
             ('clf', clf)]
    
    # Create the pipeline
    pipeline = Pipeline(steps)
    
    # Create Stratified ShuffleSplit cross-validator.
    # Provides train/test indices to split data in train/test sets.
    sss = StratifiedShuffleSplit(n_splits=n_splits, test_size=0.3, random_state=42)
    
    # Create grid search
    gs = GridSearchCV(pipeline, param_grid=parameters, scoring=('f1', 'recall'),
                      cv=sss, refit='f1')
                
    # Fit pipeline on features_train and labels_train
    gs.fit(features_train, labels_train)
    # Call pipeline.predict() on features_test data to make a set of test predictions
    labels_pred = gs.predict(features_test)
    # Test predictions using sklearn.classification_report()
    report = classification_report(labels_test, labels_pred)
    # Find the best parameters and scores
    best_params = gs.best_params_
    best_score = gs.best_score_
    # Print the reports
    print("Report:")
    print(report)
    print("Best score:")
    print(best_score)
    print("Best parameters:")
    print(best_params)
    print("Time passed: ", round(time() - t0, 3), "s")
    # Return the best estimator
    return gs.best_estimator_

for name, clf in classifiers.items():
    print("##########################################################################################################")
    print(name)
    if clf == nb:
        parameters = {'feature_selection__k':list(range(1, 5))}
    elif clf == svc:
        parameters = [{'feature_selection__k':list(range(1, 5)),
                      'clf__C':[10, 100]}]
    elif clf == dtc:
        parameters = [{'feature_selection__k':list(range(1, 5)),
                      'clf__criterion':['gini', 'entropy']}]
    elif clf == knc:
        parameters = [{'feature_selection__k':list(range(1, 5)),
                      'clf__n_neighbors':[3, 5, 7]}]
    elif clf == rfc:
        parameters = [{'feature_selection__k':list(range(1, 5)),
                      'clf__n_estimators':[1, 5, 10]}]
    elif clf == abc:
        parameters = [{'feature_selection__k':list(range(1, 5)),
                      'clf__n_estimators':[45, 50, 55]}]
    optimize_clf(clf, parameters, n_splits=10)

### Fine tune the selected algorithm
print("##########################################################################################################")
print("Decision Trees")
parameters = [{'feature_selection__k':[1, 2, 3, 4, 5],
               'clf__criterion':['gini', 'entropy'],
               'clf__splitter':['best', 'random'],
               'clf__max_features':[None, 'auto', 'sqrt', 'log2'],
               'clf__class_weight':[None, 'balanced']
              }]

clf = optimize_clf(dtc, parameters, n_splits=10)

# Access the SelectKBest features selected
# Create a new list that contains the features selected by SelectKBest
# in the optimal model selected by GridSearchCV
features_selected = [features_list[i+1] for i in clf.named_steps['feature_selection'].get_support(indices=True)]

# Access the feature importances
# The step in the pipeline for the Decision Tree Classifier is called 'clf'
# That step contains the feature importances
importances = clf.named_steps['clf'].feature_importances_

import numpy as np
indices = np.argsort(importances)[::-1]

# Use features_selected, the features selected by SelectKBest, and not features_list
print('Feature Ranking:')
for i in range(len(features_selected)):
    print("feature no. {}: {} ({})".format(i+1,features_selected[indices[i]],importances[indices[i]]))

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)