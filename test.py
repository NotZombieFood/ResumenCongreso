import functions
import url

for item in url.urls:
    title, summary , url, category = functions.parseEntry(item[0],item[1])
    functions.add2Pickle(title,summary,url,category)

print(functions.readPickle())