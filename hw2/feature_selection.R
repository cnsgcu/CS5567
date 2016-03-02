tennis_csv <- c(
  'https://raw.githubusercontent.com/cnsgcu/CS5567/master/hw2/split_ausopen.csv',
  'https://raw.githubusercontent.com/cnsgcu/CS5567/master/hw2/split_usopen.csv'
)

tennis_players <- do.call(rbind,lapply(tennis_csv, read.csv))

won_players <- subset(tennis_players, Won == 1)
lost_players <- subset(tennis_players, Won == 0)

pvalues <- lapply(1:15, function(ci) {t.test(won_players[,ci], lost_players[,ci])$p.value})

pvaluesBonferroni = p.adjust(pvalues, method = "bonferroni", n = length(pvalues))

colnames(tennis_players)[which(pvaluesBonferroni < 0.05)]
