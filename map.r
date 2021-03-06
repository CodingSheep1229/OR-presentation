library(jsonlite)
library(RCurl)
library(rjson)
library(knitr)
library(magrittr)
library(RJSONIO)
library(ggplot2)
library(mapproj)
library(ggmap)
library(tidyverse)
library(readxl)

options(encoding="UTF-8")
Sys.setlocale(category = "LC_ALL", locale = "zh_TW.UTF-8")
close_site = read_excel("/Users/hanjitsai/Documents/or/ampl/project/all.xlsx")
close_site = colnames(close_site)
result = read_excel("/Users/hanjitsai/Documents/or/ampl/project/result.xlsx")

##Part1. Crawl the json file from the website offered by taipei city gov
url = "http://data.taipei/youbike"
all_data = jsonlite::fromJSON(url)
all_data = all_data$retVal

##Part2. Parse all the data into data.frame
##As the data are list in the begining, we should 
##classify that type and combine each into the data frame df.

all_type = names(all_data[[1]])
df = data.frame()
for(i in 1:length(all_type))
{
  dat <- c()
  ss=sapply(all_data, function(x){toString(x[i])})
  if(nrow(df) == 0)
  {
    df = data.frame(ss)
  }else{
    df = data.frame(df,ss)  
  }
  
}
colnames(df) <- all_type

##In order to plot the map, transformming the latitude and longitude
##into numeric is necessarily
df$lat <- as.double(as.character(df$lat))
df$lng <- as.double(as.character(df$lng))

dff <- data.frame()
for(i in 1:length(close_site))
{
  ss <- subset(df,snaen == close_site[i])
  if(nrow(dff) == 0)
  {
    dff = data.frame(ss)
  }else{
    dff = rbind(dff,ss)  
  }
}

stat = unname(as.numeric(result[1,]))
stat = stat[stat!=0]
stat
res <- data.frame()
for(i in 1:length(stat))
{
  ss <- dff[stat[i]-1,]
  if(nrow(dff) == 0)
  {
    res = data.frame(ss)
  }else{
    res = rbind(res,ss)  
  }
}
dff$num = seq(1:nrow(dff))
print(res)

#Plot the map of remained ubike in Daan Dist. Moreover, adding the remained
##bikes in each station as the labels.
map=get_googlemap(center= c(lon=median(dff$lng),lat=median(dff$lat))
,zoom = 14 , maptype = "roadmap")

q = ggmap(map)
q = q + geom_point(data=dff, aes(lng, lat, colour="blue"), size = 4)
q = q + theme(legend.position="none") 
q = q + geom_text(data=dff, mapping=aes(x=lng, y=lat, label = num), size=2, vjust=0.5, hjust=0.5)
q = q + geom_path(aes(x = lng, y = lat,colour = "red"), data = res)
q = q + geom_text(data=dff, mapping=aes(x=lng, y=lat, label= sbi), size=2, vjust=1.5, hjust=1.5)
print(q)
ggsave(filename="/Users/hanjitsai/Documents/or/ampl/project/result.png")



