import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request


#Creating record in company amd address table

@app.route('/create/join', methods=['POST'])
def company_address():
    try:        
        _json = request.json
        Company_name = _json['company_name']
        Year = _json['year_established']
        Type = _json['type']
       # Company_id = _json['company_id']
        Street_name = _json['street_name']
        City = _json['city']
        _Country = _json['Country']	
        if id and Company_name and Year and Type  and Street_name and City and _Country and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            Q1 = "INSERT INTO company(company_name,year_established,type) VALUES(%s, %s, %s)"
            data = (Company_name, Year, Type)            
            cursor.execute(Q1, data)
            conn.commit()
            last_id = cursor.lastrowid
            Q2 = "INSERT INTO address(company_id,street_name,city,Country) VALUES(%s, %s, %s,%s)"
            data3 = (last_id, Street_name,City,_Country)            
            cursor.execute(Q2, data3)
            conn.commit()
            respone = jsonify('Details of company added Successfully!!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 


#READ ALL RECORDS FROM TABLE COMPANY     
@app.route('/comp')
def comp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT company_id, company_name, year_established, type FROM company")
        comp_details = cursor.fetchall()
        respone = jsonify(comp_details)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 



#UPDATE A RECORD IN TABLE COMPANY

@app.route('/update/comp', methods=['PUT'])
def update_company():
    try:
        _json = request.json
        Company_name = _json['company_name']
        Year = _json['year_established']
        Type = _json['type']
        Id = _json['company_id']
        if Company_name and Year and Type  and request.method == 'PUT':			
            Q1 = "UPDATE company SET company_name=%s, year_established=%s, type=%s WHERE company_id=%s"
            data =  (Company_name, Year, Type,Id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(Q1, data)
            conn.commit()
            respone = jsonify('Company items updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

# DELETE RECORD FROM COMPANY TABLE

@app.route('/comp', methods=['DELETE'])
def delete_company():
    try:
        _json = request.json
        Id = _json['company_id']
       
        if Id and request.method == 'DELETE':			
            sqlQuery = "DELETE FROM company WHERE company_id=%s"
            data =  ( Id )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, data)
            conn.commit()
            respone = jsonify('records updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()



#READ All RECORD FROM ADDRESS TABLE
@app.route('/add')
def add():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT company_id,address_id,street_name, city,Country FROM address")
        address_Rows = cursor.fetchall()
        respone = jsonify(address_Rows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 



# UPDATE A RECORD IN ADDRESS TABLE

@app.route('/update/add', methods=['PUT'])
def update_add():
    try:
        _json = request.json
        Company_id = _json['company_id']
        Address_id = _json['address_id']
        Street_name = _json['street_name']
        City = _json['city']
        _Country = _json['Country']
        if Address_id and Street_name and City and _Country and Company_id and request.method == 'PUT':			
            sqlQuery = "UPDATE address SET address_id=%s,street_name=%s, city=%s, Country=%s WHERE company_id=%s"
            data = (Address_id,Street_name, City, _Country,Company_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, data)
            conn.commit()
            respone = jsonify('Address table updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
    
# DELETE RECORD FROM ADDRESS TABLE

@app.route('/add/delete', methods=['DELETE'])
def delete_address():
    try:
        _json = request.json
        Id = _json['company_id']
        if Id and request.method == 'DELETE':			
            Q1 = "DELETE FROM address WHERE company_id=%s"
            data =  ( Id )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(Q1, data)
            conn.commit()
            respone = jsonify('records updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
          
     
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()

