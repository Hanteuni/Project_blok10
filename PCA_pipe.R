#!usr/bin/env Rscript

# Eerste argument: dataset waarop je PCA wilt uitvoeren
# Tweede argument: path waar je de PCA analyse wilt opslaan + bestandsnaam

args = commandArgs(trailingOnly = TRUE)

# convert csv to dataframe in R
csv_to_dataframe = function(csv){
  csv = read.csv(file = csv, sep = "\t", row.names = 1)
  return(csv)
}

# Compute PCA
comp_PCA = function(dfr){ #dfr = dataframe
  pr.out = prcomp(dfr, scale. = T, center = TRUE)
  return (pr.out)
}

# Write output file with PCA
exp_csv = function(dfr, location){ #drf = dataframe, location = path, bestandsnaam
  write.csv(dfr, location)
  
}
dfr = csv_to_dataframe(args[1])
pca = comp_PCA(dfr)
# exp_csv(args[2])

