import numpy as np
import pandas as pd
import statsmodels.formula.api as smf




# Data Cleaning
def clean_data(df, na_columns, categorical_columns):
    '''
    Remove NA from specified column,
    convert specified columns to categorical columns
    '''
    df = df.dropna(subset=na_columns)
    df = df.astype({col: 'category' for col in categorical_columns})
    return df.reset_index(drop=True)


# Logistic Regression
def fit_logistic(df, predictors, response='Survived'):
    '''
    fit logistic regression with specified predictor variable columns
    '''
    data = df[[response] + list(predictors)].copy()
    data[response] = data[response].astype(int) 
    formula = f"{response} ~ " + ' + '.join(f'Q("{c}")' for c in predictors)
    return smf.logit(formula, data=data).fit()


# Model Evaluation
def evaluate_model(model, df, response='Survived', threshold=0.5):
    '''
    Return the accuracy of a fitted logistic model on `df` (which must
    contain the predictors used in training and the true `response`).
    '''
    y_true = df[response].astype(int).to_numpy()
    y_pred = (np.asarray(model.predict(df)) >= threshold).astype(int)
    return float((y_pred == y_true).mean())


if __name__ == '__main__':
    # default columns to converted to factgors
    CATEGORICAL_COLUMNS = ['Pclass']
    DROPNA_COOLUMNS = ['Age', 'Embarked']     
    train = pd.read_csv('data/train.csv')
    train = clean_data(train, na_columns = DROPNA_COOLUMNS, categorical_columns=CATEGORICAL_COLUMNS)
    print('Finished data cleaning')
    print(f'converted {CATEGORICAL_COLUMNS} into categorical values and remove NaNs in {DROPNA_COOLUMNS} ')
    # print(train)

    # choose which columns to use as predictors
    PREDICTORS = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch']
    model = fit_logistic(train, predictors=PREDICTORS)
    print(model.summary())

    #Evaluate the model on training set
    accuracy = evaluate_model(model, train)
    print(f'Training accuracy: {accuracy}')


    # Evaluate model on testing set
    test = pd.read_csv('data/test.csv')
    test_label = pd.read_csv('data/gender_submission.csv')
    test = clean_data(test, na_columns = DROPNA_COOLUMNS, categorical_columns=CATEGORICAL_COLUMNS)
    test = pd.merge(test,test_label,how = 'inner', on = 'PassengerId')
    test_result = (np.asarray(model.predict(test)) >= 0.5).astype(int)
    print(f'{np.mean(test_result)*100:.2f}% of the test data is predicted to survive, while {(1-np.mean(test_result))*100:.2f}% not')