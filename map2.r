
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
close_site = read_excel("/Users/hanjitsai/Documents/or/ampl/project/dis.xlsx")
close_site = colnames(close_site)
result = read_excel("/Users/hanjitsai/Documents/or/ampl/project/result.xlsx")

##Part1. Crawl the json file from the website offered by taipei city gov

##Part2. Parse all the data into data.frame
##As the data are list in the begining, we should 
##classify that type and combine each into the data frame df.

##into numeric is necessarily
begin = colnames(result)
stat = unname(as.integer(result[1,]))
stat = stat[stat!=0]
begin = as.numeric(begin)
begin = begin[begin!=0]
begin = begin[!is.na(begin)]
end = stat
stat = c(as.numeric(begin[1]),stat)
res <- data.frame()
num_bike = unname(ceiling(as.double(result[2,])))
num_bike = num_bike[1:length(begin)]

for(i in 1:length(stat))
{
  ss <- dff[stat[i],]
  if(nrow(dff) == 0)
  {
    res = data.frame(ss)
  }else{
    res = rbind(res,ss)  
  }
}
dff$num = seq(1:nrow(dff))
#print(res)

alloc <- data.frame()
lng_list <- c()
lat_list <- c() 
for(i in 1:length(begin))
{
  lng1 = dff[begin[i],]$lng
  lng2 = dff[end[i],]$lng
  lat1 = dff[begin[i],]$lat
  lat2 = dff[end[i],]$lat
  lng_list <- c(lng_list,(lng1+lng2)/2)
  lat_list <- c(lat_list,(lat1+lat2)/2)
  
}
alloc <- data.frame(lng = lng_list,lat = lat_list,num = num_bike)


dff$num = seq(1:nrow(dff))



#Plot the map of remained ubike in Daan Dist. Moreover, adding the remained
##bikes in each station as the labels.
map=get_googlemap(center= c(lon=median(dff$lng),lat=median(dff$lat))
,zoom = 15 , maptype = "roadmap")

q = ggmap(map)
q = q + geom_point(data=dff, aes(lng, lat, colour="blue"), size = 4)
q = q + theme(legend.position="none") 
q = q + geom_text(data=dff, mapping=aes(x=lng, y=lat, label= sbi), size=3, vjust=0.5, hjust=0.5)
ggsave(filename="/Users/hanjitsai/Documents/or/ampl/project/original.png")
#q = q + geom_text(data=dff, mapping=aes(x=lng, y=lat, label = num), size=3, vjust=0.5, hjust=0.5)
q = q + geom_path(aes(x = lng, y = lat,colour = "red"), data = res , arrow = arrow(type = "open", angle = 30, length = unit(0.1, "inches")))
q = q + geom_text(data=alloc, mapping=aes(x=lng, y=lat, label= num), size=4, vjust=0.5, hjust=0.5,angle = 45,colour = rainbow(7)[6])
print(q)
ggsave(filename="/Users/hanjitsai/Documents/or/ampl/project/result.png")
