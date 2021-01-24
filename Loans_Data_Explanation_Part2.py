#!/usr/bin/env python
# coding: utf-8

# # Loans Data Explanation

# ## Dataset Overview
# The `Loans dataset` contains 113,937 loans since 2005/2014 with 81 variables on each loan, including loan amount, current loan status, borrower income, borrower occupation, and many others. <br>
# It's contains qualititave varibles such as loan status, loan category, borrower state and occupation and others. Also, it's contains quantitave variables such as loan amount, term, borrower income and others.
# 
# ## Investigation Overview
# In this investigation, I want to look what factors of difference columns (borrower income, occupation, state, etc.) that affect on loans outcome.

# In[1]:


# import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# load dataset
df = pd.read_csv('prosperLoanData.csv')


# In[6]:


df_loan = df[['ListingNumber','ListingCreationDate','Term','LoanStatus','ClosedDate','ListingCategory (numeric)','BorrowerState',
              'Occupation','EmploymentStatus','EmploymentStatusDuration','IsBorrowerHomeowner','IncomeRange','IncomeVerifiable',
              'StatedMonthlyIncome','TotalProsperLoans','TotalProsperPaymentsBilled','OnTimeProsperPayments',
              'ProsperPaymentsLessThanOneMonthLate','ProsperPaymentsOneMonthPlusLate', 'LoanOriginalAmount']].copy()


# In[8]:


# rename column
df_loan.rename(columns = {'ListingCategory (numeric)':'ListingCategory'}, inplace = True) 


# In[12]:


# check if contains duplicate
df_loan.duplicated().sum()


# In[13]:


# drop duplicates rows
df_loan.drop_duplicates(inplace = True)


# In[17]:


# create new dataset for borrower they have prosper loan
df_prosloan = df_loan[['ListingNumber','TotalProsperLoans','TotalProsperPaymentsBilled','OnTimeProsperPayments',
                      'ProsperPaymentsLessThanOneMonthLate','ProsperPaymentsOneMonthPlusLate']].copy()

# drop col
df_loan.drop(['TotalProsperLoans','TotalProsperPaymentsBilled','OnTimeProsperPayments',
                      'ProsperPaymentsLessThanOneMonthLate','ProsperPaymentsOneMonthPlusLate'], axis=1, inplace=True)


# ## Loans Status Frequencies

# In[20]:


# display loan status
base_color = sb.color_palette()[0]
st_order = df_loan['LoanStatus'].value_counts().index
sb.countplot(data = df_loan, y = 'LoanStatus', color = base_color, order = st_order);


# ## Loans Categories Frequencies

# In[21]:


# sort loan category listing
cat_order = df_loan['ListingCategory'].value_counts().index
sb.countplot(data = df_loan, x = 'ListingCategory', color = base_color, order = cat_order);
# change the figure size
sb.set(rc={'figure.figsize':(15,10)});


# > The category of the listing that the borrower selected when posting their listing:<br> 0 - Not Available, 1 - Debt Consolidation, 2 - Home Improvement, 3 - Business, 4 - Personal Loan, 5 - Student Use, 6 - Auto, 7- Other, 8 - Baby&Adoption, 9 - Boat, 10 - Cosmetic Procedure, 11 - Engagement Ring, 12 - Green Loans, 13 - Household Expenses, 14 - Large Purchases, 15 - Medical/Dental, 16 - Motorcycle, 17 - RV, 18 - Taxes, 19 - Vacation, 20 - Wedding Loans

# ## Borrowers State Proportion

# In[22]:


# display the percentage of borrower state
n_state = df_loan['BorrowerState'].value_counts().sum()
state_order = df_loan['BorrowerState'].value_counts().index
sb.countplot(data=df_loan, x='BorrowerState', color=base_color, order=state_order);

max_state = df_loan['BorrowerState'].value_counts()

# get the current tick locations and labels
locs, labels = plt.xticks(rotation=90) 

# loop through each pair of locations and labels
for loc, label in zip(locs, labels):

    # get the text property for the label to get the correct count
    count = max_state[label.get_text()]
    pct_string = '{:d}%'.format(int(100*count/n_state))

    # print the annotation just below the top of the bar
    plt.text(loc, count+2, pct_string, ha = 'center', color = 'black')

# change the figure size
sb.set(rc={'figure.figsize':(15,10)});


# ## Borrowers Occupation Frequencies

# In[23]:


# display top borrower occupation
oc_order = df_loan['Occupation'].value_counts().nlargest(15).index
sb.countplot(data = df_loan, y = 'Occupation', color = base_color, order = oc_order);


# ## Borrowers Own Home

# In[24]:


