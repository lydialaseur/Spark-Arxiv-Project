library(jsonlite)
library(wordcloud)
library(viridis)


words_0 <- fromJSON("wordclouds/part0.json")
words_1 <- fromJSON("wordclouds/part1.json")
words <- rbind(words_0, words_1)
words_df <- data.frame(word = words[,1], count = as.numeric(words[,2]))

words_df <- words_df[words_df$word != "&",]
png ("title_wordcloud2.png", width=12,height=8, units='in', res=300)
wordcloud(words_df$word, 
          words_df$count, 
          random.order = FALSE,
          max.words = Inf, 
          scale = c(6, 0.025),
          rot.per = 0,
          fixed.asp = FALSE,
          colors = magma(100, direction = -1))
dev.off()

abstract_words_0 <- fromJSON("wordclouds/abstracts_part0.json")
abstract_words_1 <- fromJSON("wordclouds/abstracts_part1.json")
abstract_words <- rbind(abstract_words_0, abstract_words_1)
abstract_words_df <- data.frame(word = abstract_words[,1], 
                                count = as.numeric(abstract_words[,2]))

png ("abstract_wordcloud2.png", width=12,height=8, units='in', res=300)
wordcloud(abstract_words_df$word, 
          abstract_words_df$count, 
          random.order = FALSE,
          max.words = Inf, 
          scale = c(6, 0.025),
          rot.per = 0,
          fixed.asp = FALSE,
          colors = viridis(100, direction = -1, option = "cividis"))
dev.off()

