import numpy as np
import pandas as pd
import os
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression

df = pd.read_excel('./Fish.xlsx')
"""
Column Structure

'Row'           : 행번호
'Name'          : 물고기 종 이름
'Species'       : 물고기 종에 따른 번호 배부

- SPECIES       : 어느 종에 해당하는지 Bool 데이터로 존재
   -> 'Species.Eq.1' : Bream     (도미)
   -> 'Species.Eq.2' : Whitefish (백어)
   -> 'Species.Eq.3' : Roach     (잉어)
   -> 'Species.Eq.4' : Parkki 
   -> 'Species.Eq.5' : Smelt     (빙어)
   -> 'Species.Eq.6' : Pike      (강꼬치고기)
   -> 'Species.Eq.7' : Perch     (농어)

'Weight_g'      : 물고기의 무게 (단위 : 그램(g))
'Weight_g.Ln'   : 물고기의 무게를 로그로 바꾸어 표현

'Length_cm'     : 물고기의 길이 (단위 : 센티미터(cm))
'Length_cm.Ln'  : 물고기의 길이를 로그로 바꾸어 표현

'Height_pct'    : 물고기의 높이 (단위 : 퍼센트(%))
'Height_pct.Ln' : 물고기의 높이을 로그로 바꾸어 표현

'Width_pct'     : 물고기의 폭 (단위 : 퍼센트(%))
'Width_pct.Ln'  : 물고기의 폭을 로그로 바꾸어 표현

"""


dummy = df.iloc[:, [2]]
y = df.loc[:, ['Weight_g.Ln']]
x = df.loc[:, ['Length_cm.Ln', 'Width_pct.Ln', 'Height_pct.Ln']]

# 무게에 따른 물고기 길이와 폭의 상관관계를 확인하기 위함
y.columns=['weight']
x.columns=['length', 'width', 'height']
dummy.columns=['species']

# 해당 상관관계를 새로운 데이터프레임에 집어넣어서 정리
new_df = pd.concat([y, x, dummy], axis=1)

# 최소 자승법 (Ordinary Least Squares)
Linear = sm.OLS(y, x)
result1 = Linear.fit()
print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
print(result1.summary())

Linear = smf.ols(formula='weight ~ length * width', data=new_df)
result = Linear.fit()
print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
print(result.summary())

Linear = smf.ols(formula='weight ~ length + width + height', data=new_df)
result = Linear.fit()
print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
print(result.summary())

Linear = smf.ols(formula='weight ~ length + width + height + C(species)', data=new_df)
result = Linear.fit()
print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
print(result.summary())

Linear = smf.ols(formula='weight ~ length * width * height + C(species)', data=new_df)
result = Linear.fit()
print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
print(result.summary())

Linear = smf.ols(formula='weight ~ length * width + C(species)', data=new_df)
result = Linear.fit()
print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
print(result.summary())


inner = np.array([[3.7, 3.9, 3.4, 2]])
result1.predict([3.7, 3.9, 3.4])
inp = pd.DataFrame([[3.7, 3.9, 3.4, 1]])
inp.columns = ['length', 'width', 'height', 'species']

result.predict(inp)


print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
print(result.summary())


model = LinearRegression()
result = model.fit(x, y)