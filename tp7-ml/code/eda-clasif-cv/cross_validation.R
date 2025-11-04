#!/usr/bin/env Rscript

# k-fold split -------------------------------------------------------------
create_folds <- function(df, k, seed = NULL) {
  if (!is.data.frame(df)) {
    stop("`df` must be a data.frame")
  }
  if (!is.numeric(k) || length(k) != 1 || k <= 1) {
    stop("`k` must be a numeric value greater than 1")
  }
  n <- nrow(df)
  if (k > n) {
    stop("`k` cannot exceed the number of rows in `df`")
  }
  if (!is.null(seed)) {
    set.seed(seed)
  }

  shuffled <- sample.int(n)
  fold_ids <- cut(
    seq_along(shuffled),
    breaks = k,
    labels = FALSE
  )

  folds <- split(shuffled, fold_ids)
  names(folds) <- sprintf("Fold%d", seq_along(folds))
  folds
}

# Metric helpers -----------------------------------------------------------
accuracy <- function(tp, tn, fp, fn) {
  total <- tp + tn + fp + fn
  if (total == 0) {
    return(NA_real_)
  }
  (tp + tn) / total
}

precision <- function(tp, fp) {
  denom <- tp + fp
  if (denom == 0) {
    return(NA_real_)
  }
  tp / denom
}

sensitivity <- function(tp, fn) {
  denom <- tp + fn
  if (denom == 0) {
    return(NA_real_)
  }
  tp / denom
}

specificity <- function(tn, fp) {
  denom <- tn + fp
  if (denom == 0) {
    return(NA_real_)
  }
  tn / denom
}

compute_metrics <- function(actual, predicted, positive_class) {
  tp <- sum(actual == positive_class & predicted == positive_class, na.rm = TRUE)
  tn <- sum(actual != positive_class & predicted != positive_class, na.rm = TRUE)
  fp <- sum(actual != positive_class & predicted == positive_class, na.rm = TRUE)
  fn <- sum(actual == positive_class & predicted != positive_class, na.rm = TRUE)

  c(
    accuracy = accuracy(tp, tn, fp, fn),
    precision = precision(tp, fp),
    sensitivity = sensitivity(tp, fn),
    specificity = specificity(tn, fp)
  )
}

# Cross validation ---------------------------------------------------------
cross_validation <- function(
    df,
    k = 5,
    formula = inclinacion_peligrosa ~ altura + circ_tronco_cm + long + lat + seccion + especie,
    seed = NULL,
    positive_class = NULL) {
  if (!requireNamespace("rpart", quietly = TRUE)) {
    stop("Package `rpart` is required. Install it with install.packages('rpart').")
  }
  if (!is.data.frame(df)) {
    stop("`df` must be a data.frame")
  }

  df_model <- df
  char_cols <- vapply(df_model, is.character, logical(1))
  if (any(char_cols)) {
    for (col in names(df_model)[char_cols]) {
      df_model[[col]] <- as.factor(df_model[[col]])
    }
  }

  target <- all.vars(formula)[1]
  if (!target %in% names(df_model)) {
    stop(sprintf("target column '%s' not found in dataframe", target))
  }

  df_model[[target]] <- as.factor(df_model[[target]])
  if (is.null(positive_class)) {
    pos_levels <- levels(df_model[[target]])
    if (length(pos_levels) != 2) {
      stop("Unable to infer positive class automatically. Please specify `positive_class`.")
    }
    positive_class <- pos_levels[length(pos_levels)]
  }

  folds <- create_folds(df_model, k, seed)

  metrics_mat <- matrix(NA_real_, nrow = length(folds), ncol = 4)
  colnames(metrics_mat) <- c("accuracy", "precision", "sensitivity", "specificity")

  for (i in seq_along(folds)) {
    test_idx <- folds[[i]]
    train_df <- df_model[-test_idx, , drop = FALSE]
    test_df <- df_model[test_idx, , drop = FALSE]

    model <- rpart::rpart(formula, data = train_df, method = "class")
    preds <- predict(model, test_df, type = "class")
    preds <- factor(preds, levels = levels(df_model[[target]]))

    metrics_mat[i, ] <- compute_metrics(
      actual = test_df[[target]],
      predicted = preds,
      positive_class = positive_class
    )
  }

  metrics_df <- cbind(
    fold = names(folds),
    as.data.frame(metrics_mat)
  )

  mean_values <- colMeans(metrics_mat, na.rm = TRUE)
  sd_values <- apply(metrics_mat, 2, stats::sd, na.rm = TRUE)

  list(
    folds = folds,
    per_fold = metrics_df,
    summary = rbind(mean = mean_values, sd = sd_values)
  )
}
