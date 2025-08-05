#from erp_enh.erp_enhancements.doctype.ctc_salary_structure.ctc_salary_structure import salary_slip_to_dfs  as sdf, fetch_ytd  as ftd,Custom_salary_str_to_dfs as cdf

prev_date = frappe.utils.getdate('03-31-' + str(frappe.utils.getdate(frappe.utils.today()).year-1))
#sal_slip = frappe.db.get_value('Salary Slip',{'employee' : doc.employee, 'end_date': prev_date},'name')
#cum_var = frappe.db.get_value('Salary Detail',{'parent':sal_slip, 'salary_component' : 'Basic'},'year_to_date')
sal_date = frappe.utils.getdate(doc.start_date)
rating = 0

ytd1 = 0
ytd2 = 0 
ytd3 = 0
ytd4 = 0
ytd5 = 0
ytd6 = 0
ytd7 = 0
ytd8 = 0
ytd9 = 0
ytd10 = 0
ytd11 = 0

base = frappe.db.get_list('Salary Structure Assignment',{'employee':doc.employee,'from_date': ('<',frappe.utils.getdate(doc.end_date))},'base',order_by='name')[-1]['base']
#ytd = frappe.db.get_value('Salary Structure Assignment',{'employee':doc.employee,'from_date': ('<',frappe.utils.getdate(doc.end_date))},'taxable_earnings_till_date')[-1]['taxable_earnings_till_date']

base = float(base*doc.payment_days/doc.total_working_days)

str_df = frappe.call('erp_enh.erp_enhancements.doctype.ctc_salary_structure.ctc_salary_structure.Custom_salary_str_to_dfs',start_date=doc.start_date,employee=doc.employee,ctc=base)
rating = frappe.db.get_value('Appraisal',{'employee':doc.employee, 'end_date' : prev_date},'total_score')


basic = 0
hra = 0 
ca = 0
sa = 0
variable =False
chk1 = False
chk2 = False
chk3 = False
chk4 = False
chk5 = False
chk6 = False
chk7 = False
chk8 = False
chk9 = False
chk10 = False
chk11 = False
comp_remove = []

#doc.gross_pay = float(base)
#doc.base_gross_pay = float(base)
lst = []
for d in doc.as_dict().earnings:
    print(d.salary_component)
    lst.append(d.salary_component)
    
for d in doc.as_dict().deductions:
    print(d.salary_component)
    lst.append(d.salary_component)
    
for index, r in str_df.iterrows():
    
    if not r['salary_component'] in lst:
        row = doc.append(r['component_type'], {})
        row.salary_component = r['salary_component']
        row.amount = float(r['amount'])
        row.year_to_date = float(r['ytd_new']) 
    
    if r['salary_component'] in lst:
        for d in doc.earnings:
            if d.salary_component == r['salary_component']:
                d.amount = float(r['amount'])
                d.year_to_date = float(r['ytd_new']) 

if r['salary_component'] in lst:
        for d in doc.deductions:
            if d.salary_component == r['salary_component']:
                d.amount = float(r['amount'])
                d.year_to_date = float(r['ytd_new'])    


ern = 0
ernytd = 0 
for d in doc.earnings:
    ern = ern + d.amount
    ernytd = ernytd + d.year_to_date
doc.gross_pay = ern
doc.base_gross_pay = ern
doc.gross_year_to_date = ernytd



ded = 0
dedytd = 0 
for d in doc.deductions:
    if not d.year_to_date:
        d.year_to_date = 0
    if not d.amount:
        d.amount = 0    
        
    if d.salary_component == 'Income Tax' and base*12 <= 700000:
        d.amount = 0
        d.year_to_date = 0
    ded = ded + d.amount
    dedytd = dedytd + d.year_to_date

doc.total_deduction = ded


doc.net_pay = doc.gross_pay - doc.total_deduction
doc.base_net_pay = doc.gross_pay - doc.total_deduction
doc.rounded_total = round((doc.gross_pay - doc.total_deduction),0)
doc.base_rounded_total = round((doc.base_gross_pay - doc.base_total_deduction),0)
doc.month_to_date = doc.gross_pay - doc.total_deduction
doc.base_month_to_date = doc.base_gross_pay - doc.base_total_deduction
doc.year_to_date = doc.gross_year_to_date - doc.total_deduction
#doc.base_year_to_date = doc.gross_year_to_date - doc.total_deduction
doc.base_gross_year_to_date = doc.gross_year_to_date
doc.base_year_to_date = doc.base_gross_year_to_date - doc.base_total_deduction

