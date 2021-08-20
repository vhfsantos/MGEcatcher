#!/home/vinicius/miniconda3/bin/R
options(warn=-1)
args = commandArgs(trailingOnly=T)

suppressPackageStartupMessages({
	require(GenomicRanges)
	require(IRanges)
    require(ggbio)
	require(dplyr)
})

# writting functions to be called in apply furtherly

GetMGEName = function(x){
	paste(x[2],
	x[5],
	strsplit(x[1],split = "::")[[1]][1],
	x[8],
	sep="_")
}

GetLen4reduced = function(x){
    sqname = x[1]
    x[6] = seqlen[sqname]
}

GetReadName = function(x){
    read = x[1]
    id = x[7]
    paste(read,id,sep="_")
}

filtered_data = args[1]

df = read.table(filtered_data)
df$row = rownames(df)

df$MGE = apply(df,
	FUN = GetMGEName,
	MARGIN = 1)

df = df[,c(2,3,4,6,9)]
colnames(df) = c("seqnames", "start", "end", "seqlength", "MGE")
df$strand = "+"
toPlot = head(df,10)

gr = makeGRangesFromDataFrame(df,
                              seqnames.field="seqnames",
                              start.field="start",
                              end.field="end",
                              strand.field="strand")

tmp = makeGRangesFromDataFrame(toPlot,
                              seqnames.field="seqnames",
                              start.field="start",
                              end.field="end",
                              strand.field="strand")

dfnames = toPlot[,c(1,4)]
dfnames = distinct(dfnames)
seqlen = dfnames$seqlength
names(seqlen) = dfnames$seqnames
tmp = GRanges(tmp, seqlengths = seqlen)

dfnames = df[,c(1,4)]
dfnames = distinct(dfnames)
seqlen = dfnames$seqlength
names(seqlen) = dfnames$seqnames
toReduce = GRanges(gr, seqlengths = seqlen)

Reduced = reduce(toReduce)
tmp = reduce(tmp)

pdf(paste0(filtered_data, ".reduced.pdf"))

suppressMessages({
autoplot(tmp, aes(fill="strand"), nrow=2) +
        scale_fill_manual(values = "#d95f02") +
        ggtitle("MGE mapping", subtitle = "First 10 mappings") +
        theme(legend.position = "none", 
              axis.text.x = element_text(angle=90,vjust=0.5,hjust=0.5))
})
      
final_df = as.data.frame(Reduced) 

final_df$seqlen = apply(final_df, 
	FUN = GetLen4reduced,
	MARGIN = 1)

final_df = final_df[,c(1,2,3,6)]

write.table(final_df, paste0(filtered_data, ".reduced.txt"),
	quote=F, row.names = F, col.names = F)

dev.off()
