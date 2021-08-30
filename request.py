import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'math_1':100,'math_2':100,'math_3':100,'phy_1':100,'phy_2':100,'phy_3':85,'chem_1':100,'chem_2':85,'chem_3':95,'gender':1,'sleeping_hours':5,'distance_to_school (kms)':25,'school_type':1,'income(Rs)':20000})

print(r.json())