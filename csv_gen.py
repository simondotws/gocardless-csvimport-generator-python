import gocardless_pro
import csv

token = os.environ['ACCESS_TOKEN']
client = gocardless_pro.Client(access_token=token, environment='sandbox')

#Create empty array
array = []

#Setup the search query, we are using created from
mandates = client.mandates.list(params={"created_at[gte]": "2021-04-14T00:00:00.123Z"})


for mandate in mandates.records:
    customer = client.customers.get(mandate.links.customer)
    bankaccount = client.customer_bank_accounts.get(mandate.links.customer_bank_account)
    array.append([mandate.id,customer.id,customer.given_name,customer.family_name,customer.company_name,customer.email,bankaccount.currency])

while mandates.after:
    mandates = client.mandates.list(params={"created_at[gte]": "2021-04-14T00:00:00.123Z", "after": mandates.after})

    for mandate in mandates.records:
        customer = client.customers.get(mandate.links.customer)
        bankaccount = client.customer_bank_accounts.get(mandate.links.customer_bank_account)
        array.append([mandate.id,customer.id,customer.given_name,customer.family_name,customer.company_name,customer.email,bankaccount.currency])

    continue
with open('customers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['mandate.id','customer.id','customer.given_name','customer.family_name','customer.company_name','customer.email','payment.amount','payment.currency','payment.description','payment.charge_date'])

    for y in array:
        writer.writerow([y[0],y[1],y[2],y[3],y[4],y[5],'',y[6],'',''])

print('done')
