# Data Cleaning
library(dplyr)
clean_data <- function(df, na_columns, categorical_columns) {
  # Remove rows with NA in the specified columns,
  # convert the specified columns to categorical (factor) columns
  df <- df[complete.cases(df[na_columns]), ]
  df[categorical_columns] <- lapply(df[categorical_columns], factor)
  rownames(df) <- NULL
  df
}


# Logistic Regression
fit_logistic <- function(df, predictors, response = "Survived") {
  # Fit logistic regression with the specified predictor columns
  formula <- reformulate(predictors, response = response)
  glm(formula, data = df, family = binomial)
}


# Model Evaluation
evaluate_model <- function(model, df, response = "Survived", threshold = 0.5) {
  y_true <- as.integer(df[[response]])
  y_pred <- as.integer(predict(model, newdata = df, type = "response") >= threshold)
  mean(y_pred == y_true)
}



if (sys.nframe() == 0L) {
  # default columns to convert to factors
  CATEGORICAL_COLUMNS <- c("Pclass")
  DROPNA_COLUMNS <- c("Age", "Embarked")
  train <- read.csv("data/train.csv", na.strings = c("", "NA"))
  train <- clean_data(train, na_columns = DROPNA_COLUMNS, categorical_columns = CATEGORICAL_COLUMNS)
  cat("Finished data cleaning\n")
  cat(sprintf("converted [%s] into categorical values and remove NaNs in [%s]\n",
              CATEGORICAL_COLUMNS, DROPNA_COLUMNS))
 

  # Fit the model with specified predictors
  PREDICTORS <- c("Pclass", "Sex", "Age", "SibSp", "Parch")
  model <- fit_logistic(train, predictors = PREDICTORS)
  print(summary(model))

  # Evaluate the model on training set
  accuracy <- evaluate_model(model, train)
  cat(sprintf("Training accuracy: %s\n", format(accuracy, digits = 16)))

  # running predictions on testing set
  test <- read.csv("data/test.csv", na.strings = c("", "NA"))
  test_label <- read.csv("data/gender_submission.csv")
  test <- clean_data(test, na_columns = DROPNA_COLUMNS, categorical_columns = CATEGORICAL_COLUMNS)
  test <- merge(test, test_label, by = "PassengerId")
  test_result <- as.integer(predict(model, newdata = test, type = "response") >= 0.5)
  cat(sprintf("%.2f%% of the test data is predicted to survive, while %.2f%% not\n",
              mean(test_result) * 100, (1 - mean(test_result)) * 100))
}
