#!/usr/bin/env Rscript

#' Compute accuracy from confusion matrix counts.
accuracy <- function(tp, tn, fp, fn) {
  total <- tp + tn + fp + fn
  if (total == 0) {
    return(NA_real_)
  }
  (tp + tn) / total
}

#' Compute precision from confusion matrix counts.
precision <- function(tp, fp) {
  denom <- tp + fp
  if (denom == 0) {
    return(NA_real_)
  }
  tp / denom
}

#' Compute sensitivity (recall) from confusion matrix counts.
sensitivity <- function(tp, fn) {
  denom <- tp + fn
  if (denom == 0) {
    return(NA_real_)
  }
  tp / denom
}

#' Compute specificity from confusion matrix counts.
specificity <- function(tn, fp) {
  denom <- tn + fp
  if (denom == 0) {
    return(NA_real_)
  }
  tn / denom
}

# Convenience helper to compute all metrics from a confusion matrix.
metrics_from_conf <- function(conf) {
  c(
    accuracy = accuracy(conf$tp, conf$tn, conf$fp, conf$fn),
    precision = precision(conf$tp, conf$fp),
    sensitivity = sensitivity(conf$tp, conf$fn),
    specificity = specificity(conf$tn, conf$fp)
  )
}