# is the borrower own a home?
df_loan.IsBorrowerHomeowner.value_counts().plot(kind = 'pie', autopct= '%1.1f%%');


# ## Loans Amount Frequencies

# In[25]:


# display loans amount
plt.hist(data = df_loan, x = 'LoanOriginalAmount', bins = 30);


# ## Relation Between Loan Amount and Borrower Income

# In[27]:


# relation between loan amount and borrower income
plt.scatter(data = df_loan, x = 'LoanOriginalAmount', y = 'StatedMonthlyIncome')
plt.title('Relation Between Loan Amount and Borrower Income')
plt.xlabel('Loan Amount')
plt.ylabel('Monthly Income');


# In[28]:


# employ transparency and jitter 
sb.regplot(data = df_loan, x = 'LoanOriginalAmount', y = 'StatedMonthlyIncome', truncate=False, x_jitter=0.3)
plt.ylim(0, 0.7)
plt.title('Relation Between Loan Amount and Borrower Income')
plt.xlabel('Loan Amount')
plt.ylabel('Monthly Income (1e5)');


# ## Relation Between Loan Status and Rest Monthly Payment

# In[31]:


# make loan status ordered
loan_status = ['Completed', 'Current', 'Defaulted', 'FinalPaymentInProgress', 'Chargedoff', 'Cancelled']
lstatus = pd.api.types.CategoricalDtype(ordered=True, categories=loan_status)

# taking the borrowers they have loan duration more than their employment duration 
emp = df_loan.loc[(df_loan.EmploymentStatusDuration < df_loan.Term),['EmploymentStatusDuration', 'Term', 'LoanStatus']].copy()
# the rest loan months after employment contract ended = the loan months - the rest months in employment
emp['EmploymentRest'] = emp['Term'] - emp['EmploymentStatusDuration']
emp['Lstatus'] = df_loan['LoanStatus'].astype(lstatus);


# relation between the employment contract duration < loan duration .. Is affect on loan status?
sb.violinplot(data= emp, x='Lstatus', y= 'EmploymentRest')
plt.title('Relation Between Loan Status and Rest Monthly Payment')
plt.xlabel('Loan Status')
plt.ylabel('Rest Monthly Payment');


# ## Relation Between Income Range and The Payment Months of Loan

# In[32]:


# take the data with income range
income_range = df_loan.loc[df_loan['IncomeRange'].isin(['$1-24,999', '$25,000-49,999', '$50,000-74,999','$75,000-99,999','$100,000+'])].copy()

# relation between income range and the payment months of loan
g = sb.FacetGrid(data = income_range, col = 'IncomeRange', row = 'Term', height = 2.5,
                margin_titles = True)
g.map(plt.scatter, 'IncomeRange', 'Term');


# In[34]:


# re-arrange the data
pros_loan = {'#ofLoans': [1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8],
                              'Total': [219842, 156859, 75895,  26747,6731, 1671, 422, 37, 6771, 4049, 1813, 624, 153, 36, 25, 1, 542, 318, 147, 40, 4, 6, 4, 2],
                             'PaymentStatus': ['on time', 'on time', 'on time', 'on time', 'on time', 'on time', 'on time', 'on time',
                                       'less month late', 'less month late','less month late','less month late','less month late','less month late','less month late','less month late',
                                       'plus month late', 'plus month late','plus month late','plus month late','plus month late','plus month late','plus month late','plus month late']}
total_pros_loan = pd.DataFrame(pros_loan)
total_pros_loan.head()


# ## Relation Between Total Prosper Loans and Payment Status

# In[35]:


# display the relation between number of prosper loans vs. (payment on time, late < month and late > month).. 
sb.catplot(data=total_pros_loan, x='#ofLoans', y='Total', hue='PaymentStatus', height=10);
plt.title('Relation Between Total Prosper Loans and Payment Status')
plt.xlabel('Total Prosper Loans')
plt.ylabel('Total Status Frequencies');


# ## Conclusion
# The conclusion of the investigation clarifies that the most exist loans status are current, and completed. Regarding loans categories, loans are for debt consolidation, auto, home improvement, respectively. For borrowers state, CA is got the most loans proportion by 13% followed by TX, FL and NY equally by 6%. For the borrower's occupation, professional has got the most numbers of loans followed by computer programmer and executive. <br>
# Also, the conclusion that there is 50.5% of borrowers they owner home while there is 49.5% of them they didn't own. Additionally, the range of most loans amount is between 5000 and 15000. <br>
# Also, there is a positive and weak relationship between the loan amount and the borrower income.  Finally, if the prosper loans was a lot, that will lead to late occurring in payment, either in less than a month or plus a month.

# In[ ]:




