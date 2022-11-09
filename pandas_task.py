import pandas as pd
import numpy as np

first_file = 'Energy Indicators.xls'
second_file = 'world_bank.csv'
third_file = 'scimagojr country rank 1996-2021.xlsx'
ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'}

energy = pd.read_excel(first_file, skiprows=18, nrows=227, header=None)
del energy[0]
del energy[1]
energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

def gigajouls(x):
    return 1000000*x

def replace_empty(x):
    return np.NaN if x == '...' else x


def refactor(x):
    res = ''.join([i for i in x if not i.isdigit()])
    if res.__contains__('('):
        n = res.index('(')
        res = res[:n-1]
    if res == 'Democratic People\'s Republic of Korea':
        res = 'South Korea'
    if res == 'United States of America':
        res = 'United States'
    if res == 'United Kingdom of Great Britain and Northern Ireland':
        res = 'United Kingdom'
    if res == 'China, Hong Kong Special Administrative Region':
        res = 'Hong Kong'
    return res


energy['Energy Supply'] = energy['Energy Supply'].apply(replace_empty)
energy['Energy Supply'] = energy['Energy Supply'].apply(gigajouls)
energy['Energy Supply per Capita'] = energy['Energy Supply per Capita'].apply(replace_empty)
energy['Country'] = energy['Country'].apply(refactor)

gdp = pd.read_csv(second_file, sep=',', dtype=None, skiprows=4, encoding='utf-8')
del gdp['Unnamed: 66']


def refactor_gdp(x):
    if x == 'Korea, Rep.':
        return 'South Korea'
    elif x == 'Iran, Islamic Rep.':
        return 'Iran'
    elif x == 'Hong Kong SAR, China':
        return 'Hong Kong'
    else:
        return x


gdp['Country Name'] = gdp['Country Name'].apply(refactor_gdp)

ScimEn = pd.read_excel(third_file)


def answer_one():
    res = ScimEn.iloc[:15]
    del res['Region']
    res = pd.merge(res, energy, on='Country')
    res = pd.merge(res, gdp[['Country Name', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']],left_on='Country', right_on='Country Name')
    del res['Country Name']
    res = res.set_index(['Country'])

    return res


def answer_two():
    Top15 = answer_one()
    Top15['Average GDP'] = Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].sum(
        axis=1) / Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].count(axis=1)
    avgGDP = pd.Series(Top15['Average GDP'])
    avgGDP.sort_values(ascending=False, inplace=True)
    return avgGDP


def answer_three():
    Top15 = answer_one()
    Top15['Average GDP'] = Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].sum(
        axis=1) / Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].count(axis=1)
    Top15.sort_values(by='Average GDP', ascending=False, inplace=True)
    return Top15['2015'].iloc[5] - Top15['2006'].iloc[5]


def answer_four():
    Top15 = answer_one()
    Top15['Self-Citations to Total Citations'] = Top15['Self-citations'] / Top15['Citations']
    Top15.sort_values(by='Self-Citations to Total Citations', ascending=False, inplace=True)
    return Top15.index.values[0], Top15['Self-Citations to Total Citations'].iloc[0]


def answer_five():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15.sort_values(by='Population', ascending=False, inplace=True)
    return Top15.index.values[2]


def answer_six():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable documents per person'] = Top15['Citable documents'] / Top15['Population']
    return Top15['Citable documents per person'].corr(Top15['Energy Supply per Capita'])


def answer_seven():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    df_ContinentDict = pd.DataFrame([ContinentDict], index=['Region']).T
    Top15 = pd.concat([Top15, df_ContinentDict], axis=1)
    Top15.reset_index(inplace=True)

    res = pd.DataFrame()
    res['size'] = Top15.groupby(['Region'])['index'].count()
    res['sum'] = Top15.groupby(['Region'])['Population'].sum()
    res['mean'] = Top15.groupby(['Region'])['Population'].mean()
    res['std'] = Top15.groupby(['Region'])['Population'].std()
    return res


with pd.option_context('display.max_rows', None, 'display.max_columns', None, ):
    print("Answer One:")
    print(answer_one())
    print("Answer Two:")
    print(answer_two())
    print("Answer Three:")
    print(answer_three())
    print("Answer Four:")
    print(answer_four())
    print("Answer Five:")
    print(answer_five())
    print("Answer Six:")
    print(answer_six())
    print("Answer Seven:")
    print(answer_seven())
