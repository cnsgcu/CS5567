cals <- c(mean, var)
match_urls <- c('https://raw.githubusercontent.com/cnsgcu/CS5567/master/hw1/usopen.csv', 'https://raw.githubusercontent.com/cnsgcu/CS5567/master/hw1/ausopen.csv')

match_stats <- do.call(rbind, lapply(match_urls, read.csv))

params <- do.call(rbind, lapply(cals, function(cal){ as.data.frame(lapply(match_stats[,1:30], cal)) }))
