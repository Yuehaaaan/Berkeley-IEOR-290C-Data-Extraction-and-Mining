import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.stats.api import ols
import statsmodels.formula.api as sm

impact = None
loans = None
countries = None
members = None
about = None

loans_per_member = None
total_loans = None
total_amount_lent = None
borrower_female_count = None
borrower_male_count = None

#borrower_female_count borrower_male_count	
#team_members	total_amount_lent
#team_url	
#loans_per_member	borrower_male_percentage	
#borrower_female_percentage	total_loans

""" Select columns:
borrower_female_count
borrower_male_count
total_amount_lent
loans_per_member
total_loans
"""

def initialize_data():
	global impact,loans,countries,members
	about = pd.read_csv("about.csv",sep=",")
	impact = pd.read_csv("impact.csv",sep=",")
	loans = pd.read_csv("loans.csv",sep=",")
	countries = pd.read_csv("countries.csv",sep=",")
	members = pd.read_csv("members.csv",sep=",")


	impact = impact.dropna(how="any")
	intro = about[["team_url","intro"]]
	impact = pd.merge(impact,intro,how="inner",on="team_url")
	impact = impact.fillna("")
	impact["intro_len"] = impact["intro"].str.split().apply(len)

	impact["loans_per_member"] = impact["loans_per_member"].astype(float)
	impact["total_loans"] = impact["total_loans"].astype(int)
	impact["total_amount_lent"] = impact["total_amount_lent"].astype(float)
	impact["borrower_female_count"] = impact["borrower_female_count"].astype(int)
	impact["borrower_male_count"] = impact["borrower_male_count"].astype(int)

	global loans_per_member, total_loans, total_amount_lent,borrower_female_count,borrower_male_count
	loans_per_member = impact["loans_per_member"]
	total_loans = impact["total_loans"]
	total_amount_lent = impact["total_amount_lent"]
	borrower_female_count = impact["borrower_female_count"]
	borrower_male_count = impact["borrower_male_count"]







def getMin():
	print "Minimum Values"
	print "Min of loans per members: {0:0.2f}".format(loans_per_member.min())
	print "Min of total loans: {0}".format(total_loans.min())
	print "Min of total amount_lent: {0:0.2f}".format(total_amount_lent.min())
	print "Min of borrower male count: {0}".format(borrower_male_count.min())
	print "Min of borrower female count: {0}".format(borrower_female_count.min())

def getMax():
	print "Maximum Values"
	print "Max of loans per members: {0:0.2f}".format(loans_per_member.max())
	print "Max of total loans: {0}".format(total_loans.max())
	print "Max of total amount_lent: {0:0.2f}".format(total_amount_lent.max())
	print "Max of borrower male count: {0}".format(borrower_male_count.max())
	print "Max of borrower female count: {0}".format(borrower_female_count.max())

def getMode():
	mode = impact.mode(numeric_only=True)
	print "Mode Values"
	print "Mode of loans per member: ",mode["loans_per_member"].loc[0]
	print "Mode of total loans: ",mode["total_loans"].loc[0]
	print "Mode of total amount lent: ", mode["total_amount_lent"].loc[0]
	print "Mode of borrower male count: ", mode["borrower_male_count"].loc[0]
	print "Mode of borrower female count: ",mode["borrower_female_count"].loc[0]

def getMedian():
	print "Median Values"
	print "Median of loans per members: {0:0.2f}".format(loans_per_member.median())
	print "Median of total loans: {0}".format(total_loans.median())
	print "Median of total amount_lent: {0:0.2f}".format(total_amount_lent.median())
	print "Median of borrower male count: {0}".format(borrower_male_count.median())
	print "Median of borrower female count: {0}".format(borrower_female_count.median())

def getMean():
	print "Mean Values"
	print "Mean of loans per members: {0:0.2f}".format(loans_per_member.mean())
	print "Mean of total loans: {0:0.2f}".format(total_loans.mean())
	print "Mean of total amount_lent: {0:0.2f}".format(total_amount_lent.mean())
	print "Mean of borrower male count: {0:0.2f}".format(borrower_male_count.mean())
	print "Mean of borrower female count: {0:0.2f}".format(borrower_female_count.mean())

