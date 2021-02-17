#Api Connections
from ApiConnections import *

def Filter(alerts):

    filtered_alerts = []
    artifacts = []

    for alert in alerts:

        for artifact in alert['artifacts']:
            if not artifact['data'] in artifacts:
                artifacts.append(artifact['data'])
                filtered_alerts.append(alert)

    msg = "Se realizó el filtrado. De " +  str(len(alerts)) + " alertas se crearon solo " + str(len(filtered_alerts)) + " casos"
    Logging("[INFO]",msg)

    return filtered_alerts

def CreateCase(alert):
    
    tasks = [
        CaseTask(title='Revisión', status='Waiting', flag=True)
    ]

    customFields = CustomFieldHelper()\
        .add_boolean('booleanField', True)\
        .add_string('businessImpact', 'HIGH')\
        .add_date('occurDate', int(time.time())*1000)\
        .add_number('cvss', 9)\
        .build()

    artifacts = ""
    for artifact in alert['artifacts']:
        artifacts += "*" + artifact['data'] + "* " 

    title_case = alert['id']
    case = Case(title=title_case,
                tlp=3,
                flag=True,
                tags=['TheHive4Py', artifacts],
                description='N/A',
                tasks=tasks,
                customFields=customFields)

    case_id = None
    response = apiH.create_case(case)

    if response.status_code == 201:
        case_id = response.json()['id']
        case_number = response.json()['caseId']
        msg = "Se creó correctamente el caso numero " +  str(case_number) + " con id " + case_id
        Logging("[INFO]",msg)

    else:
        Logging("[ERROR]","No fue posible crear el caso, la Api falló")
    
    return case_id

def CreateCaseObservable(artifact, case_id):

    try:       
        caseObservable = CaseObservable(dataType=artifact['dataType'],
                                data=artifact['data'],
                                tlp=artifact['tlp'],
                                ioc=artifact['ioc'],
                                tags=artifact['tags'],
                                message=artifact['message']
                                )

    except KeyError as e:
        caseObservable = CaseObservable(dataType=artifact['dataType'],
                                data=artifact['data'],
                                tlp=artifact['tlp'],
                                ioc=False,
                                tags=artifact['tags'],
                                message=artifact['message']
                                )

    response = apiH.create_case_observable(case_id, caseObservable)

    if response.status_code == 201:

        artifact_id = response.json()['id']
        msg = "Se asoció correctamente el observable " + artifact['data'] + " con el caso " + case_id
        Logging("[INFO]",msg)
        return artifact_id

    else:
        msg = "No fue posible crear el observable para el caso " + case_id + ", la Api falló"
        Logging("[ERROR]",msg)
        return None

def SearchAnalyzers(data_type):

    analyzers = apiC.analyzers.get_by_type(data_type)
    return analyzers

def Logging(title, message):

    date = time.strftime("%a %d-%m-%y %H:%M:%S")
    LogFile = open("ApiTheHive.log", "a+")
    Log = "ApiTheHive: " + date + " " + title + " " + message
    print(Log)
    LogFile.write(Log + "\n")
    LogFile.close()

