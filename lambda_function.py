import boto3
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("FriendsDDB")

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_file_name = event['Records'][0]['s3']['object']['key']
    resp = s3_client.get_object(Bucket=bucket_name,Key=s3_file_name)
    data = resp['Body'].read().decode("utf-8")
    print(f' Data dopo lettura body\n{data}')
    
    student_clear = []
    student_clear_final = []
    Students = data.split("\t")
    for student in Students:
        student_clear.append(student.split("\r\n"))
    
    for lista in student_clear:
        student_clear_final.extend(lista)
        
    print(f' lista pulita :{student_clear_final}')
    
    if student_clear_final[-1] == '':
        student_clear_final.pop()
        
    passo = 3 # reader step

    # Utilizza un ciclo for per scorrere la lista di 3 in 3
    for i in range(0, len(student_clear_final), passo):
        # Estrai i prossimi 3 elementi
        tre_elementi = student_clear_final[i:i+passo]
        
        # Stampa ogni elemento con il formato specificato
        print(f' Id: {tre_elementi[0]}')
        print(f' Name: {tre_elementi[1]}')
        print(f' Subject: {tre_elementi[2]}')
        
        # add to dynamodb
        try:
           table.put_item(
                Item = {
                    "Id"        : tre_elementi[0],
                    "name"      : tre_elementi[1],
                    "Subject"   : tre_elementi[2]
               }
            )
        except Exception as e:
           print(f"Error: {str(e)}")