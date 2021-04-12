# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from scrapy import cmdline

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test1 = "scrapy crawl ebay -a site= -a keyword= -a category_entry=https://www.ebay.de/b/Fernseher/11071/bn_1844904 -o data.csv"
    test2 = "scrapy crawl ebay -a site=https://www.ebay.de -a keyword=projector+screen -a category_entry= -o data.csv"
    cmdline.execute(test2.split())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
