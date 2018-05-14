library(jsonlite)
library(wordcloud)
library(viridis)


words_0 <- fromJSON("wordclouds/part0.json")
words_1 <- fromJSON("wordclouds/part1.json")
words <- rbind(words_0, words_1)
words_df <- data.frame(word = words[,1], count = as.numeric(words[,2]))

png ("title_wordcloud.png", width=12,height=8, units='in', res=300)
wordcloud(words_df$word, 
          words_df$count, 
          random.order = FALSE,
          max.words = Inf, 
          scale = c(6, 0.025),
          rot.per = 0,
          fixed.asp = FALSE,
          colors = magma(100, direction = -1))
dev.off()