def getStd():
	print "Standard Deviation Values"
	print "Std of loans per members: {0:0.2f}".format(loans_per_member.std())
	print "Std of total loans: {0:0.2f}".format(total_loans.std())
	print "Std of total amount lent: {0:0.2f}".format(total_amount_lent.std())
	print "Std of borrower male count: {0:0.2f}".format(borrower_male_count.std())
	print "Std of borrower female count: {0:0.2f}".format(borrower_female_count.std())

def getNumberOfObservations():
	print "Number of number of Oberservations: ", loans_per_member.count()

def getOutliersCount():
	# outlier is defined as outside of 2 std deviation
	print "Outliers values"

	print "Number of loans per member"
	out = getOutliers(loans_per_member)
	print "Number of loans per member outliers: ", out.count()

	print "Number of total loans"
	out = getOutliers(total_loans)
	print "Number of total loans outliers: ", out.count()

	print "Number of total amount lent"
	out = getOutliers(total_amount_lent)
	print "Number of total amount lent outliers: ", out.count()

	print "Number of total borrower male count"
	out = getOutliers(borrower_male_count)
	print "Number of total borrower male count outliers: ", out.count()

	print "Number of total borrower female count"
	out = getOutliers(borrower_female_count)
	print "Number of total borrower female count outliers ", out.count()


def getOutliers(df):
	boolean1 = df < df.mean()-2*df.std()
	boolean2 = df > df.mean()+2*df.std()
	boolean = boolean1 | boolean2
	print impact[boolean]["team_url"]
	return df[boolean]

def getTrimmed(df):
	boolean = df < df.mean()+2*df.std()
	s = df[boolean]
	return s


def plotHistogram():
	plot1a = histoPlot(title="Loans per member (Untrimmed)",s=loans_per_member,div=50,xlabel="Loans per member")
	plot1b = histoPlot(title="Loans per member (Trimmed)",s=getTrimmed(loans_per_member),div=200,xlabel="Loans per member")
	count,division = np.histogram(getTrimmed(loans_per_member),bins = 200)
	print "LPM: divisions {0} to {1} has the maximum count of {2}".format(division[0],division[1],count[0])
	plot1a.savefig("figures/Loans per member (untrimemd).png")
	plot1b.savefig("figures/Loans per member (trimmed).png")

	plot2a = histoPlot(title="Total loans (Untrimmed)", s=total_loans,div = 50, xlabel="Total loans")
	plot2b = histoPlot(title="Total loans (Trimmed)", s = getTrimmed(total_loans), div = 200, xlabel="Total loans")
	count,division = np.histogram(getTrimmed(total_loans),bins = 200)
	
	print "TL: divisions {0} to {1} has the maximum count of {2}".format(division[0],division[1],count[0])
	plot2a.savefig("figures/Total loans (untrimmed).png")
	plot2b.savefig("figures/Total loans (trimmed).png")


	plot3a = histoPlot(title="Total amount lent (Untrimmed)", s=total_amount_lent,div = 50, xlabel="Total amount lent")
	plot3b = histoPlot(title="Total amount lent (Trimmed)", s = getTrimmed(total_amount_lent), div = 200, xlabel="Total amount lent")
	count,division = np.histogram(getTrimmed(total_amount_lent),bins = 200)
	print "TAL: divisions {0} to {1} has the maximum count of {2}".format(division[0],division[1],count[0])
	plot3a.savefig("figures/Total amount lent (untrimmed).png")
	plot3b.savefig("figures/Total amount lent (trimmed).png")

	plot4a = histoPlot(title="Borrower male count (Untrimmed)", s=borrower_male_count,div = 50, xlabel="Borrower male count")
	plot4b = histoPlot(title="Borrower male count (Trimmed)", s = getTrimmed(borrower_male_count), div = 200, xlabel="Borrower male count")
	count,division = np.histogram(getTrimmed(borrower_male_count),bins = 200)
	print "BMC: divisions {0} to {1} has the maximum count of {2}".format(division[0],division[1],count[0])
	plot4a.savefig("figures/Borrower male count (untrimmed).png")
	plot4b.savefig("figures/Borrower male count (trimmed).png")

	plot5a = histoPlot(title="Borrower female count (Untrimmed)", s=borrower_female_count,div = 50, xlabel="Borrower female count")
	plot5b = histoPlot(title="Borrower female count (Trimmed)", s = getTrimmed(borrower_female_count), div = 200, xlabel="Borrower female count")
	count,division = np.histogram(getTrimmed(borrower_female_count),bins = 200)
	print "BFC: divisions {0} to {1} has the maximum count of {2}".format(division[0],division[1],count[0])
	plot5a.savefig("figures/Borrower female count (untrimmed).png")
	plot5b.savefig("figures/Borrower female count (trimmed).png")

	plot6a = histoPlot(title="Length of introduction (Untrimmed)", s = impact["intro_len"],div = 50, xlabel="Length of introduction")
	plot6b = histoPlot(title="Length of introduction (Trimmed)",s=impact["intro_len"],div = 200, xlabel = "Length of introduction")
	plot6a.savefig("figures/Length of introduction (untrimmed).png")
	plot6b.savefig("figures/Length of introduction (trimmed).png")



