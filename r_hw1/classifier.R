match_urls <- c(
	'https://raw.githubusercontent.com/cnsgcu/CS5567/master/hw1/usopen.csv',
	'https://raw.githubusercontent.com/cnsgcu/CS5567/master/hw1/ausopen.csv'
)

match_stats <- do.call(rbind, lapply(match_urls, read.csv))

team1_won_matches <- match_stats[match_stats$Match.Winner==0, 1:30]
team2_won_matches <- match_stats[match_stats$Match.Winner==1, 1:30]

training_gnb <- function(train) {
	cals <- c(mean, var)
	params <- do.call(rbind, lapply(cals, function(cal){ as.data.frame(lapply(train, cal)) }))
	return(params)
}

pstprob <- function(x, params) {
	cal_params <- rbind(params, x)
	prob <- prod(unname(sapply(cal_params, function(p){ 1/sqrt(2 * pi * p[2]) * exp(-(p[3] - p[1]) ^ 2 / (2 * p[2])) } )))
	return(prob)
}

team1_params <- training_gnb(head(team1_won_matches, 10))
team2_params <- training_gnb(head(team2_won_matches, 10))

team1_persp <- unname(apply(team1_won_matches[11:24,], 1, function(m) {pstprob(m, team1_params)}))
team2_persp <- unname(apply(team1_won_matches[11:24,], 1, function(m) {pstprob(m, team2_params)}))

team1_persp <- unname(apply(team1_won_matches[11:22,], 1, function(m) {pstprob(m, team1_params)}))
team2_persp <- unname(apply(team2_won_matches[11:22,], 1, function(m) {pstprob(m, team2_params)}))
