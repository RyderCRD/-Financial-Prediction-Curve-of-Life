import pandas as pd
import matplotlib.pyplot as plt

# 初始资本
initial_capital = 5.0
# 每月收入
monthly_income = 3.0
# 每月花费
monthly_outcome = 1.0
# 每月房租
monthly_rent = 0.5

# 初始年龄
initial_age = 25
# 退休年龄
retirement_age = 60
# 终点年龄
final_age = 90

# 投资比例百分点
investment_ratio = 70.0
# 投资年利百分点
annual_interest_rate = 4.0

# 买房价格
house_price = 300.0
# 买房首付
down_payment = 100.0
# 买房年龄
purchasing_age = 32
# 房贷利率百分点
lending_rate = 6.5
# 贷款年数
loan_period = 12.0

# 结婚年龄
marriage_age = 30
# 结婚花费
marriage_cost = 40
# 对方月收入
h_monthly_income = 1.8
# 对方月花费
h_monthly_outcome = 1.0
# 对方退休年龄
h_retirement_age = 50


#------------------------------------------------------------------

prediction_range = range(initial_age, final_age + 1, 1)

# 每年不算住房的净收入
yearly_net_income = pd.Series(0, index=prediction_range)
yearly_net_income.iloc[0] = initial_capital
yearly_net_income.loc[:retirement_age] += monthly_income * 12
yearly_net_income -= monthly_outcome * 12
yearly_net_income.loc[retirement_age:] += monthly_outcome * 4

# 不投资不买房的情况
no_investment_case = (yearly_net_income - (monthly_rent * 12)).cumsum()

# 投资不买房的情况
compound_interest = [yearly_net_income.iloc[0] - (monthly_rent * 12)]
for income in yearly_net_income[1:]:
    compound_interest.append(compound_interest[-1] * (investment_ratio / 100.0) * (annual_interest_rate / 100.0 + 1) + compound_interest[-1] * ((100 - investment_ratio) / 100) + income - (monthly_rent * 12))
investment_case = pd.Series(compound_interest, index=prediction_range)

# 不投资要买房的情况
house_cost = pd.Series(0, index=prediction_range)
house_cost.loc[purchasing_age] = down_payment
house_cost.loc[purchasing_age:purchasing_age+loan_period-1] += (house_price - down_payment) / loan_period
debt = pd.Series(0, index=prediction_range)
debt.loc[purchasing_age:] = house_price
debt -= house_cost.cumsum()
debt_interest = debt.shift().fillna(0) * lending_rate / 100.0
rent_before_purchasing = pd.Series(monthly_rent * 12, index=prediction_range)
rent_before_purchasing.loc[purchasing_age:] = 0
house_without_investment_case = (yearly_net_income - house_cost - debt_interest - rent_before_purchasing).cumsum()

# 投资且要买房的情况
compound_interest_with_house = [yearly_net_income.iloc[0] - house_cost.iloc[0] - debt_interest.iloc[0] - rent_before_purchasing.iloc[0]]
for i in range(1, len(prediction_range)):
    compound_interest_with_house.append(compound_interest_with_house[-1] * (investment_ratio / 100.0) * (annual_interest_rate / 100.0 + 1) + compound_interest_with_house[-1] * ((100 - investment_ratio) / 100) + yearly_net_income.iloc[i] - house_cost.iloc[i] - debt_interest.iloc[i] - rent_before_purchasing.iloc[i])
house_with_investment_case = pd.Series(compound_interest_with_house, index=prediction_range)

# 不投资 + 买房 + 结婚
h_yearly_net_income = pd.Series(0, index=prediction_range)
h_yearly_net_income[marriage_age] -= marriage_cost
h_yearly_net_income.loc[marriage_age:h_retirement_age] += h_monthly_income * 12
h_yearly_net_income.loc[marriage_age:] -= h_monthly_outcome * 12
h_yearly_net_income.loc[h_retirement_age:] += h_monthly_outcome * 4
house_marriage_without_investment_case = (yearly_net_income + h_yearly_net_income - house_cost - debt_interest - rent_before_purchasing).cumsum()

# 投资 + 买房 + 结婚
h_compound_interest_with_house = [yearly_net_income.iloc[0] + h_yearly_net_income.iloc[0] - house_cost.iloc[0] - debt_interest.iloc[0] - rent_before_purchasing.iloc[0]]
for i in range(1, len(prediction_range)):
    h_compound_interest_with_house.append(h_compound_interest_with_house[-1] * (investment_ratio / 100.0) * (annual_interest_rate / 100.0 + 1) + h_compound_interest_with_house[-1] * ((100 - investment_ratio) / 100) + yearly_net_income.iloc[i] + h_yearly_net_income.iloc[i] - house_cost.iloc[i] - debt_interest.iloc[i] - rent_before_purchasing.iloc[i])
house_marriage_with_investment_case = pd.Series(h_compound_interest_with_house, index=prediction_range)


# 画走势线
investment_case.plot(color='tab:blue', label='investment, single, rent apartment')
house_marriage_with_investment_case.plot(color='tab:olive', label='investment, marriage, purchase house')
house_with_investment_case.plot(color='tab:green', label='investment, single, purchase house')
no_investment_case.plot(color='tab:orange', label='no investment, single, rent apartment')
house_without_investment_case.plot(color='tab:brown', label='no investment, single, purchase house')
house_marriage_without_investment_case.plot(color='tab:red', label='no investment, marriage, purchase house')

# 显示预测图像
plt.grid(linestyle='-.')
plt.xlabel('age')
plt.ylabel('money')
plt.title("Financial Prediction Curve of Life")
plt.legend(loc = 'upper left')
plt.show()