def histoPlot(title,s,div,xlabel):
	fig = plt.figure()
	s.hist(bins=div,log=True)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel("Frequency")
	return fig

def getRegression():
	merged = pd.concat([total_amount_lent,total_loans, loans_per_member, borrower_female_count,borrower_male_count],axis = 1)
	result = sm.ols(formula="total_amount_lent ~ total_loans", data = merged).fit()
	print result.summary()
	result = sm.ols(formula="total_amount_lent ~ loans_per_member", data = merged).fit()
	print result.summary()
	result = sm.ols(formula="total_amount_lent ~ borrower_female_count", data = merged).fit()
	print result.summary()
	result = sm.ols(formula="total_amount_lent ~ borrower_male_count", data = merged).fit()
	print result.summary()
	result = sm.ols(formula = "total_amount_lent ~ intro_len", data = impact).fit()
	print result.summary()

def plotScatter():
	plot1 = scatterPlot(title="Total amount lent vs. total loans",x=total_loans,y=total_amount_lent,
				xlabel="Total number of loans",ylabel="Total amount lent ($)")

	plot2 = scatterPlot(title="Total amount lent vs. loans per member",x=loans_per_member,y=total_amount_lent,
				xlabel="Loans per member",ylabel="Total amount lent ($)")
	
	plot3 = scatterPlot(title="Total amount lent vs. number of female borrowers",x=borrower_female_count,y=total_amount_lent,
				xlabel="number of female borrowers",ylabel="Total amount lent ($)")
	
	plot4 = scatterPlot(title="Total amount lent vs. number of male borrowers",x=borrower_male_count,y=total_amount_lent,
				xlabel="number of male borrowers",ylabel="Total amount lent ($)")
	
	plot4 = scatterPlot(title="Total amount lent vs. number of male borrowers",x=borrower_male_count,y=total_amount_lent,
				xlabel="number of male borrowers",ylabel="Total amount lent ($)")

	plot5 = scatterPlot(title="Total amount lent vs. length of introduction", x=impact["intro_len"],y = total_amount_lent,
						xlabel = "length of introduction", ylabel = "Total amount lent ($)")


	plot1.savefig("figures/Total amount lent vs. total loans.png")
	plot2.savefig("figures/Total amount lent vs. loans per member.png")
	plot3.savefig("figures/Total amount lent vs. number of female borrowers.png")
	plot4.savefig("figures/Total amount lent vs. number of male borrowers.png")
	plot5.savefig("figures/Total amount lent vs. length of introduction.png")

def scatterPlot(title,x,y,xlabel,ylabel):
	fig = plt.figure()
	plt.scatter(x=x,y=y)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	m,b = np.polyfit(x,y,1)
	plt.plot(x,m*x+b,"-")
	return fig




initialize_data()
getMin()
getMax()
getMode()
getMedian()
getMean()
getStd()
getNumberOfObservations()
getOutliersCount()
plotHistogram()
getRegression()
plotScatter()


def myOLS(data):
	n = len(data)
	sum_xy = 0
	sum_x  =0
	sum_y = 0
	sum_x_sq = 0
	m = 0
	for x,y in data:
		sum_xy = sum_xy + x*y
		sum_x = sum_x + x
		sum_y = sum_y + y
		sum_x_sq = sum_x_sq + x**2
	m = float((n*sum_xy - sum_x * sum_y)/(n*sum_x_sq - sum_x**2))
	b = float((sum_y - m*sum_x)/n)
	return m,b

# data = [(1,1),(2,2),(4,4),(10,10)]
# m,b = myOLS(data)
# print m,b
# data = [(1,1),(2,4),(4,16),(3,9)]
# m,b = myOLS(data)
# print m,b





