from fsplit.filesplit import FileSplit

fs = FileSplit(file='flantastic/data/boulangeries.csv', splitsize=5000000, output_dir='flantastic/data/boulangeries_chunks') #5.9 Mio

fs.split()